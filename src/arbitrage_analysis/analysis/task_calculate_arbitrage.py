import pandas as pd
from arbitrage_analysis.config import SRC, BLD_data, BLD_figures

def identify_arbitrage_opportunities(df_path, total_investment, output_path):
    """
    Identifies arbitrage opportunities from odds data and calculates stakes.

    Parameters:
    - df_path (str or Path): Path to the DataFrame containing odds information.
    - total_investment (float): Total investment amount for arbitrage betting.
    - output_path (str or Path): Path to save the DataFrame with arbitrage opportunities.
    """
    df = pd.read_pickle(df_path)
    
    # Calculate implied probabilities and total implied probability
    df['imp_prob_home'] = 1 / df['best_odds_home']
    df['imp_prob_draw'] = 1 / df['best_odds_draw']
    df['imp_prob_away'] = 1 / df['best_odds_away']
    df['total_imp_prob'] = df['imp_prob_home'] + df['imp_prob_draw'] + df['imp_prob_away']
    
    # Identify arbitrage opportunities
    arb_opportunities = df[df['total_imp_prob'] < 1].copy()
    
    # Calculate potential arbitrage profit margin
    arb_opportunities['arb_profit_margin'] = (1 - arb_opportunities['total_imp_prob']) * 100
    
    # Apply function to calculate stakes
    arb_opportunities = arb_opportunities.apply(lambda row: calculate_stakes(row, total_investment), axis=1)
    
    # Calculate expected payout for each bet
    arb_opportunities['payout_home'] = arb_opportunities['stake_home'] * arb_opportunities['best_odds_home']
    arb_opportunities['payout_draw'] = arb_opportunities['stake_draw'] * arb_opportunities['best_odds_draw']
    arb_opportunities['payout_away'] = arb_opportunities['stake_away'] * arb_opportunities['best_odds_away']
    
    arb_opportunities.to_pickle(output_path)

def calculate_stakes(row, total_investment):
    """
    Calculate the stakes for each betting outcome (home win, draw, away win) based on total investment and implied probabilities.

    Parameters:
    - row (Series): A Pandas Series containing odds information for a single match.
    - total_investment (float): The total amount of money to be invested across all outcomes.

    Returns:
    - row (Series): The original Series updated with the calculated stake amounts for each outcome.
    """
    total_imp_prob = row['total_imp_prob']
    row['stake_home'] = (1 / row['best_odds_home'] / total_imp_prob) * total_investment
    row['stake_draw'] = (1 / row['best_odds_draw'] / total_imp_prob) * total_investment
    row['stake_away'] = (1 / row['best_odds_away'] / total_imp_prob) * total_investment
    return row


def task_calculate_arbitrage_stakes(
    depends_on = BLD_data / "best_odds_info.pkl",
    produces= BLD_data / "arbitrage_opportunities.pkl"
    ):
    total_investment = 100  # Define total investment
    identify_arbitrage_opportunities(depends_on, total_investment, produces)
