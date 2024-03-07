import pandas as pd
from arbitrage_analysis.config import BLD_data

def investment_growth_path(initial_investment, averages_df):
    """
    Calculate the growth path of an initial investment based on average daily changes.

    Parameters:
    - initial_investment (float): The amount of the initial investment.
    - averages_df (pandas.DataFrame): A DataFrame containing the average daily change for each day within 15-day intervals.

    Returns:
    - pandas.DataFrame: A DataFrame containing the value of the investment for each day across the 15-day intervals.
    """
    # Initialize the growth path list with the initial investment
    growth_path = [initial_investment]

    # Calculate the investment value for each day
    for change in averages_df['Average Daily Change']:
        # Update the investment value based on the daily change
        new_value = growth_path[-1] * (change)
        growth_path.append(new_value)

    # Convert the growth path to a DataFrame
    growth_path_df = pd.DataFrame(growth_path, columns=['Investment Value'])

    return growth_path_df

# Example usage
initial_investment = 100  # Starting with an investment of $100
averages_df = pd.read_pickle(BLD_data / "yield_averages_BTC.pkl")
growth_path_df = investment_growth_path(initial_investment, averages_df)
print(growth_path_df)