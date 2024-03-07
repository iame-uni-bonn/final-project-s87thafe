import pandas as pd
from arbitrage_analysis.config import SRC, BLD_data

def standardize_team_names_and_merge(df_the_odds_api_path, df_rapid_api_path, output_path):
    """
    Standardizes team names in two DataFrames and merges them into a single DataFrame.

    Parameters:
    - df_the_odds_api_path (Path): Path to the "The Odds API" DataFrame pickle file.
    - df_rapid_api_path (Path): Path to the "Rapid API" DataFrame pickle file.
    - output_path (Path): Path where the merged DataFrame will be saved as a .pkl.

    The function reads two DataFrames from pickle files, standardizes team names using
    a predefined mapping, renames columns for consistency, merges them, and saves
    the result as a Pickle file.
    """
    # Load the DataFrames
    df_the_odds_api = pd.read_pickle(df_the_odds_api_path)
    df_rapid_api = pd.read_pickle(df_rapid_api_path)

    # Define the mapping of team names
    team_name_mapping = {
        'Ssc Napoli': 'Napoli', 'Inter Milano': 'Inter Milan', 'Cagliari ': 'Cagliari',
        'Us Sassuolo ': 'Sassuolo', 'Genoa Cfc': 'Genoa', 'Us Lecce': 'Lecce',
        'Ac Milan': 'AC Milan', 'Juventus Turin': 'Juventus', 'Acf Fiorentina': 'Fiorentina',
        'Fc Torino': 'Torino', 'Sportiva Salernitana': 'Salernitana', 'Frosinone ': 'Frosinone',
        'Ac Monza': 'Monza', 'Hellas Verona Fc': 'Hellas Verona FC', 'Fc Empoli': 'Empoli',
        'Atalanta Bergamasca ': 'Atalanta BC', 'As Roma': 'AS Roma'
    }

    # Standardize team names in df_rapid_api using the mapping
    df_rapid_api['home_team'] = df_rapid_api['home_team'].map(team_name_mapping).fillna(df_rapid_api['home_team'])
    df_rapid_api['away_team'] = df_rapid_api['away_team'].map(team_name_mapping).fillna(df_rapid_api['away_team'])

    # Rename columns in df_rapid_api for consistency
    df_rapid_api.rename(columns={'away': 'away_win_odds', 'home': 'home_win_odds', 'draw': 'draw_odds', 'bookie': 'bookmaker'}, inplace=True)

    # Merge the DataFrames
    df_merged = pd.concat([df_the_odds_api, df_rapid_api], ignore_index=True)

    # Extract unique pairs of home_team, away_team, and their commence_time from df_the_odds_api
    commence_time_mapping = df_the_odds_api[['home_team', 'away_team', 'commence_time']].drop_duplicates()

    # Left merge to fill in commence_time for matches in df_rapid_api based on matches in df_the_odds_api
    df_merged_updated = pd.merge(df_merged, commence_time_mapping, on=['home_team', 'away_team'], how='left', suffixes=('', '_from_api'))

    # Resolve any commence_time conflicts (if both columns have values, prefer the original commence_time)
    df_merged_updated['commence_time'] = df_merged_updated['commence_time'].fillna(df_merged_updated['commence_time_from_api'])

    # Drop the temporary column used for merging
    df_merged_updated.drop(columns=['commence_time_from_api'], inplace=True)

    # Sort and save the merged DataFrame
    df_merged_sorted = df_merged_updated.sort_values(by=['home_team', 'away_team'])
    df_merged_sorted.to_pickle(output_path)

standardize_and_merge_depends_on = {
    "df_the_odds_api_path": BLD_data / "all_odds_the_odds_api.pkl",
    "df_rapid_api_path": BLD_data / "all_odds_rapid_api.pkl"
}

def task_standardize_and_merge(
        depends_on= standardize_and_merge_depends_on,
        produces= BLD_data / "all_odds_merged.pkl"
        ):
    standardize_team_names_and_merge(depends_on["df_the_odds_api_path"], depends_on["df_rapid_api_path"], produces)
