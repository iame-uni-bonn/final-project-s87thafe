import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from arbitrage_analysis.data_management.task_retrieve_data_yfinance import calculate_average_returns

@pytest.fixture
def mock_yfinance_data():
    # Create a sample DataFrame that mimics yfinance data structure
    data = pd.DataFrame({
        'Close': [100, 105, 102, 110, 108, 112, 115, 113, 118, 120, 122, 125, 127, 130, 132, 135]
    })
    data['Close'] = data['Close'].astype(float)
    return data

def test_calculate_average_returns(mock_yfinance_data):
    with patch('arbitrage_analysis.data_management.task_retrieve_data_yfinance.yf.download', return_value=mock_yfinance_data) as mock_download, \
         patch('pandas.DataFrame.to_pickle') as mock_to_pickle:

        # Call the function with a sample ticker and a path
        calculate_average_returns('AAPL', 'dummy/path.pkl')

        # Ensure yfinance.download was called correctly
        mock_download.assert_called_once_with('AAPL', period="1y")

        # Assert to_pickle was called with the correct path
        mock_to_pickle.assert_called_once_with('dummy/path.pkl')