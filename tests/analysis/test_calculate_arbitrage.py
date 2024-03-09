import pandas as pd
import pytest
import os
import numpy as np
from arbitrage_analysis.analysis.task_calculate_arbitrage import identify_arbitrage_opportunities

# Sample data
data = {
    'home_team': ['AC Milan', 'AS Roma'],
    'away_team': ['Empoli', 'Sassuolo'],
    'commence_time': ['2024-03-10T14:00:00Z', '2024-03-17T17:00:00Z'],
    'best_odds_home': [1.47, 1.44],
    'best_odds_draw': [5.10, 5.60],
    'best_odds_away': [8.50, 8.50]
}

# Setup function to create a sample DataFrame and save it as a pickle
@pytest.fixture(scope="module")
def setup_data(tmpdir_factory):
    df = pd.DataFrame(data)
    file = tmpdir_factory.mktemp("data").join("odds_info.pkl")
    df.to_pickle(file)
    return file

def test_identify_arbitrage_opportunities(setup_data):
    """Tests arbitrage opportunity identification for sample betting odds data."""
    output_path = setup_data.dirname + '/arbitrage_opportunities.pkl'
    identify_arbitrage_opportunities(setup_data, 100, output_path)
    result_df = pd.read_pickle(output_path)
    
    # Assert
    assert os.path.exists(output_path), "Output file was not created."
    assert not result_df.empty, "No arbitrage opportunities were identified."
    np.testing.assert_allclose(result_df['payout_home'].values, result_df['payout_draw'].values, rtol=1e-5, atol=0, err_msg="Payouts for home and draw should be almost equal.")
    np.testing.assert_allclose(result_df['payout_home'].values, result_df['payout_away'].values, rtol=1e-5, atol=0, err_msg="Payouts for home and away should be almost equal.")