import requests
import pandas as pd
import os
from arbitrage_analysis.config import SRC
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Access environment variables for RapidAPI
rapid_api_key = os.getenv('RAPIDAPI_API_KEY')

def get_matches_rapid_api(sport, country, competition, api_key):
    """
    Fetches matches for a specific sport, country, and competition from the RapidAPI.
    
    Parameters:
        sport (str): The sport to fetch matches for.
        country (str): The country to fetch matches for.
        competition (str): The competition to fetch matches for.
        match_urls (bool, optional): Whether to include match URLs in the response. Defaults to False.
        
    Returns:
        dict: A JSON response containing the matches if the request is successful.
        str: An error message indicating the HTTP status code if the request fails.
    """
    url = "https://odds-api1.p.rapidapi.com/matches"
    querystring = {
        "sport": sport,
        "country": country,
        "competition": competition,
        "match_urls": "false"
    }
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "odds-api1.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        return response.json()  # Returns the JSON response from the API
    else:
        return f"Error fetching data: {response.status_code}"

def extract_matchid_bookie_pairs(csv_path):
    """
    Extracts match IDs and their corresponding bookmakers from a CSV file, creating a list of dictionaries
    with each dictionary containing a 'match_id' and its 'bookies'.

    Parameters:
        csv_path (str): The path to the CSV file containing match and bookmaker data.

    Returns:
        list: A list of dictionaries, where each dictionary includes:
            - 'match_id' (str): The match ID.
            - 'bookies' (str): The comma-separated string of bookmakers for that match.
    """
    # Load the CSV file
    df_matches = pd.read_csv(csv_path)
    
    # Initialize a list to hold dictionaries of matchid and corresponding bookies
    matchid_bookie_pairs = []

    # Extract matchids and corresponding bookies
    for i in range(15):  # Assuming the first 15 matches are of interest
        matchid_column = f"{i}.matchid"
        bookie_column = f"{i}.bookie"
        
        # Extract matchid and corresponding bookies
        matchid = df_matches[matchid_column].values[0]
        bookies = df_matches[bookie_column].values[0]  # Assuming bookies are stored as a comma-separated string
        
        # Append the dictionary to the list
        matchid_bookie_pairs.append({"match_id": matchid, "bookies": bookies})

    return matchid_bookie_pairs

def get_odds_for_matchid_bookie_pairs(matchid_bookie_pairs, api_key):
    """
    Fetches odds for each match ID and its corresponding bookmakers using RapidAPI.

    Parameters:
        matchid_bookie_pairs (list of dicts): List of dictionaries, each containing a match ID and its bookies.
        api_key (str): API key for authenticating requests to RapidAPI.

    Returns:
        pandas.DataFrame: A DataFrame containing odds for the specified matches and bookmakers.
    """
    all_odds = []  # List to store odds data for all matches
    
    for pair in matchid_bookie_pairs:
        matchid = pair["match_id"]
        bookies = pair["bookies"]
        
        url = "https://odds-api1.p.rapidapi.com/odds"
        querystring = {
            "matchid": matchid,
            "bookmakers": bookies
        }
        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "odds-api1.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code == 200:
            odds_data = response.json()            
            all_odds.append(odds_data)

        else:
            print(f"Error fetching data for match {matchid} with bookies {bookies}: {response.status_code}")
    
    # Convert the collected odds data into a DataFrame
    df_odds = pd.json_normalize(all_odds)
     
    return df_odds

# Serie A matches
sport = "soccer"
country = "italy"
competition = "serie-a"

# Fetch matches data
matches_data = get_matches_rapid_api(sport, country, competition, rapid_api_key)
df_matches = pd.json_normalize(matches_data)
df_matches.to_csv(SRC / "data" / "df_matches_rapid_api.csv", index=False)

# Define the path to the CSV file
csv_path = SRC / "data" / "df_matches_rapid_api.csv"
# Extract matchids and bookies
matchid_bookie_pairs = extract_matchid_bookie_pairs(csv_path)

#Fetch odds data
df_odds = get_odds_for_matchid_bookie_pairs(matchid_bookie_pairs, rapid_api_key)
df_odds.to_csv(SRC / "data" / "df_odds_rapid_api.csv", index=False)