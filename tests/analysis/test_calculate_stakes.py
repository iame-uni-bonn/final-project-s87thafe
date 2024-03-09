import pandas as pd
from arbitrage_analysis.analysis.task_calculate_arbitrage import calculate_stakes

def test_calculate_stakes():
    # Creating a sample row with arbitrage opportunity
    sample_row = pd.Series({
        'best_odds_home': 2.0,
        'best_odds_draw': 3.0,
        'best_odds_away': 6.0,
        'total_imp_prob': 0.9
    })

    total_investment = 100

    # Manually calculating expected stakes
    expected_stake_home = (1 / 2.0 / 0.9) * total_investment
    expected_stake_draw = (1 / 3.0 / 0.9) * total_investment
    expected_stake_away = (1 / 6.0 / 0.9) * total_investment

    # Calling the calculate_stakes function
    calculated_row = calculate_stakes(sample_row, total_investment)

    # Assert
    assert calculated_row['stake_home'] == expected_stake_home, f"Expected stake_home to be {expected_stake_home}, got {calculated_row['stake_home']}"
    assert calculated_row['stake_draw'] == expected_stake_draw, f"Expected stake_draw to be {expected_stake_draw}, got {calculated_row['stake_draw']}"
    assert calculated_row['stake_away'] == expected_stake_away, f"Expected stake_away to be {expected_stake_away}, got {calculated_row['stake_away']}"
