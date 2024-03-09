import pandas as pd
from arbitrage_analysis.config import BLD_data, BLD_tables

def _format_column_name(col_name):
    """
    Formats a given column name by making stylistic adjustments.

    This function takes a column name string, replaces underscores with spaces, and capitalizes the first letter of each word. The transformation makes column names more readable, especially when presenting data in user-friendly formats (e.g., reports, tables).

    Args:
        col_name (str): The original column name to be formatted.

    Returns:
        str: The formatted column name with spaces instead of underscores and each word capitalized.

    Example:
        Input: "best_odds_home"
        Output: "Best Odds Home"
    """
    return ' '.join(word.capitalize() for word in col_name.split('_'))

def display_stakes_in_latex(file_path, output_path):
    """
    Reads a DataFrame from a pickle file, selects and renames specific columns, then exports it as a LaTeX table.

    This function processes a DataFrame containing arbitrage stakes information by selecting relevant columns,
    formatting their names for readability, and finally converting the data into a LaTeX table format. The resultant
    table is saved to a specified file path.

    Args:
        file_path (str): Path to the pickle (.pkl) file containing the DataFrame with arbitrage opportunities.
        output_path (str): Destination path for the generated LaTeX table file.

    Returns:
        None: The LaTeX table is written to `output_path`, with no value returned.
    """
    # Load the DataFrame from .pkl file
    df = pd.read_pickle(file_path)
    
    # Select and rename columns
    selected_columns = [
        'home_team', 'away_team', 'best_odds_home', 'best_odds_draw', 'best_odds_away',
        'stake_home', 'stake_draw', 'stake_away', 'payout_home'
    ]
    df = df[selected_columns]
    
    # Rename 'payout_home' to 'Safe Payout' and format other column names
    df = df.rename(columns={col: _format_column_name(col) if col != 'payout_home' else 'Safe Payout' for col in df.columns})
    
    # Convert the DataFrame to a LaTeX table
    latex_table = df.to_latex(index=False, column_format='l' * len(df.columns))
    
    # Save the LaTeX table to the specified output path
    with open(output_path, 'w') as file:
        file.write(latex_table)

def task_display_stakes_in_latex(
    depends_on = BLD_data / "arbitrage_opportunities.pkl",
    produces = BLD_tables / "arbitrage_opportunities.tex"
):
    display_stakes_in_latex(depends_on, produces)