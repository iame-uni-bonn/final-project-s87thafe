import plotly.graph_objects as go
import pandas as pd
from arbitrage_analysis.config import BLD_figures

arb_opportunities = pd.read_pickle(BLD_figures / "arbitrage_opportunities.pkl")

fig = go.Figure()

bar_width = 0.2
offset = 0.2  # Adjust this for spacing between bars

# Use a numeric index for the x-axis positions
for i, row in enumerate(arb_opportunities.itertuples(index=False)):
    match_index = i

    # Calculate the potential payout for the current row
    potential_payout = max(
        getattr(row, 'stake_home') * getattr(row, 'best_odds_home'),
        getattr(row, 'stake_draw') * getattr(row, 'best_odds_draw'),
        getattr(row, 'stake_away') * getattr(row, 'best_odds_away')
    )
    
    # Add the bars for stakes
    fig.add_trace(go.Bar(
        name='Home Win Stake',
        x=[match_index - offset],  # Adjust x position by subtracting offset
        y=[getattr(row, 'stake_home')],
        marker_color='lightblue',
        width=bar_width,
        showlegend=(i == 0)  # Show legend only for the first set of bars
    ))
    fig.add_trace(go.Bar(
        name='Draw Stake',
        x=[match_index],  # Centered x position for draw
        y=[getattr(row, 'stake_draw')],
        marker_color='lightgreen',
        width=bar_width,
        showlegend=(i == 0)
    ))
    fig.add_trace(go.Bar(
        name='Away Win Stake',
        x=[match_index + offset],  # Adjust x position by adding offset
        y=[getattr(row, 'stake_away')],
        marker_color='coral',
        width=bar_width,
        showlegend=(i == 0)
    ))
    
    # Add the bar for potential payout
    fig.add_trace(go.Bar(
        name='Potential Payout',
        x=[match_index + 2 * offset],  # Adjust x position further by adding double offset
        y=[potential_payout],
        marker_color='gold',
        width=bar_width,
        showlegend=(i == 0)
    ))

# Add a horizontal line to represent the total investment
total_investment = 100  # Replace this with your total investment value
fig.add_shape(
    type='line',
    x0=-0.5,
    y0=total_investment,
    x1=len(arb_opportunities) - 0.5,
    y1=total_investment,
    line=dict(color='red', width=3),
    name='Total Investment'
)
fig.add_trace(go.Scatter(
    x=[-0.5, len(arb_opportunities) - 0.5], 
    y=[total_investment, total_investment],
    mode='lines',
    line=dict(color='red', width=3),
    showlegend=False
))

# Update layout
fig.update_layout(
    title='Arbitrage Opportunities: Stakes and Payout per Game',
    xaxis=dict(
        tickmode='array',
        tickvals=list(range(len(arb_opportunities))),
        ticktext=[f"{row.home_team} vs {row.away_team}" for row in arb_opportunities.itertuples(index=False)]
    ),
    yaxis_title='Amount ($)',
    legend_title='Outcome',
    barmode='group',
    bargap=0.15  # Adjust the gap between bars as needed
)

fig.show()