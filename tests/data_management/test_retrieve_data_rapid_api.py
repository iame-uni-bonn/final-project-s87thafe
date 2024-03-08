import pandas as pd
import pytest
from arbitrage_analysis.data_management.task_retrieve_odds_rapid_api import extract_odds_rapid_api  # Adjust the import based on your script's actual name

def mock_read_csv(file_path):
    # Simulate a DataFrame with mock data for multiple matches
    data = {}
    for i in range(5):  # Simulating data for 5 matches as an example
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
    # Use monkeypatch to replace pd.read_csv with mock_read_csv for testing
    monkeypatch.setattr(pd, "read_csv", mock_read_csv)

def test_extract_odds_with_mock(mock_df):
    # Call the function with a dummy path, as pd.read_csv is mocked
    result_df = extract_odds_rapid_api("dummy_path.csv")
    
    # Define the expected columns based on your function's output specification
    expected_columns = ['away_team', 'home_team', 'away', 'home', 'draw', 'bookie']

    # Assertions to verify the DataFrame is as expected
    assert not result_df.empty, "The DataFrame should not be empty."
    assert list(result_df.columns) == expected_columns, "DataFrame should have the expected column names."
    assert result_df.isna().sum().sum() == 0, "DataFrame should not contain NaN values."

