import requests
import pandas as pd
import os
from arbitrage_analysis.config import SRC
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Access environment variables
the_odds_api_key = os.getenv('THEODDSAPI_API_KEY')

def get_sports_the_odds_api(api_key):
    """
    Fetches the list of available sports from The Odds API.

    Args:
        api_key (str): The API key for authenticating requests to The Odds API.

    Returns:
        dict: A JSON response with the list of sports, if the request is successful.
        str: An error message with the HTTP status code, if the request fails.
    """
    url = f"https://api.the-odds-api.com/v4/sports/?apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # Returns the JSON response from the API
    else:
        return f"Error fetching data: {response.status_code}"

def get_odds_the_odds_api(sport, api_key, regions, markets):
    """
    Fetches odds for a specified sport from The Odds API, filtered by regions and markets.

    Args:
        sport (str): The sport to fetch odds for.
        api_key (str): The API key for authenticating requests to The Odds API.
        regions (str): Comma-separated string of region codes for which to fetch odds.
        markets (str): Comma-separated string of market types for which to fetch odds.

    Returns:
        dict: A JSON response with the odds, if the request is successful.
        str: An error message with the HTTP status code, if the request fails.
    """
    url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds/"
    params = {
        "apiKey": api_key,
        "regions": regions,
        "markets": markets,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()  # Returns the JSON response from the API
    else:
        return f"Error fetching data: {response.status_code}"

# As the retrival depends on API keys and the data changes frequently, this code should not run via pytask.
if __name__ == "__main__":
    # Fetch and save sports to CSV
    sports = get_sports_the_odds_api(the_odds_api_key)
    df_sports = pd.json_normalize(sports)
    df_sports.to_csv(SRC / "data" / "df_sports_the_odds_api.csv", index=False)

    # Define parameters for the API request
    sport = "soccer_italy_serie_a"
    regions = "eu"
    markets = "h2h"

    # Fetch odds data, print and save to CSV
    odds_data = get_odds_the_odds_api(sport, the_odds_api_key, regions, markets)
    df_odds = pd.json_normalize(odds_data)
    df_odds.to_csv(SRC / "data" / "df_odds_the_odds_api.csv", index=False)

