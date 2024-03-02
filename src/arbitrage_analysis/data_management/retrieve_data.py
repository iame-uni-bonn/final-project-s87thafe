import requests
import pandas as pd
from arbitrage_analysis.config import THE_ODDS_API_API_KEY

apiKey = THE_ODDS_API_API_KEY
# Example usage
sport = "soccer_epl"
regions = "eu" 
markets = "h2h"

def get_sports_the_odds_api(apiKey):
    """
    Fetches the list of sports from The Odds API.
    
    Parameters:
        apiKey (str): The API key for authenticating requests to The Odds API.
        
    Returns:
        dict: A JSON response containing the list of sports if the request is successful.
        str: An error message indicating the HTTP status code if the request fails.
    """
    url = f"https://api.the-odds-api.com/v4/sports/?apiKey={apiKey}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # Returns the JSON response from the API
    else:
        return f"Error fetching data: {response.status_code}"

def get_odds_the_odds_api(sport, apiKey, regions, markets):
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
        "apiKey": apiKey,
        "regions": regions,
        "markets": markets,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()  # Returns the JSON response from the API
    else:
        return f"Error fetching data: {response.status_code}"

# Fetch and save sports to CSV
sports = get_sports_the_odds_api(apiKey)
df_sports = pd.json_normalize(sports)
df_sports.to_csv("df_sports.csv", index=False)

# Fetch odds data, print and save to CSV
odds_data = get_odds_the_odds_api(sport, apiKey, regions, markets)
# Assuming you want to save `odds_data` to CSV, ensure it's in DataFrame form
df_odds = pd.json_normalize(odds_data)
df_odds.to_csv("df_odds.csv", index=False)
