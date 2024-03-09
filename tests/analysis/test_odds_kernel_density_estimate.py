import pandas as pd
import numpy as np
import pytest
from arbitrage_analysis.analysis.task_odds_kernel_density_estimate import kernel_density_estimation

@pytest.fixture
def mock_data():
    return pd.Series([1.4, 1.42, 1.47, 1.45, 1.42])

def test_kernel_density_estimation_basic(mock_data):
    grid, kde_vals = kernel_density_estimation(mock_data, bandwidth=0.1, gridsize=100)
    
    # Check that the grid and kde_vals are of the expected size
    assert len(grid) == 100, "Grid size should be 100"
    assert len(kde_vals) == 100, "KDE values size should be 100"
