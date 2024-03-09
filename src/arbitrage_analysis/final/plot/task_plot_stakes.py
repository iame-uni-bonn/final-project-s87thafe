import plotly.graph_objects as go
import pandas as pd
from arbitrage_analysis.config import BLD_data, BLD_figures

def plot_arbitrage_opportunities(data_path, fig_path):
    """
    Generates and saves a plot of arbitrage opportunities, showcasing stakes and potential payouts per game.

    This function visualizes the stakes placed on different outcomes (home win, draw, away win) and the
    potential payout for each game. It also includes a line indicating the total investment across all games.
    The resulting plot is saved to a specified location.

    Args:
        data_path (Path): Path to a pickle file containing arbitrage opportunities. This file
            should contain a DataFrame with columns specifying stakes and potential payouts.
        fig_path (Path): Path where the generated plot figure will be saved.

    Returns:
        None: The plot is directly saved to the location specified by `fig_path`.

    """
    arb_opportunities = pd.read_pickle(data_path)
    fig = go.Figure()
    bar_width = 0.2
    offset = 0.2
    total_investment = 100

    for i, row in enumerate(arb_opportunities.itertuples(index=False)):
        match_index = i
        potential_payout = max(row.stake_home * row.best_odds_home, 
                               row.stake_draw * row.best_odds_draw, 
                               row.stake_away * row.best_odds_away)

        # Adding traces for stakes and potential payout
        fig.add_trace(go.Bar(name='Home Win Stake', x=[match_index - offset], y=[row.stake_home], marker_color='lightblue', width=bar_width, showlegend=(i == 0)))
        fig.add_trace(go.Bar(name='Draw Stake', x=[match_index], y=[row.stake_draw], marker_color='lightgreen', width=bar_width, showlegend=(i == 0)))
        fig.add_trace(go.Bar(name='Away Win Stake', x=[match_index + offset], y=[row.stake_away], marker_color='coral', width=bar_width, showlegend=(i == 0)))
        fig.add_trace(go.Bar(name='Potential Payout', x=[match_index + 2 * offset], y=[potential_payout], marker_color='gold', width=bar_width, showlegend=(i == 0)))
    
    # Add total investment line
    fig.add_shape(type='line', x0=-0.5, y0=total_investment, x1=len(arb_opportunities) - 0.5, y1=total_investment, line=dict(color='red', width=3))

    # Update layout
    fig.update_layout(title='Arbitrage Opportunities: Stakes and Payout per Game',
                      xaxis=dict(tickmode='array', tickvals=list(range(len(arb_opportunities))), ticktext=[f"{row.home_team} vs {row.away_team}" for row in arb_opportunities.itertuples(index=False)]),
                      yaxis_title='Amount ($)', legend_title='Outcome', barmode='group', bargap=0.15)

    # Save the figure
    fig.write_image(fig_path)

def task_plot_stakes(
    depends_on = BLD_data / "arbitrage_opportunities.pkl",
    produces = BLD_figures / "arbitrage_opportunities.png"
    ):
    plot_arbitrage_opportunities(depends_on, produces)