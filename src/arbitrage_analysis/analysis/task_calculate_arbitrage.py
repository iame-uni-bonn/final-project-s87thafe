import pandas as pd
from arbitrage_analysis.config import BLD_data

def identify_arbitrage_opportunities(df_path, total_investment, output_path):
    """
    Identifies arbitrage opportunities from given betting odds data, calculates stakes for each outcome, and saves the results.

    This function processes a dataset of betting odds to identify arbitrage opportunities, calculates the optimal stakes for each outcome to ensure a profit regardless of the match result, and saves the resulting dataset with arbitrage opportunities and their respective stakes to a specified path.

    Args:
        df_path (Path): Path to the DataFrame containing betting odds information.
        total_investment (float): Total investment amount allocated for arbitrage betting.
        output_path (Path): Destination path for saving the DataFrame with identified arbitrage opportunities and calculated stakes.

    Returns:
        None: The function does not return any value. The results are saved to `output_path`.
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
    arb_opportunities = arb_opportunities.apply(lambda row: _calculate_stakes(row, total_investment), axis=1)
    
    # Calculate expected payout for each bet
    arb_opportunities['payout_home'] = arb_opportunities['stake_home'] * arb_opportunities['best_odds_home']
    arb_opportunities['payout_draw'] = arb_opportunities['stake_draw'] * arb_opportunities['best_odds_draw']
    arb_opportunities['payout_away'] = arb_opportunities['stake_away'] * arb_opportunities['best_odds_away']
    
    arb_opportunities.to_pickle(output_path)

def _calculate_stakes(row, total_investment):
    """
    Calculates the stakes for each possible outcome (home win, draw, away win) based on the total investment and the odds of each outcome.

    This function computes the amount to be staked on each possible outcome of a single game, ensuring that the total investment is optimally distributed according to the implied probabilities derived from the odds. The aim is to guarantee a profit regardless of the game's outcome if an arbitrage opportunity is present.

    Args:
        row (pd.Series): A Pandas Series containing the odds and implied probabilities for a single match.
        total_investment (float): The total amount to be invested in the identified arbitrage opportunity.

    Returns:
        pd.Series: The input Series updated with the stake amounts calculated for each betting outcome.
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
    total_investment = 100
    identify_arbitrage_opportunities(depends_on, total_investment, produces)
