import pandas as pd
import json
from arbitrage_analysis.config import BLD_data, SRC


def extract_odds_the_odds_api(bookmakers_json, home_team, away_team):
    """
    Creates a DataFrame containing the odds offered by bookmakers for a given game between a home team and an away team.
    
    Parameters:
    - bookmakers_json (str): A JSON string containing the bookmakers' odds data.
    - home_team (str): The name of the home team.
    - away_team (str): The name of the away team.
    
    The function parses the JSON data to extract the odds for the home win, draw, and away win offered by each bookmaker.
    
    Returns:
    - pandas.DataFrame: A DataFrame where each row represents the odds from a different bookmaker, including columns for
      the bookmaker's name, the home team, the away team, odds for home win, draw, and away win.
    """
    bookmakers_data = json.loads(bookmakers_json.replace("'", "\""))
    bookmakers_odds = []

    for bookmaker in bookmakers_data:
        bookmaker_odds = {
            'bookmaker': bookmaker['title'],
            'home_team': home_team,  # Add home team name
            'away_team': away_team,  # Add away team name
            'home_win_odds': None,
            'draw_odds': None,
            'away_win_odds': None
        }
        for market in bookmaker['markets']:
            if market['key'] == 'h2h':
                for outcome in market['outcomes']:
                    if outcome['name'] == home_team:
                        bookmaker_odds['home_win_odds'] = outcome['price']
                    elif outcome['name'] == away_team:
                        bookmaker_odds['away_win_odds'] = outcome['price']
                    elif outcome['name'] == 'Draw':
                        bookmaker_odds['draw_odds'] = outcome['price']
        bookmakers_odds.append(bookmaker_odds)

    return pd.DataFrame(bookmakers_odds)

create_odds_dataframe_depends_on = {
    "data": SRC / "data" / "df_odds_the_odds_api.csv",
    "directory": BLD_data / ".dir_created"
}

def task_extract_odds_the_odds_api(
        depends_on= create_odds_dataframe_depends_on,
        produces=BLD_data / "df_all_games_odds.pkl",
):
    # Load the dataset containing the odds data
    df_odds = pd.read_csv(depends_on["data"])
    # Initialize an empty list to store each game's DataFrame
    all_games_odds = []

    # Iterate over each game in the dataset
    for index, row in df_odds.iterrows():
        game_odds_df = extract_odds_the_odds_api(row['bookmakers'], row['home_team'], row['away_team'])
        all_games_odds.append(game_odds_df)

    # Concatenate all individual DataFrames into a single DataFrame
    df_all_games_odds = pd.concat(all_games_odds, ignore_index=True)
    # Display the combined DataFrame
    df_all_games_odds.to_pickle(produces, index=False)
