import pandas as pd
from arbitrage_analysis.config import SRC, BLD_data

def extract_odds_rapid_api(src_file):
    """
    Reads and cleans odds data from a specified CSV file. This involves extracting key columns,
    renaming them for consistency, and removing any rows with missing values.

    Args:
        src_file (Path): Path to the source CSV file containing odds data.

    Returns:
        pandas.DataFrame: Cleaned DataFrame with odds data structured with columns
                          ['away_team', 'home_team', 'away', 'home', 'draw', 'bookie'].
    """
    # Read the source CSV file
    df = pd.read_csv(src_file)

    # Initialize an empty DataFrame with the desired column names
    final_df = pd.DataFrame(columns=['away_team', 'home_team', 'away', 'home', 'draw', 'bookie'])

    # Loop through each match's data, extracting and transforming relevant columns
    for i in range(167):
        # Define the column names to extract for this match
        columns_to_extract = [
            f'{i}.away_team', f'{i}.home_team', f'{i}.away', f'{i}.home', f'{i}.draw', f'{i}.bookie'
        ]

        # Check if the columns exist, then extract, rename, and concatenate them
        if all(column in df.columns for column in columns_to_extract):
            extracted_df = df[columns_to_extract].copy()
            extracted_df.columns = ['away_team', 'home_team', 'away', 'home', 'draw', 'bookie']
            final_df = pd.concat([final_df, extracted_df], ignore_index=True)
        else:
            break

    # Drop any rows containing NaN values to clean the dataset
    final_df.dropna(inplace=True)

    return final_df

create_odds_dataframe_depends_on = {
    "data": SRC / "data" / "df_odds_rapid_api.csv",
    "directory": BLD_data / ".dir_created"
}

def task_extract_odds_rapid_api(
        depends_on= create_odds_dataframe_depends_on,
        produces=BLD_data / "all_odds_rapid_api.pkl",
):
    # Extract the path to the source data file from task dependencies
    data_file = depends_on["data"]

    # Transform the source data into a cleaned DataFrame
    all_odds_df = extract_odds_rapid_api(data_file)
    
    # Save the transformed DataFrame to a pickle file
    all_odds_df.to_pickle(produces)
