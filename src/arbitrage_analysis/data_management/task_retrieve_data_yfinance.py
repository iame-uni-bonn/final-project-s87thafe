import yfinance as yf
import numpy as np
import pandas as pd
from arbitrage_analysis.config import BLD_data

def calculate_average_returns(ticker, yield_average_path):
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