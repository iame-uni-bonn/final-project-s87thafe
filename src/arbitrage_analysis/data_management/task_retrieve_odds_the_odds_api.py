import pandas as pd
import json
from arbitrage_analysis.config import BLD_data, SRC

def extract_odds_the_odds_api(bookmakers_json, home_team, away_team, commence_time):
    """
    Extends functionality to include the commencement time of the game.
    
    Parameters:
    - bookmakers_json (str): A JSON string containing the bookmakers' odds data.
    - home_team (str): The name of the home team.
    - away_team (str): The name of the away team.
    - commence_time (str): The start time of the game.
    
    Returns:
    - pandas.DataFrame: A DataFrame including odds from different bookmakers and the commence time.
    """
    bookmakers_data = json.loads(bookmakers_json.replace("'", "\""))
    bookmakers_odds = []

    for bookmaker in bookmakers_data:
        bookmaker_odds = {
            'bookmaker': bookmaker['title'],
            'home_team': home_team,
            'away_team': away_team,
            'commence_time': commence_time,  # Add commence time
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
        depends_on=create_odds_dataframe_depends_on,
        produces=BLD_data / "all_odds_the_odds_api.pkl"
        ):
    df_odds = pd.read_csv(depends_on["data"])
    all_games_odds = []

    for index, row in df_odds.iterrows():
        # Include commence_time in the function call
        game_odds_df = extract_odds_the_odds_api(row['bookmakers'], row['home_team'], row['away_team'], row['commence_time'])
        all_games_odds.append(game_odds_df)

    df_all_games_odds = pd.concat(all_games_odds, ignore_index=True)
    df_all_games_odds.to_pickle(produces)
