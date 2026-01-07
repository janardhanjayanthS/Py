from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# WEB URLS to document
urls: list[str] = []


def get_docs():
    docs = [WebBaseLoader(url).url for url in urls]
    docs_list = []
    for doc in docs:
        for item in doc:
            docs_list.append(item)

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=100, chunk_overlap=50
    )
    doc_splits = text_splitter.split_documents(docs_list)
    return doc_splits
