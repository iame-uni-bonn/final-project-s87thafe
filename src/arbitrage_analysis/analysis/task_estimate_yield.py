import pandas as pd
from arbitrage_analysis.config import BLD_data, SRC

def calculate_and_filter_highest_yield(arbitrage_opportunity_path, initial_investment=100, filtered_arbitrage_path = BLD_data / "filtered_arbitrage_opportunities.pkl"):
    """
    Calculates the yield for betting opportunities and filters out those with the highest yield per commence time.
    Additionally, calculates and appends the investment growth over time assuming reinvestment of payouts.

    Parameters:
    betting_data_path (Path or str): The path to the pickled DataFrame containing betting opportunities.
    initial_investment (float): The initial amount to be invested.

    Returns:
    DataFrame: A DataFrame containing filtered betting opportunities with the highest yield per commence time,
                including the reinvestment growth calculation.
    """
    # Load the dataset
    df = pd.read_pickle(arbitrage_opportunity_path)

    # Process data
    df['commence_time'] = pd.to_datetime(df['commence_time'])
    df['total_staked'] = df['stake_home'] + df['stake_draw'] + df['stake_away']
    df['total_payout'] = df['payout_home']  # Assuming all payouts are the same, we use one column
    df['profit'] = df['total_payout'] - df['total_staked']
    df['yield'] = (df['profit'] / df['total_staked']) * 100

    # Filter out the entry with the highest yield for each commence time
    def filter_highest_yield(group):
        return group.loc[group['yield'].idxmax()]

    df_filtered = df.groupby('commence_time', group_keys=False).apply(filter_highest_yield).reset_index(drop=True)
    
    # Initialize investment
    current_investment = initial_investment
    df_filtered['investment_growth'] = 0  # Initialize the column

    # Calculate compounded investment growth and append it to df_filtered
    for i, row in df_filtered.iterrows():
        current_investment *= 1 + (row['yield'] / 100)
        df_filtered.at[i, 'investment_growth'] = current_investment

    df_filtered.to_pickle(filtered_arbitrage_path)


def ticker_growth_path(ticker_yield_path, initial_investment, benchmark_growth_path):
    """
    Calculate the growth path of an initial investment based on average daily changes.

    Parameters:
    - initial_investment (float): The amount of the initial investment.
    - ticker_yield_path (str): Path to the pickled DataFrame containing the average daily changes.

    Returns:
    - pandas.DataFrame: A DataFrame showing the investment value across the 15-day intervals.
    """
    # Load the dataset
    averages_df = pd.read_pickle(ticker_yield_path)

    # Initialize the growth path with the initial investment value
    growth_path = [initial_investment]

    # Adjust the first entry calculation if needed here
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
    calculate_and_filter_highest_yield(depends_on["arbitrage_opportunity"], initial_investment=100, filtered_arbitrage_path=produces["filtered_arbitrage_opportunity"])
    ticker_growth_path(depends_on["ticker_yield_averages"], initial_investment=100, benchmark_growth_path=produces["average_growth_BTC"])