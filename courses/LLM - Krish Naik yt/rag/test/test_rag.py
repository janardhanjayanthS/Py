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