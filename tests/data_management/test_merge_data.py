import pandas as pd
from arbitrage_analysis.config import BLD_data
from arbitrage_analysis.data_management.task_merge_data import standardize_team_names_and_merge

def test_standardize_team_names_and_merge(tmp_path):
    # Create mock DataFrames
    df_the_odds_api = pd.DataFrame({
        'bookmaker': ['888sport', 'Pinnacle'],
        'home_team': ['Napoli', 'Inter Milan'],
        'away_team': ['Juventus', 'Genoa'],
        'commence_time': ['2024-03-03T19:45:50Z', '2024-03-04T19:45:50Z'],
        'home_win_odds': [2.30, 1.25],
        'draw_odds': [2.60, 6.25],
        'away_win_odds': [3.60, 11.0]
    })
    df_rapid_api = pd.DataFrame({
        'away_team': ['Juventus Turin', 'Genoa Cfc'],
        'home_team': ['Ssc Napoli', 'Inter Milano'],
        'away': [3.2, 11.0],
        'home': [2.35, 1.25],
        'draw': [2.75, 6.25],
        'bookie': ['admiralbet', 'interwetten']
    })

    # Define paths for mock input/output
    df_the_odds_api_path = tmp_path / "df_the_odds_api.pkl"
    df_rapid_api_path = tmp_path / "df_rapid_api.pkl"
    output_path = tmp_path / "merged.pkl"

    # Save mock DataFrames as pickle files
    df_the_odds_api.to_pickle(df_the_odds_api_path)
    df_rapid_api.to_pickle(df_rapid_api_path)

    # Call the function under test
    standardize_team_names_and_merge(df_the_odds_api_path, df_rapid_api_path, output_path)

    # Load the output DataFrame
    merged_df = pd.read_pickle(output_path)

    # Asserts
    assert len(merged_df) == len(df_the_odds_api) + len(df_rapid_api), "Merged DataFrame should contain all rows from both inputs"
    assert all(column in merged_df.columns for column in df_the_odds_api.columns), "Merged DataFrame should contain all columns"
    assert merged_df['home_team'].isin(['Napoli', 'Inter Milan']).all(), "Team names should be standardized"

