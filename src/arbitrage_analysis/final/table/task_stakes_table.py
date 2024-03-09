import pandas as pd
from arbitrage_analysis.config import BLD, BLD_data, BLD_tables

def _format_column_name(col_name):
    """
    Formats a column name by replacing underscores with spaces and capitalizing the first letter of each word.
    
    Parameters:
    - col_name (str): The original column name.
    
    Returns:
    - str: The formatted column name.
    """
    return ' '.join(word.capitalize() for word in col_name.split('_'))

def _display_stakes_in_latex(file_path, output_path):
    """
    Reads a DataFrame from a .pkl file, selects specific columns, renames them, and converts it to a LaTeX table.
    
    Parameters:
    - file_path (str): Path to the .pkl file containing the DataFrame.
    - output_path (str): Path where the LaTeX table will be saved.
    
    Returns:
    - None
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
    _display_stakes_in_latex(depends_on, produces)