from pathlib import Path
from unittest.mock import Mock, patch
from requests import Response
import sys


parent = str(Path(__file__).resolve().parents[2]) + "/Week 1/Day 1/"
sys.path.append(parent)

import weather_api


@patch("weather_api.get")
def test_successful_weather_fetch(mock_get):
    """Test successful API call returns weather text"""
    mock_response = Mock(spec=Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "current": {"condition": {"text": "Partly cloudy"}}
    }
    mock_get.return_value = mock_response

    result = weather_api.get_current_weather_text_at("London")

    assert result == "Partly cloudy"
    mock_get.assert_called_once()
