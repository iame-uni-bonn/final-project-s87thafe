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
    Fetches the list of sports from The Odds API.
    
    Parameters:
        apiKey (str): The API key for authenticating requests to The Odds API.
        
    Returns:
        dict: A JSON response containing the list of sports if the request is successful.
        str: An error message indicating the HTTP status code if the request fails.
    """
    url = f"https://api.the-odds-api.com/v4/sports/?apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # Returns the JSON response from the API
    else:
        return f"Error fetching data: {response.status_code}"

def get_odds_the_odds_api(sport, api_key, regions, markets):
    """
    Fetches odds for a specific sport from The Odds API based on the specified regions and markets.
    
    Parameters:
        sport (str): The sport to fetch odds for.
        apiKey (str): The API key for authenticating requests to The Odds API.
        regions (str): Comma-separated string of region codes to fetch odds for.
        markets (str): Comma-separated string of market types to fetch odds for.
        
    Returns:
        dict: A JSON response containing the odds if the request is successful.
        str: An error message indicating the HTTP status code if the request fails.
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
