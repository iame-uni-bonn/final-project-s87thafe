from arbitrage_analysis.config import BLD_data, BLD_figures
import pandas as pd
import plotly.graph_objects as go
from plotly.colors import qualitative

def plot_kernel_density_estimate(all_odds_x, all_odds_y, df_arb_opp, produces):
    """
    Plots the kernel density estimation (KDE) for betting odds and highlights arbitrage opportunities.

    This function generates a Plotly figure illustrating the distribution of betting odds with a KDE curve.
    It also marks certain odds indicating arbitrage opportunities using different colors.

    Args:
        all_odds_x (Iterable[float]): Odds values for KDE calculation, representing different betting odds.
        all_odds_y (Iterable[float]): Computed density values for the KDE plot, corresponding to `all_odds_x`.
        df_arb_opp (pandas.DataFrame): Information on arbitrage opportunities. Required columns: 'home_team', 'away_team',
            'best_odds_home', 'best_odds_draw', 'best_odds_away'.
        produces (str): File path or name for saving the generated plot image.

    Returns:
        None: A Plotly figure is created and saved as an image at the specified `produces` path.
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
                                 legendgroup=game_label,
                                 showlegend=True))

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