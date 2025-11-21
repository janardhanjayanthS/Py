# From claude
import pytest
from unittest.mock import Mock, patch, MagicMock
from langchain_core.documents import Document

# ============================================================================
# APPROACH 1: Test Individual Components Directly
# ============================================================================

class TestPDFLoading:
    """Test PDF loading and text splitting"""
    
    @patch('langchain_community.document_loaders.PyPDFLoader')
    def test_pdf_loader_called_correctly(self, mock_loader):
        """Test that PDF loader is instantiated with correct path"""
        from langchain_community.document_loaders import PyPDFLoader
        
        # Mock the loader
        mock_loader_instance = Mock()
        mock_loader_instance.load.return_value = [
            Document(page_content="Test content")
        ]
        mock_loader.return_value = mock_loader_instance

        # Your code
        loader = PyPDFLoader('~/Books/algorithms_to_live_by.pdf')
        documents = loader.load()
        
        # Assertions
        mock_loader.assert_called_once_with('~/Books/algorithms_to_live_by.pdf')
        assert len(documents) > 0

    def test_text_splitter_configuration(self):
        """
        tests for text splitter configurations (chunk size, chunk overlap) 
        """
        from langchain_text_splitters import RecursiveCharacterTextSplitter

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1024,
            chunk_overlap=224
        )

        assert text_splitter._chunk_size == 1024
        assert text_splitter._chunk_overlap == 224

    def test_text_splitting_produces_chunks(self):
        """Test that text splitting works correctly"""
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        
        # Create sample document
        long_text = "This is a test. " * 200  # Create long text
        documents = [Document(page_content=long_text)]
        
        # Split documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=100,
            chunk_overlap=20
        )
        split_docs = text_splitter.split_documents(documents)
        
        # Assertions
        assert len(split_docs) > 1
        for doc in split_docs:
            assert len(doc.page_content) <= 120

class TestVectorStore:
    """Test vector store operations"""
    
    @pytest.fixture
    def sample_documents(self):
        """Create sample documents"""
        return [
            Document(page_content="Chapter 1: Introduction to algorithms and optimization."),
            Document(page_content="The authors are Brian Christian and Tom Griffiths."),
            Document(page_content="The book contains 11 chapters covering different topics."),
        ]
    
    @patch('langchain_community.vectorstores.LanceDB')
    @patch('langchain_openai.OpenAIEmbeddings')
    def test_lancedb_vector_store_creation(self, mock_embeddings, mock_lancedb, sample_documents):
        """Test LanceDB vector store creation"""
        # Setup mocks
        mock_lance_instance = Mock()
        mock_vector_store = Mock()
        mock_lance_instance.from_documents.return_value = mock_vector_store
        mock_lancedb.return_value = mock_lance_instance
        
        # Your code
        from langchain_community.vectorstores import LanceDB
        emb = mock_embeddings(api_key="test-key")
        lance_db = LanceDB(uri='./lancedb', embedding=emb)
        vector_store = lance_db.from_documents(sample_documents, emb)
        
        # Assertions
        assert vector_store == mock_vector_store
        mock_lancedb.assert_called_once_with(uri='./lancedb', embedding=emb)
    
    def test_similarity_search_returns_documents(self, sample_documents):
        """Test similarity search returns documents"""
        # Mock vector store
        mock_db = Mock()
        mock_db.similarity_search.return_value = sample_documents[:2]
        
        # Your code
        query = 'Who are the authors of the book'
        result = mock_db.similarity_search(query=query)
        
        # Assertions
        assert len(result) == 2
        assert all(isinstance(doc, Document) for doc in result)
        mock_db.similarity_search.assert_called_once_with(query=query)


class TestRetriever:
    """Test retriever configuration"""
    
    def test_retriever_configuration(self):
        """Test retriever is configured correctly"""
        mock_vector_store = Mock()
        mock_retriever = Mock()
        mock_vector_store.as_retriever.return_value = mock_retriever
        
        # Your code
        retriever = mock_vector_store.as_retriever(
            search_type='similarity',
            search_kwargs={"k": 3}
        )
        
        # Assertions
        mock_vector_store.as_retriever.assert_called_once_with(
            search_type='similarity',
            search_kwargs={"k": 3}
        )
        assert retriever == mock_retriever
    
    def test_format_docs_function(self):
        """Test format_docs helper function"""
        def format_docs(docs):
            return '\n\n'.join(doc.page_content for doc in docs)
        
        # Test data
        docs = [
            Document(page_content="First doc"),
            Document(page_content="Second doc"),
            Document(page_content="Third doc"),
        ]
        
        # Test formatting
        result = format_docs(docs)
        
        assert "First doc" in result
        assert "Second doc" in result
        assert "Third doc" in result
        assert result.count("\n\n") == 2  # Two separators for 3 docs