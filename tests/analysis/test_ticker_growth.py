import pandas as pd
import numpy as np
import tempfile
from pathlib import Path
import pytest
from arbitrage_analysis.analysis.task_estimate_yield import ticker_growth_path

@pytest.fixture
def mock_yield_data():
    data = {
        "Average Daily Change": [1.0, 1.009256, 0.994140, 1.006043, 1.003111]
    }
    df = pd.DataFrame(data)
    return df

def test_ticker_growth_path(mock_yield_data):
    with tempfile.TemporaryDirectory() as tempdir:
        # Save mock data to a pickle file
        yield_path = Path(tempdir) / "mock_yield_data.pkl"
        mock_yield_data.to_pickle(yield_path)

        # Specify the path for the output to be tested
        output_path = Path(tempdir) / "output_growth_path.pkl"

        # Initial investment
        initial_investment = 100

        # Call the function with the test paths
        ticker_growth_path(yield_path, initial_investment, output_path)

        # Load the result
        result_df = pd.read_pickle(output_path)

        # Assertions to verify the function's behavior
        assert not result_df.empty, "The result should not be empty"
        assert 'investment_growth_ticker' in result_df.columns, "Result DataFrame must contain 'investment_growth_ticker' column"
        
        # Verify the growth calculations - simplified example
        expected_growth = initial_investment
        for change in mock_yield_data['Average Daily Change']:
            expected_growth *= change
        np.testing.assert_almost_equal(result_df['investment_growth_ticker'].iloc[-1], expected_growth, decimal=5, err_msg="Final investment growth does not match expected value")