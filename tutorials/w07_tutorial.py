""" CSC271H1 - Web API Tutorial """

import requests
import pandas as pd
from pprint import pprint

BASE_URL = "https://api.open-meteo.com/v1/forecast"
LAT_INDEX = 0
LONG_INDEX = 1

def get_current_weather(coords: list[float]) -> dict:
    """Return the current weather data as a dictionary fetched from BASE_URL
    for the location with the coordinates coords (latitude and longitude).
    """

    # According to the API docs the parameters latitude and longitude
    # must be passed (in WGS84). The helper constants LAT_INDEX and
    # LONG_INDEX can be used to extract them from the coords list.
    params = {
        'latitude': coords[LAT_INDEX],
        'longitude': coords[LONG_INDEX],
        'current_weather': True
    }

    response = requests.get(BASE_URL, params=params)
    
    return response.json()

def get_forecast(coords: list[float], n: int) -> dict | None:
    """Return the n-day forecast for location with coordinates coords
    as a dictionary fetched from BASE_URL. If n is not a valid number of
    days according, return None.
    """

    # forecast_days accepts integer values from 0 up to 16 (default 7).
    # The assignment implies we should treat anything outside 1..16 as invalid.
    # Note: 0 would return no forecast days so we consider it invalid as well.
    if isinstance(n, int) and 1 <= n <= 16:
        params = {
            'latitude': coords[LAT_INDEX],
            'longitude': coords[LONG_INDEX],
            'forecast_days': n,
            'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum',
        }

        response = requests.get(BASE_URL, params=params)
        
        return response.json()
    else:
        return None


def get_temperature(weather_data: dict) -> float:
    """Return the temperature in degrees celcius for the current
    weather in the dictionary of weather_data.
    """
    # the current weather block contains a key 'temperature' with the
    # value in °C. Extract it and return.
    try:
        return weather_data['current_weather']['temperature']
    except (KeyError, TypeError):
        raise ValueError("Invalid weather data provided")
    

def make_dataframe(forecast_data: dict) -> pd.DataFrame:
    """Return a DataFame with columns time, temperature_2m_max,
    temperature_2m_min and precipitation_sum populated with the data
    associated with key 'daily' in forecast_to_data.
    """

    # the forecast_data should have a 'daily' key containing
    # sub-lists.  pandas can directly construct a DataFrame from that dict.
    if 'daily' not in forecast_data or not isinstance(forecast_data['daily'], dict):
        raise ValueError("Invalid forecast data")

    df = pd.DataFrame(forecast_data['daily'])

    # ensure only requested columns are present
    cols = ['time', 'temperature_2m_max', 'temperature_2m_min', 'precipitation_sum']
    # some APIs may return extra columns, drop them if they exist
    df = df.loc[:, [c for c in cols if c in df.columns]]
    return df
    

if __name__ == "__main__":

    city_to_coords = {
        'Toronto': (43.7, -79.4),
        'London': (51.5, -0.12),
        'Tokyo': (35.68, 139.69),
        'New York': (40.71, -74.0),
        'Vancouver': (49.28, -123.12),
        'Montreal': (45.50, -73.57),
        'Milan': (45.46, 9.19)
    }

    # Sample calls to use for testing

    toronto_json = get_current_weather(city_to_coords['Toronto'])
    pprint(toronto_json)

    toronto_temp = get_temperature(toronto_json)
    print(f"current temp: {toronto_temp}")

    forecast_json = get_forecast(city_to_coords['Toronto'], 3)
    pprint(forecast_json)

    df = make_dataframe(forecast_json)
    print(df.head())
