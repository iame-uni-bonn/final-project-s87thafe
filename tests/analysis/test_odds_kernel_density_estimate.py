import pandas as pd
import numpy as np
import pytest
import tempfile
from pathlib import Path
from arbitrage_analysis.analysis.task_odds_kernel_density_estimate import kernel_density_estimation

@pytest.fixture
def mock_odds_data():
    data = {
        "home_win_odds": [1.40, 1.42, 1.47, 1.45, 1.42],
        "draw_odds": [5.00, 4.69, 4.92, 5.10, 4.75],
        "away_win_odds": [7.50, 6.78, 7.55, 7.40, 6.75]
    }
    df = pd.DataFrame(data)
    return df

def test_kernel_density_estimation_basic(mock_odds_data):
    """Tests the kernel density estimation function with mock data for expected output sizes."""
    with tempfile.TemporaryDirectory() as tempdir:
        # Save mock data to a pickle file
        odds_path = Path(tempdir) / "mock_odds_data.pkl"
        mock_odds_data.to_pickle(odds_path)

        # Call the kernel density estimation function
        grid, kde_vals = kernel_density_estimation(odds_path, bandwidth=0.1, gridsize=100)

        # Test assertions
        assert len(grid) == 100, "Grid size should be 100"
        assert len(kde_vals) == 100, "KDE values size should be 100"

