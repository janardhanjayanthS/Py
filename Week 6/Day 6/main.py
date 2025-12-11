from constants import OPENAI_API_KEY, connection
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector

embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=OPENAI_API_KEY)
collection_name = "my_docs"

vector = PGVector(
    embeddings=embeddings,
    collection_name=collection_name,
    connection=connection,
    use_jsonb=True,
)


documents = [
    Document(
        page_content="PostgreSQL is a powerful database",
        metadata={"source": "intro.txt", "page": 1},
    ),
    Document(
        page_content="Docker makes deployment easier",
        metadata={"source": "docker.txt", "page": 1},
    ),
]

if __name__ == "__main__":
    # vector.add_documents(documents=documents)
    results = vector.similarity_search(query="tell me about databases", k=2)
    for result in results:
        print(result)

