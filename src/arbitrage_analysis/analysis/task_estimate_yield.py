import pandas as pd
from arbitrage_analysis.config import BLD_data, SRC


def calculate_and_filter_highest_yield(arbitrage_opportunity_path, initial_investment=100):
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

    return df_filtered

def task_estimate_yield(
    depends_on = BLD_data / "arbitrage_opportunities.pkl",
    produces = BLD_data / "filtered_arbitrage_opportunities.pkl"
):
    df_filtered = calculate_and_filter_highest_yield(depends_on, initial_investment=100)
    df_filtered.to_pickle(produces)