import os
from time import perf_counter
from typing import Literal

from deepagents import create_deep_agent
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from tavily import TavilyClient

load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """Run a web search"""
    return tavily_client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )


class WeatherReport(BaseModel):
    """A structured weather report with current conditions and forecast."""

    location: str = Field(description="The location for this weather report")
    temperature: float = Field(description="Current temperature in Celsius")
    condition: str = Field(
        description="Current weather condition (e.g., sunny, cloudy, rainy)"
    )
    humidity: int = Field(description="Humidity percentage")
    wind_speed: float = Field(description="Wind speed in km/h")
    forecast: str = Field(description="Brief forecast for the next 24 hours")


if __name__ == "__main__":
    model = ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))
    agent = create_deep_agent(
        model=model,
        response_format=WeatherReport,
        tools=[internet_search],
    )
    query = input("Enter location/prompt to ai to get weather details: ")

    start = perf_counter()
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": query,
                }
            ]
        }
    )

    print("Structured Result: ", result["structured_response"])
    print(f"Response time: {perf_counter() - start}")
