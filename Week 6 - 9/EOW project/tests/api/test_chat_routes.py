from unittest.mock import MagicMock, patch

from fastapi import status
from langchain_core.documents import Document


class TestChatEndpoint:
    """Tests for chat endpoint with RAG"""

    @patch("src.api.routes.chat.get_conversational_rag_chain")
    @patch("src.api.routes.chat.get_cached_response")
    def test_chat_query_success(
        self, mock_get_cache, mock_get_chain, client, auth_headers, test_user
    ):
        """Test successful chat query with RAG"""
        # No cached response
        mock_get_cache.return_value = None

        # Mock RAG chain response
        mock_response = MagicMock()
        mock_response.content = "Based on your documents, the answer is..."
        mock_response.usage_metadata = {"input_tokens": 500, "output_tokens": 200}

        mock_chain = MagicMock()
        mock_chain.invoke = MagicMock(return_value=mock_response)
        mock_get_chain.return_value = mock_chain

        query_data = {"query": "What does my document say?"}
        response = client.post("/chat", json=query_data, headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["response"] == "success"
        assert "query response" in data["message"]
        assert "token cost" in data["message"]
        assert "response time" in data["message"]

    @patch("src.api.routes.chat.get_cached_response")
    def test_chat_query_from_cache(self, mock_get_cache, client, auth_headers):
        """Test chat query returns cached response"""
        cached_response = "This is a cached response"
        mock_get_cache.return_value = cached_response

        query_data = {"query": "Cached question"}
        response = client.post("/chat", json=query_data, headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["response"] == "success"
        assert data["message"]["query response"] == cached_response
        assert "response time" in data["message"]
        # Token cost should not be present for cached responses
        assert "token cost" not in data["message"]

    def test_chat_query_without_auth_fails(self, client):
        """Test chat query without authentication"""
        query_data = {"query": "Test query"}
        response = client.post("/chat", json=query_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_chat_query_missing_query_field(self, client, auth_headers):
        """Test chat query without query field"""
        response = client.post("/chat", json={}, headers=auth_headers)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @patch("src.api.routes.chat.get_conversational_rag_chain")
    @patch("src.api.routes.chat.get_cached_response")
    def test_chat_query_rag_error(
        self, mock_get_cache, mock_get_chain, client, auth_headers
    ):
        """Test chat query when RAG chain fails"""
        mock_get_cache.return_value = None

        mock_chain = MagicMock()
        mock_chain.invoke = MagicMock(side_effect=Exception("RAG error"))
        mock_get_chain.return_value = mock_chain

        query_data = {"query": "Test query"}
        response = client.post("/chat", json=query_data, headers=auth_headers)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Error while chatting with AI" in response.json()["detail"]

    @patch("src.api.routes.chat.save_to_cache")
    @patch("src.api.routes.chat.get_conversational_rag_chain")
    @patch("src.api.routes.chat.get_cached_response")
    def test_chat_query_saves_to_cache(
        self, mock_get_cache, mock_get_chain, mock_save_cache, client, auth_headers
    ):
        """Test that successful query saves to cache"""
        mock_get_cache.return_value = None

        mock_response = MagicMock()
        mock_response.content = "New response"
        mock_response.usage_metadata = {"input_tokens": 100, "output_tokens": 50}

        mock_chain = MagicMock()
        mock_chain.invoke = MagicMock(return_value=mock_response)
        mock_get_chain.return_value = mock_chain

        query_data = {"query": "New query"}
        response = client.post("/chat", json=query_data, headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK
        # Verify save_to_cache was called
        mock_save_cache.assert_called_once()

    @patch("src.api.routes.chat.get_conversational_rag_chain")
    @patch("src.api.routes.chat.get_cached_response")
    def test_chat_query_with_long_context(
        self, mock_get_cache, mock_get_chain, client, auth_headers
    ):
        """Test chat query with long document context"""
        mock_get_cache.return_value = None

        mock_response = MagicMock()
        mock_response.content = "Response based on long documents"
        mock_response.usage_metadata = {
            "input_tokens": 10000,  # Large input
            "output_tokens": 500,
        }

        mock_chain = MagicMock()
        mock_chain.invoke = MagicMock(return_value=mock_response)
        mock_get_chain.return_value = mock_chain

        query_data = {"query": "Summarize all documents"}
        response = client.post("/chat", json=query_data, headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        # High token cost expected
        token_cost = float(data["message"]["token cost"])
        assert token_cost > 0


class TestRAGChainFunctions:
    """Tests for RAG chain utility functions"""

    @patch("src.core.ai_utility.get_vector_store")
    def test_contextualized_retrieval_without_history(self, mock_vector_store):
        """Test document retrieval without chat history"""
        from src.core.ai_utility import contextualized_retrival

        mock_docs = [
            Document(
                page_content="Test content",
                metadata={"title": "Test Doc", "user_id": 1},
            )
        ]

        mock_store = MagicMock()
        mock_store.similarity_search = MagicMock(return_value=mock_docs)
        mock_vector_store.return_value = mock_store

        input_dict = {"question": "What is this?", "chat_history": [], "user_id": 1}

        result = contextualized_retrival(input_dict)

        # Should return documents
        assert len(result) > 0
        # Should search with original question when no history
        mock_store.similarity_search.assert_called_once()

    @patch("src.core.ai_utility.get_contextualize_rag_chain")
    @patch("src.core.ai_utility.get_vector_store")
    def test_contextualized_retrieval_with_history(
        self, mock_vector_store, mock_contextualize_chain
    ):
        """Test document retrieval with chat history reformulates question"""
        from langchain_core.messages import AIMessage, HumanMessage
        from src.core.ai_utility import contextualized_retrival

        mock_docs = [Document(page_content="Content", metadata={"user_id": 1})]

        mock_store = MagicMock()
        mock_store.similarity_search = MagicMock(return_value=mock_docs)
        mock_vector_store.return_value = mock_store

        mock_chain = MagicMock()
        mock_chain.invoke = MagicMock(return_value="Reformulated question")
        mock_contextualize_chain.return_value = mock_chain

        input_dict = {
            "question": "What about that?",
            "chat_history": [
                HumanMessage(content="Tell me about X"),
                AIMessage(content="X is..."),
            ],
            "user_id": 1,
        }

        result = contextualized_retrival(input_dict)

        # Should call contextualize chain when history exists
        mock_chain.invoke.assert_called_once()
        assert len(result) > 0

    def test_format_docs(self):
        """Test document formatting for LLM"""
        from src.core.ai_utility import format_docs

        docs = [
            Document(
                page_content="First document content", metadata={"title": "Doc 1"}
            ),
            Document(
                page_content="Second document content", metadata={"title": "Doc 2"}
            ),
        ]

        formatted = format_docs(docs)

        # Check formatting includes metadata and content
        assert "DOCUMENT 1" in formatted
        assert "DOCUMENT 2" in formatted
        assert "Metadata Title: Doc 1" in formatted
        assert "Metadata Title: Doc 2" in formatted
        assert "First document content" in formatted
        assert "Second document content" in formatted

    def test_format_docs_unknown_title(self):
        """Test document formatting with missing title metadata"""
        from src.core.ai_utility import format_docs

        docs = [Document(page_content="Content without title", metadata={})]

        formatted = format_docs(docs)

        # Should handle missing title gracefully
        assert "Unknown Title" in formatted
        assert "Content without title" in formatted

    @patch("src.core.ai_utility.get_vector_store")
    def test_contextualized_retrieval_user_filter(self, mock_vector_store):
        """Test that retrieval filters by user_id"""
        from src.core.ai_utility import contextualized_retrival

        mock_docs = [Document(page_content="User doc", metadata={"user_id": 123})]

        mock_store = MagicMock()
        mock_store.similarity_search = MagicMock(return_value=mock_docs)
        mock_vector_store.return_value = mock_store

        input_dict = {"question": "My documents", "chat_history": [], "user_id": 123}

        contextualized_retrival(input_dict)

        # Verify filter was applied
        call_kwargs = mock_store.similarity_search.call_args.kwargs
        assert call_kwargs["filter"] == {"user_id": 123}
