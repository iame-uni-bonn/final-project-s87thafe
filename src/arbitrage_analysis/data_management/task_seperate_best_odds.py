import pandas as pd
from arbitrage_analysis.config import SRC, BLD_data, BLD_figures

def find_best_odds(df_path) -> pd.DataFrame:
    """
    Loads betting odds data and identifies the best odds for home wins, draws, and away wins for each match, along with the corresponding bookmakers.

    Args:
        df_path (Path): The path to the pickle file containing the dataset with merged odds from various bookmakers.

    Returns:
        pd.DataFrame: A DataFrame with columns for home team, away team, commence time, best odds for home win, draw, and away win, and the bookmakers offering these odds.
    """
    # Load the merged odds data
    df = pd.read_pickle(df_path)

    # Initialize a list to store data for each match
    data_to_append = []

    # Iterate over each match to find the best odds and corresponding bookmakers
    for (home_team, away_team), group in df.groupby(['home_team', 'away_team']):
        best_home = group.loc[group['home_win_odds'].idxmax()]
        best_draw = group.loc[group['draw_odds'].idxmax()]
        best_away = group.loc[group['away_win_odds'].idxmax()]
        commence_time = group['commence_time'].iloc[0]
        
        # Append information for each match
        data_to_append.append({
            'home_team': home_team,
            'away_team': away_team,
            'commence_time': commence_time,
            'best_odds_home': best_home['home_win_odds'],
            'best_odds_draw': best_draw['draw_odds'],
            'best_odds_away': best_away['away_win_odds'],
            'bookie_home': best_home['bookmaker'],
            'bookie_draw': best_draw['bookmaker'],
            'bookie_away': best_away['bookmaker']
        })

    # Convert the list of data into a DataFrame
    return pd.DataFrame(data_to_append)


def task_find_best_odds(
        depends_on = BLD_data / "all_odds_merged.pkl",
        produces = BLD_data / "best_odds_info.pkl"
    ):
    best_odds_info = find_best_odds(depends_on)
    best_odds_info.to_pickle(produces)
