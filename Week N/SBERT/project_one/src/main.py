from os import getenv

from docs import pdf_dir, pdf_files
from dotenv import load_dotenv
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_postgres.vectorstores import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter

_ = load_dotenv()

OPENAI_API_KEY = getenv("OPENAI_API_KEY")
DB_CONNECTION = (
    f"postgresql+psycopg://postgres:{getenv('PG_PWD')}@localhost:5432/new_vector_db"
)


class VectorManager:
    def __init__(self) -> None:
        self.openai_embeddings: OpenAIEmbeddings = OpenAIEmbeddings(
            model="text-embedding-3-small"
        )
        self.sbert_embeddings: HuggingFaceEmbeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )

    def _get_collection_name(self, model_type: str) -> str:
        return "sbert_collection" if model_type == "sbert" else "openai_collection"

    def _get_vector_stores(self, model_type: str = "sbert") -> PGVector:
        embed_model = (
            self.sbert_embeddings if model_type == "sbert" else self.openai_embeddings
        )

        store = PGVector(
            connection=DB_CONNECTION,
            embeddings=embed_model,
            collection_name=self._get_collection_name(model_type=model_type),
            use_jsonb=True,
        )

        store.create_tables_if_not_exists()
        return store

    def store_pdf(self, file_path: str, model_type: str = "sbert") -> None:
        try:
            loader = PyMuPDFLoader(file_path)
            docs = loader.load()

            text_splits = RecursiveCharacterTextSplitter(
                chunk_size=600, chunk_overlap=100
            )
            chunks = text_splits.split_documents(docs)

            store = self._get_vector_stores(model_type=model_type)
            store.add_documents(chunks)
            print("Docs added successfully!")
        except Exception as e:
            print(f"Cannot add docs, Error: {e}")

    def query(
        self, query: str, model_type: str = "sbert", k: int = 5
    ) -> list[Document]:
        store = self._get_vector_stores(model_type=model_type)
        results = store.similarity_search(query, k)
        return results


def add_pdfs(manager: VectorManager, model_type: str = "sbert") -> None:
    for pdf_file in pdf_files:
        pdf_path = f"{pdf_dir}/{pdf_file}"
        print(f"adding {pdf_path} with {model_type} embedding")
        manager.store_pdf(file_path=f"{pdf_dir}/{pdf_file}", model_type=model_type)
        print("-" * 50)


def print_results(results: list[Document]) -> None:
    for i, result in enumerate(results, start=1):
        print(i)
        print("source: ", result.metadata["source"])
        print("page content: ", result.page_content)
        print("-" * 100)


if __name__ == "__main__":
    v_manager = VectorManager()
    # For adding docs
    # add_pdfs(manager=v_manager, model_type="sbert")
    # add_pdfs(manager=v_manager, model_type="openai")

    print("-" * 100)
    llm_query = "what is medical insurance"
    print(f"QUERY: {llm_query}")
    print("Results from Openai")
    print_results(v_manager.query(query=llm_query, model_type="openai"))
    print("-" * 100)
    print("Results from SBERT")
    print_results(v_manager.query(query=llm_query, model_type="sbert"))
