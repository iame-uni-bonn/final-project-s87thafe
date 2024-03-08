import pandas as pd
import pytest
from arbitrage_analysis.data_management.task_seperate_best_odds import find_best_odds

@pytest.fixture
def sample_data():
    data = {
        "bookmaker": ["888sport", "Pinnacle", "1xBet", "Suprabets", "MyBookie.ag"],
        "home_team": ["AC Milan"] * 5,
        "away_team": ["Empoli"] * 5,
        "commence_time": ["2024-03-10T14:00:00Z"] * 5,
        "home_win_odds": [1.40, 1.42, 1.47, 1.45, 1.42],
        "draw_odds": [5.00, 4.69, 4.92, 5.10, 4.75],
        "away_win_odds": [7.50, 6.78, 7.55, 7.40, 6.75]
    }
    df = pd.DataFrame(data)
    test_path = "test_odds.pkl"
    df.to_pickle(test_path)
    return test_path

def test_find_best_odds(sample_data):
    result_df = find_best_odds(sample_data)
    # Assuming your function is correctly implemented, the expected outcome would be:
    expected_data = {
        "home_team": ["AC Milan"],
        "away_team": ["Empoli"],
        "commence_time": ["2024-03-10T14:00:00Z"],
        "best_odds_home": [1.47],  # Best home win odds from 1xBet
        "best_odds_draw": [5.10],  # Best draw odds from Suprabets
        "best_odds_away": [7.55],  # Best away win odds from 1xBet
        "bookie_home": ["1xBet"],
        "bookie_draw": ["Suprabets"],
        "bookie_away": ["1xBet"]
    }
    expected_df = pd.DataFrame(expected_data)
    pd.testing.assert_frame_equal(result_df.reset_index(drop=True), expected_df.reset_index(drop=True))