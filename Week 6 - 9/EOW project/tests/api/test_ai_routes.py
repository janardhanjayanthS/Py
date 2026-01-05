from unittest.mock import AsyncMock, MagicMock, patch

from fastapi import status


class TestAIQuery:
    """Tests for AI query endpoint"""

    @patch("src.api.routes.ai.get_agent")
    async def test_ai_query_success(self, mock_get_agent, client):
        """Test successful AI query"""
        # Mock AI response
        mock_response = MagicMock()
        mock_response.content = "This is an AI generated response"
        mock_response.usage_metadata = {"input_tokens": 100, "output_tokens": 50}

        mock_agent = MagicMock()
        mock_agent.ainvoke = AsyncMock(return_value=mock_response)
        mock_get_agent.return_value = mock_agent

        query_data = {"query": "What is the meaning of life?"}
        response = client.post("/ai/query", json=query_data)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["response"] == "success"
        assert "ai response" in data["message"]
        assert "token cost" in data["message"]
        assert len(data["message"]["ai response"]) > 0

    @patch("src.api.routes.ai.get_agent")
    async def test_ai_query_with_markdown_cleanup(self, mock_get_agent, client):
        """Test that AI response markdown is cleaned"""
        mock_response = MagicMock()
        mock_response.content = "**Bold text** and *italic* with \\backslashes"
        mock_response.usage_metadata = {"input_tokens": 50, "output_tokens": 25}

        mock_agent = MagicMock()
        mock_agent.ainvoke = AsyncMock(return_value=mock_response)
        mock_get_agent.return_value = mock_agent

        query_data = {"query": "Test query"}
        response = client.post("/ai/query", json=query_data)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        # Check that markdown and special characters are cleaned
        ai_response = data["message"]["ai response"]
        assert "**" not in ai_response
        assert "*" not in ai_response
        assert "\\" not in ai_response

    def test_ai_query_empty_query(self, client):
        """Test AI query with empty string"""
        query_data = {"query": ""}
        response = client.post("/ai/query", json=query_data)

        # Should reject empty queries due to validation
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_ai_query_missing_query_field(self, client):
        """Test AI query without query field"""
        response = client.post("/ai/query", json={})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @patch("src.api.routes.ai.get_agent")
    async def test_ai_query_agent_error(self, mock_get_agent, client):
        """Test AI query when agent raises error"""
        mock_agent = MagicMock()
        mock_agent.ainvoke = AsyncMock(side_effect=Exception("OpenAI API error"))
        mock_get_agent.return_value = mock_agent

        query_data = {"query": "What is AI?"}
        response = client.post("/ai/query", json=query_data)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Error while processing AI query" in response.json()["detail"]

    @patch("src.api.routes.ai.get_agent")
    async def test_ai_query_token_cost_calculation(self, mock_get_agent, client):
        """Test that token cost is calculated correctly"""
        mock_response = MagicMock()
        mock_response.content = "Response"
        mock_response.usage_metadata = {"input_tokens": 1000, "output_tokens": 500}

        mock_agent = MagicMock()
        mock_agent.ainvoke = AsyncMock(return_value=mock_response)
        mock_get_agent.return_value = mock_agent

        query_data = {"query": "Calculate tokens"}
        response = client.post("/ai/query", json=query_data)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        # Token cost should be present and greater than 0
        token_cost = float(data["message"]["token cost"])
        assert token_cost > 0

    @patch("src.api.routes.ai.get_agent")
    async def test_ai_query_long_input(self, mock_get_agent, client):
        """Test AI query with very long input"""
        mock_response = MagicMock()
        mock_response.content = "Response to long query"
        mock_response.usage_metadata = {"input_tokens": 5000, "output_tokens": 100}

        mock_agent = MagicMock()
        mock_agent.ainvoke = AsyncMock(return_value=mock_response)
        mock_get_agent.return_value = mock_agent

        long_query = "What is " + ("very " * 1000) + "long?"
        query_data = {"query": long_query}
        response = client.post("/ai/query", json=query_data)

        assert response.status_code == status.HTTP_200_OK


class TestAIQueryUtils:
    """Tests for AI utility functions"""

    @patch("src.core.ai_utility.ChatOpenAI")
    def test_get_agent_initialization(self, mock_chat_openai):
        """Test that get_agent initializes ChatOpenAI correctly"""
        from src.core.ai_utility import get_agent
        from src.core.constants import AIModels

        mock_instance = MagicMock()
        mock_chat_openai.return_value = mock_instance

        agent = get_agent(AIModels.GPT_4o_MINI)

        # Verify ChatOpenAI was called with correct parameters
        mock_chat_openai.assert_called_once()
        call_kwargs = mock_chat_openai.call_args.kwargs
        assert call_kwargs["model"] == AIModels.GPT_4o_MINI.value
        assert call_kwargs["temperature"] == 0
        assert call_kwargs["stream_usage"] is True

    def test_calculate_token_cost(self):
        """Test token cost calculation"""
        from src.core.ai_utility import calculate_token_cost
        from src.core.constants import AIModels

        token_usage = {"input_tokens": 1000, "output_tokens": 500}

        cost = calculate_token_cost(token_usage, AIModels.GPT_4o_MINI)

        # Cost should be a string representation of a decimal
        assert isinstance(cost, str)
        assert float(cost) > 0

    def test_clean_llm_output(self):
        """Test LLM output cleaning"""
        from src.core.ai_utility import clean_llm_output

        dirty_text = "**Bold** text with *italics* and \\backslashes  extra   spaces"
        cleaned = clean_llm_output(dirty_text)

        # Check markdown and special chars are removed
        assert "**" not in cleaned
        assert "*" not in cleaned
        assert "\\" not in cleaned

        # Check extra whitespace is normalized
        assert "  " not in cleaned

    def test_update_history(self):
        """Test conversation history update"""
        from src.core.ai_utility import update_history
        from src.core.constants import HISTORY
        from src.schema.ai import Query

        # Clear history
        HISTORY.clear()

        mock_result = MagicMock()
        mock_result.content = "AI response"

        query = Query(query="User question")

        update_history(mock_result, query)

        # History should contain both messages
        assert len(HISTORY) == 2
        assert HISTORY[0].content == "User question"
        assert HISTORY[1].content == "AI response"
