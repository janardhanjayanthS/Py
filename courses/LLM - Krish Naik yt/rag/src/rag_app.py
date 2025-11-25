from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma  # vector store
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv


load_dotenv("../.env")
loader = PyPDFLoader("~/Books/algorithms_to_live_by.pdf")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=224)
document = loader.load()
document = text_splitter.split_documents(document)


# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# using lanceDB
from langchain_community.vectorstores import LanceDB

emb = OpenAIEmbeddings()
lance_db = LanceDB(uri="./lancedb", embedding=emb)
vector_store = lance_db.from_documents(document, emb)

resutl = vector_store.similarity_search("summerize the first chapter")

from langchain_openai import ChatOpenAI

openai = ChatOpenAI(model="gpt-4o-mini")

# prompt
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    template="""
You are a helpful bot answering user queries
Try to get accurate results for the user query
from the provide context - from below.
<context>
{context}
<context>

question: {question}
""",
)


# retriever
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


content = {"context": retriever | format_docs, "question": RunnablePassthrough()}
rag_chain = content | prompt | openai | StrOutputParser()

query = "how many chapters does the book contain"

result = rag_chain.invoke(query)
print(result)
