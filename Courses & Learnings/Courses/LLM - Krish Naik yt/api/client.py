import streamlit as st
import requests


def get_opneai_response(topic: str) -> str:
    response = requests.post(
        "http://localhost:5001/essay/invoke", json={"input": {"topic": topic}}
    )
    return response.json()["output"]["content"]


def get_ollama_response(topic: str) -> str:
    response = requests.post(
        "http://localhost:5001/poem/invoke", json={"input": {"topic": topic}}
    )
    return response.json()["output"]



st.title("LLM poet/essayist")
essay_topic = st.text_input("Enter topic to write an essay")
poem_topic = st.text_input("Enter topic to write a poem")

if essay_topic:
    st.write(get_opneai_response(topic=essay_topic))
if poem_topic:
    st.write(get_ollama_response(topic=poem_topic))
