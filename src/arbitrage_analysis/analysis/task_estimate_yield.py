import pandas as pd
from arbitrage_analysis.config import BLD_data, SRC

def calculate_and_filter_highest_yield(arbitrage_opportunity_path, filtered_arbitrage_path, initial_investment=100):
    """
    Calculates the yield from arbitrage opportunities and filters them to identify the highest yield for each unique commence time.
    It simulates reinvestment of payouts to calculate how the initial investment would grow over time based on the yields.

    Args:
        arbitrage_opportunity_path (Path): Path to the pickle file containing the DataFrame of arbitrage opportunities.
        filtered_arbitrage_path (Path): Path where the filtered DataFrame will be saved as a pickle file.
        initial_investment (float, optional): The amount of money to start investing with. Defaults to 100.

    Returns:
        None: This function does not return a value. Instead, it saves the filtered DataFrame with the highest yield opportunities and their investment growth to a pickle file.
    """
    # Load the dataset
    df = pd.read_pickle(arbitrage_opportunity_path)

    # Process data
    df['commence_time'] = pd.to_datetime(df['commence_time'])
    df['total_staked'] = df['stake_home'] + df['stake_draw'] + df['stake_away']
    df['total_payout'] = df['payout_home']  # Assuming all payouts are the same, we use one column
    df['profit'] = df['total_payout'] - df['total_staked']
    df['yield'] = (df['profit'] / df['total_staked']) * 100

    df_filtered = df.groupby('commence_time', group_keys=False).apply(_filter_highest_yield).reset_index(drop=True)
    
    # Initialize investment
    current_investment = initial_investment
    df_filtered['investment_growth'] = 0  # Initialize the column

    # Calculate compounded investment growth and append it to df_filtered
    for i, row in df_filtered.iterrows():
        current_investment *= 1 + (row['yield'] / 100)
        df_filtered.at[i, 'investment_growth'] = current_investment

    df_filtered.to_pickle(filtered_arbitrage_path)


def _filter_highest_yield(group):
    """
    Helper function to identify the opportunity with the highest yield within a group of arbitrage opportunities.

    Args:
        group (DataFrame): A subset of the arbitrage opportunities DataFrame, grouped by 'commence_time'.
    
    Returns:
        DataFrame: A single-row DataFrame corresponding to the opportunity with the highest yield in the group.
    """
    return group.loc[group['yield'].idxmax()]

def ticker_growth_path(ticker_yield_path, benchmark_growth_path, initial_investment=100):
    """
    Simulates the growth of an initial investment over time, based on the average daily yield changes recorded for a specific ticker.

    Args:
        ticker_yield_path (Path): Path to the pickle file containing a DataFrame with the average daily yield changes of a ticker.
        benchmark_growth_path (Path): Path where the resulting DataFrame showing the investment growth over time will be saved as a pickle file.
        initial_investment (float, optional): The amount of money to start investing with. Defaults to 100.
    
    Returns:
        None: This function does not return a value. Instead, it saves a DataFrame representing the investment growth over time to a pickle file.
    
    Note:
        The function assumes the DataFrame contains a column 'Average Daily Change' representing the daily yield changes.
    """
    # Load the dataset
    averages_df = pd.read_pickle(ticker_yield_path)

    # Initialize the growth path with the initial investment value
    growth_path = [initial_investment]

    # Start calculation from the first day
    for change in averages_df['Average Daily Change']:
        new_value = growth_path[-1] * (change)
        growth_path.append(new_value)

    # Shift the values one row higher
    growth_path.pop(0)

    # Convert the growth path to a DataFrame
    growth_path_df = pd.DataFrame(growth_path, columns=['investment_growth_ticker'])

    growth_path_df.to_pickle(benchmark_growth_path)


depends_on_estimate_yield = {
    "arbitrage_opportunity": BLD_data / "arbitrage_opportunities.pkl",
    "ticker_yield_averages":   BLD_data / "yield_averages_BTC.pkl"
}

produces_estimate_yield = {
    "filtered_arbitrage_opportunity": BLD_data / "filtered_arbitrage_opportunities.pkl",
    "average_growth_BTC":   BLD_data / "benchmark_growth_path_BTC.pkl"
}

def task_estimate_yield(
    depends_on = depends_on_estimate_yield,
    produces = produces_estimate_yield
):
    calculate_and_filter_highest_yield(depends_on["arbitrage_opportunity"], produces["filtered_arbitrage_opportunity"], initial_investment=100)
    ticker_growth_path(depends_on["ticker_yield_averages"], produces["average_growth_BTC"], initial_investment=100)