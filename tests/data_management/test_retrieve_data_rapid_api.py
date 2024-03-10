import pandas as pd
import pytest
from arbitrage_analysis.data_management.task_retrieve_odds_rapid_api import extract_odds_rapid_api

def _mock_read_csv(file_path):
    """
    Simulates reading a CSV file and returns a DataFrame with mock odds data for testing purposes.

    Args:
        file_path (str): The file path for the CSV file to be read. This parameter is ignored in this mock function.

    Returns:
        pd.DataFrame: A DataFrame containing simulated odds data for multiple matches.
    """
    # Simulate a DataFrame with mock data for multiple matches
    data = {}
    for i in range(5):
        data.update({
            f'{i}.away_team': [f'Team A{i}'],
            f'{i}.home_team': [f'Team B{i}'],
            f'{i}.away': [1.5 + i],
            f'{i}.home': [2.5 + i],
            f'{i}.draw': [3.0 + i],
            f'{i}.bookie': [f'Bookie{i}']
        })
    return pd.DataFrame(data)

@pytest.fixture
def mock_df(monkeypatch):
    # Use monkeypatch to replace pd.read_csv with mock_read_csv
    monkeypatch.setattr(pd, "read_csv", _mock_read_csv)

def test_extract_odds_with_mock(mock_df):
    """Verifies that the extraction of odds from a mocked CSV via Rapid API produces a DataFrame with the expected structure and no NaN values."""
    # Call the function with a dummy path
    result_df = extract_odds_rapid_api("dummy_path.csv")
    
    # Define expected columns
    expected_columns = ['away_team', 'home_team', 'away', 'home', 'draw', 'bookie']

    # Assert
    assert not result_df.empty, "The DataFrame should not be empty."
    assert list(result_df.columns) == expected_columns, "DataFrame should have the expected column names."
    assert result_df.isna().sum().sum() == 0, "DataFrame should not contain NaN values."

