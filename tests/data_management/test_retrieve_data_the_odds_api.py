import pytest
import pandas as pd
from arbitrage_analysis.data_management.task_retrieve_odds_the_odds_api import extract_odds_the_odds_api

def test_extract_odds_the_odds_api():
    """Ensures that odds data is correctly extracted from JSON and converted to a DataFrame with the expected format and values."""
    # Sample JSON data
    bookmakers_json = """
    [
        {
            "title": "Bookmaker1",
            "markets": [
                {
                    "key": "h2h",
                    "outcomes": [
                        {"name": "Team A", "price": 2.1},
                        {"name": "Team B", "price": 3.5},
                        {"name": "Draw", "price": 3.0}
                    ]
                }
            ]
        }
    ]
    """
    home_team = "Team A"
    away_team = "Team B"
    commence_time = "2022-03-15T00:00:00Z"

    expected_df = pd.DataFrame([
        {
            'bookmaker': 'Bookmaker1',
            'home_team': home_team,
            'away_team': away_team,
            'commence_time': commence_time,
            'home_win_odds': 2.1,
            'draw_odds': 3.0,
            'away_win_odds': 3.5
        }
    ])

    result_df = extract_odds_the_odds_api(bookmakers_json, home_team, away_team, commence_time)

    pd.testing.assert_frame_equal(result_df.sort_index(axis=1), expected_df.sort_index(axis=1), check_dtype=False)

