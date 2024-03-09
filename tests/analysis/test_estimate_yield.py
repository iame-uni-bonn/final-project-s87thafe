import pandas as pd
from pathlib import Path
import tempfile
import pytest
from arbitrage_analysis.analysis.task_estimate_yield import calculate_and_filter_highest_yield

@pytest.fixture
def mock_data():
    data = {
        "home_team": ["AC Milan", "AS Roma"],
        "away_team": ["Empoli", "Sassuolo"],
        "commence_time": ["2024-03-10T14:00:00Z", "2024-03-17T17:00:00Z"],
        "best_odds_home": [1.47, 1.44],
        "best_odds_draw": [5.10, 5.60],
        "stake_home": [70, 70],
        "stake_draw": [20, 20],
        "stake_away": [10, 10],
        "payout_home": [100.6, 100.9],
        "payout_draw": [100.6, 100.9],
        "payout_away": [100.6, 100.9]
    }
    df = pd.DataFrame(data)
    df['commence_time'] = pd.to_datetime(df['commence_time'])
    return df

def test_calculate_and_filter_highest_yield_basic(mock_data):
    with tempfile.TemporaryDirectory() as tempdir:
        # Save mock data to a pickle file
        temp_path = Path(tempdir) / "mock_arbitrage_opportunity.pkl"
        mock_data.to_pickle(temp_path)

        # Call your function with the mock data path
        filtered_arbitrage_path = Path(tempdir) / "filtered_arbitrage_opportunities.pkl"
        calculate_and_filter_highest_yield(temp_path, 100, filtered_arbitrage_path)
        
        # Load the result
        result_df = pd.read_pickle(filtered_arbitrage_path)
        
        # Assertions to verify your function's behavior
        assert not result_df.empty, "The result should not be empty"
        assert 'yield' in result_df.columns, "Result DataFrame must contain 'yield' column"
        assert 'investment_growth' in result_df.columns, "Result DataFrame must contain 'investment_growth' column"
