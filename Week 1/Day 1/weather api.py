from requests import get, Response
from typing import Any
import os
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY: str | None = os.getenv('weather_api_key')
WEATHER_API_HEADER: str = 'http://api.weatherapi.com/v1/current.json'



def get_current_weather_text_at(place: str) -> None:
    """
    Prints weather text for a certain location
    Args:
        place: location at which we get weather report
    """
    response: Response = get(WEATHER_API_HEADER, params=parameters)
    if response.status_code == 200:
        print(f"Current weather at {place} {response.json()['current']['condition']['text']}")
    else:
        print(f'invalid status code: {response.status_code}')



if __name__ == '__main__':
    place: str = input('Enter an example location to check weather: ').title() 
    parameters: dict[str, Any] = {
        'key': WEATHER_API_KEY,
        'q': place,
        'aqi': 'no'
    }
    get_current_weather_text_at(place)