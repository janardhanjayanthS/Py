from pathlib import Path
import sys


parent = str(Path(__file__).resolve().parents[2]) + '/Week 1/Day 1/'
sys.path.append(parent)

from weather_api import get_current_weather_text_at


get_current_weather_text_at('Chennai')