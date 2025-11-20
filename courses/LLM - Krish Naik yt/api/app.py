from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from langserve import add_routes
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='../.env')

app = FastAPI(
    title="Langchain server",
    version='0.0.1',
    description='backend for a llm'
)


add_routes(
    app, ChatOpenAI(), path='/openai'
)

openai_model = ChatOpenAI(api_key=os.getenv('OPENAI_API_KEY'))
ollama_model = Ollama(model='gemma3')

prompt_for_openai_model = ChatPromptTemplate.from_template('Create an essay with {topic} as topic with 100 words')
prompt_for_ollama_model = ChatPromptTemplate.from_template('Create an poem with {topic} as topic with 100 words')

add_routes(app, prompt_for_openai_model | openai_model, path='/essay')

add_routes(app, prompt_for_ollama_model | ollama_model, path='/poem')

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=5001)