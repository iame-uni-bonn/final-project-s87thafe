import yfinance as yf
import numpy as np
import pandas as pd
from arbitrage_analysis.config import BLD_data

def calculate_average_returns(ticker, yield_average_path):
    """
    Fetches historical closing prices for a given ticker symbol over the last year from Yahoo Finance,
    calculates daily returns, and then computes the average return for each day across all 15-day intervals
    within the year. The averages are saved to a specified path.

    Args:
        ticker (str): The ticker symbol for the stock or asset to fetch historical data for.
        yield_average_path (Path): The path where the DataFrame containing the average daily changes
                                          will be saved as a pickle file.

    Returns:
        None: This function does not have a return value. It saves the calculated averages to a file specified by
              `yield_average_path`.
    """
    # Fetch data for the given ticker over the last year
    data = yf.download(ticker, period="1y")

    # Calculate daily returns
    data['Returns'] = data['Close'].pct_change() + 1

    # Create an array to hold the average results
    averages = []

    # Calculate the number of 15-day intervals in the data
    interval_count = len(data) // 15

    # Iterate over each day in the 15-day interval
    for day in range(15):
        # Calculate the average of this day across all intervals
        day_avg = np.mean([data['Returns'].iloc[i * 15 + day] for i in range(interval_count) if i * 15 + day < len(data)])
        averages.append(day_avg)

    # Convert the averages to a DataFrame for easier handling
    averages_df = pd.DataFrame(averages, columns=['Average Daily Change'])
    averages_df = averages_df.fillna(1)

    averages_df.to_pickle(yield_average_path)


def task_calculate_intervals_average(
    depends_on = BLD_data / ".dir_created",
    produces = BLD_data / "yield_averages_BTC.pkl"
):
    ticker = 'BTC-USD'
    calculate_average_returns(ticker, produces)