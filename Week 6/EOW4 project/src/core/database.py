import io
from ast import Bytes

import pyPDF2
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from src.core.constants import OPENAI_API_KEY, OPENAI_EMBEDDING_MODEL, PG_PWD

connection = f"postgresql+psycopg://postgres:{PG_PWD}@localhost:5432/vector_db"

embeddings = OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL, api_key=OPENAI_API_KEY)


CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    length_function=len,
    separators=["\n\n", "\n", " ", ""],
)

vector_store = PGVector(
    embeddings=embeddings,
    collection_name="uploaded_documents",
    connection=connection,
    use_jsonb=True,
)


def add_file_as_embedding(contents: Bytes, filename: str) -> None:
    documents = get_documents_from_file_content(content=contents, filename=filename)
    vector_store.add_documents(documents)


def get_documents_from_file_content(content: Bytes, filename: str) -> list[Document]:
    pdf_file = io.BytesIO(content)
    pdf_reader = pyPDF2.PdfReader(pdf_file)

    page_documents = []

    for page_num, page in enumerate(pdf_reader.pages, start=1):
        text = page.extract_text()

        if text:
            page_documents.append(
                Document(
                    page_content=text, metadata={"source": filename, "page": page_num}
                )
            )

    # chunked document
    chunked_document = text_splitter.split_document(page_documents)
    return chunked_document
