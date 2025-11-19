from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = str(os.getenv("OPENAI_API_KEY"))
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = str(os.getenv("LANGCHAIN_API_KEY"))

# Prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "you are a helpful assistant. Please respond to the user queries"),
        ("user", "Question: {question}"),
    ]
)


# Streamlit framework
st.title("Langchain with OpenAI")
input_text = st.text_input("User! give some Query...")

# OpenAI LLM
llm = ChatOpenAI(model='gpt-4o-mini')
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

if input_text:
    st.write(chain.invoke({'question': input_text}))

