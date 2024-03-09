import pandas as pd
import plotly.graph_objects as go
from datetime import timedelta
from arbitrage_analysis.config import BLD_data, BLD_figures


def plot_investment_growth(filtered_arbitrage_opp_path, investment_growth_path, btc_ticker_path):
    """
    Generates and saves a plot of investment growth over time based on filtered arbitrage opportunities and Bitcoin (BTC) yield averages.

    This function reads filtered arbitrage opportunities data and BTC yield averages from specified paths, then generates a time series plot. The x-axis represents dates of each bet, and the y-axis shows the cumulative value of the investment over time. Betting events are indicated with colored dots, and BTC yield averages are plotted for comparison.

    Args:
        filtered_arbitrage_opp_path (Path or str): Path to the pickle file with filtered arbitrage opportunities data.
        investment_growth_path (Path or str): File path where the generated plot image will be saved.
        btc_ticker_path (Path or str): Path to the pickle file with Bitcoin yield averages data.

    Returns:
        None: The plot is directly saved to the location specified by `investment_growth_path`.
    """
    # Load the filtered dataset
    df_filtered = pd.read_pickle(filtered_arbitrage_opp_path)
    ticker_averages = pd.read_pickle(btc_ticker_path)
    
    # Sort the DataFrame by commence_time to ensure chronological order
    df_filtered = df_filtered.sort_values(by='commence_time')

    # Plotting
    fig = go.Figure()

    # A predefined set of colors for the matches
    colors = [
        "#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A",
        "#19D3F3", "#FF6692", "#B6E880", "#FF97FF", "#FECB52"
    ]

    # Add traces for investment growth at each game
    for i, (index, row) in enumerate(df_filtered.iterrows()):
        if i == 0:
            # Calculate the starting investment assuming it grows from the initial investment
            initial_investment = row['investment_growth'] / (1 + (row['yield'] / 100))
            start_time = row['commence_time'] - timedelta(days=1)
            # Initial line
            fig.add_trace(go.Scatter(x=[start_time, row['commence_time']], y=[initial_investment, initial_investment], mode='lines', line=dict(color='blue'), showlegend=False))
            fig.add_trace(go.Scatter(x=[row['commence_time'], row['commence_time']], y=[initial_investment, row['investment_growth']], mode='lines', line=dict(color='blue'), showlegend=False))
        else:
            # Previous row data
            prev_row = df_filtered.iloc[i-1]
            # Horizontal line to current game
            fig.add_trace(go.Scatter(x=[prev_row['commence_time'], row['commence_time']], y=[prev_row['investment_growth'], prev_row['investment_growth']], mode='lines', line=dict(color='blue'), showlegend=False))
            # Vertical jump for current game
            fig.add_trace(go.Scatter(x=[row['commence_time'], row['commence_time']], y=[prev_row['investment_growth'], row['investment_growth']], mode='lines', line=dict(color='blue'), showlegend=False))
        
        # Dot for each match with unique color
        match_label = f"{row['home_team']} vs {row['away_team']}"
        fig.add_trace(go.Scatter(x=[row['commence_time']], y=[row['investment_growth']], mode='markers', marker=dict(color=colors[i % len(colors)], size=8), name=match_label))

    # Extend the final horizontal line beyond the last match
    end_time = df_filtered['commence_time'].max() + timedelta(days=1)
    final_investment = df_filtered.iloc[-1]['investment_growth']
    fig.add_trace(go.Scatter(x=[df_filtered.iloc[-1]['commence_time'], end_time], y=[final_investment, final_investment], mode='lines', line=dict(color='blue'), showlegend=False))

    # Plotting Ticker yield averages
    btc_dates = pd.date_range(start=df_filtered['commence_time'].min(), periods=len(ticker_averages))
    fig.add_trace(go.Scatter(x=btc_dates, y=ticker_averages['investment_growth_ticker'], mode='lines+markers', name='BTC Yield Average', line=dict(color='red')))

    # Update layout
    fig.update_layout(title='Investment Growth Over Time', xaxis_title='Date', yaxis_title='Investment Value ($)', xaxis=dict(type='date', showline=True, showticklabels=True, ticks='outside', linecolor='rgb(204, 204, 204)', linewidth=2, tickfont=dict(family='Arial', size=12, color='rgb(82, 82, 82)')), yaxis=dict(showline=True, showticklabels=True, ticks='outside', linecolor='rgb(204, 204, 204)', linewidth=2, tickfont=dict(family='Arial', size=12, color='rgb(82, 82, 82)')))

    fig.write_image(investment_growth_path)

depends_on_plot_investment = {
    "filtered_arbitrage_opp_path": BLD_data / "filtered_arbitrage_opportunities.pkl",
    "ticker_path": BLD_data / "benchmark_growth_path_BTC.pkl"
}

def task_plot_investment_growth(
    depends_on = depends_on_plot_investment,
    produces = BLD_figures / "investment_growth.png"
):
    plot_investment_growth(depends_on["filtered_arbitrage_opp_path"], produces, depends_on["ticker_path"])
