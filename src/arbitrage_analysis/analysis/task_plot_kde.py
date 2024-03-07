from arbitrage_analysis.config import BLD_data, BLD_figures
import pandas as pd
import plotly.graph_objects as go
from plotly.colors import qualitative
from arbitrage_analysis.analysis.task_odds_kernel_density_estimate import kernel_density_estimation

def plot_kernel_density_estimate(all_odds_x, all_odds_y, df_arb_opp, produces):
    """
    Load arbitrage opportunities and all odds, calculate the kernel density estimation (KDE) for all odds,
    and plot the KDE along with arbitrage opportunities using Plotly.

    Parameters:
    - odds_file_path (str): Path to the pickle file containing all odds.
    - arbitrage_file_path (str): Path to the pickle file containing arbitrage opportunities.
    - bandwidth (float): The bandwidth for the KDE calculation. Defaults to 1.
    - gridsize (int): The number of points to generate for the KDE plot. Defaults to 1000.

    Returns:
    - Plotly figure object displaying the KDE of all odds combined with arbitrage opportunities highlighted.
    """

    # Initialize Plotly figure
    fig = go.Figure(layout=go.Layout(
        title='Kernel Density Estimation of all Odds and Odds with Arbitrage Opportunities',
        xaxis_title='Odds',
        yaxis_title='Density',
        margin=dict(l=20, r=20, t=40, b=120),
        legend=dict(orientation="h",
                    yanchor="bottom",
                    y=-0.3,
                    xanchor="center",
                    x=0.5),
        width=1000,
        height=600,
    ))

    fig.add_trace(go.Scatter(x=all_odds_x, y=all_odds_y, mode='lines', name='Kernel Density Estimate', line=dict(color='black')))

    # Generate a list of colors for the games
    num_games = len(df_arb_opp)
    colors = qualitative.Plotly[:num_games]

    # Plot arbitrage opportunities with unique colors but only one legend entry per game
    for i, row in df_arb_opp.iterrows():
        color = colors[i % len(colors)]
        game_label = f"{row['home_team']} vs {row['away_team']}"
        fig.add_trace(go.Scatter(x=[row['best_odds_home'], row['best_odds_draw'], row['best_odds_away']],
                                 y=[0, 0, 0],
                                 mode='markers',
                                 marker=dict(color=color, size=8),
                                 name=game_label,
                                 legendgroup=game_label,  # Group by game for a single legend entry
                                 showlegend=True))  # Show legend only for the first occurrence

    fig.write_image(produces, width=1000, height=800, scale=2)

depends_on_plot_kde = {
    "odds_kde": BLD_data / "odds_kde_with_arbitrage_opportunities.pkl",
    "arbitrage_opportunities": BLD_data / "arbitrage_opportunities.pkl"
} 

def task_plot_kde(
    depends_on = depends_on_plot_kde,
    produces = BLD_figures / 'kde_with_arbitrage_opportunities.png'
    ):
    all_odds_x, all_odds_y = pd.read_pickle(depends_on["odds_kde"])
    df_arb_opp = pd.read_pickle(depends_on["arbitrage_opportunities"])
    plot_kernel_density_estimate(all_odds_x, all_odds_y, df_arb_opp, produces)