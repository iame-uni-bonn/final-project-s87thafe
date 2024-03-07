from arbitrage_analysis.config import BLD_data, BLD_figures
import pandas as pd
import numpy as np

def kernel_density_estimation(data, bandwidth=0.5, gridsize=1000):
    """
    Calculate the kernel density estimate (KDE) with proper normalization.
    
    Parameters:
    - data: pandas.Series, the data for which to calculate the KDE.
    - bandwidth: float, the bandwidth for the KDE calculation.
    - gridsize: int, the number of points to generate for the KDE plot.
    
    Returns:
    - A tuple of (grid, kde_vals) where 'grid' is a numpy array of points at which the KDE is evaluated,
      and 'kde_vals' is a numpy array of KDE values at those points.
    """
    grid = np.linspace(data.min(), data.max(), gridsize)
    kde_vals = np.zeros(gridsize)
    n = len(data)
    for value in data:
        kernel = np.exp(-0.5 * ((grid - value) / bandwidth) ** 2) / (bandwidth * np.sqrt(2 * np.pi))
        kde_vals += kernel / (n * bandwidth)
    return grid, kde_vals

def task_odds_kernel_density_estimate(
    depends_on = BLD_data / 'all_odds_merged.pkl',
    produces = BLD_data / 'odds_kde_with_arbitrage_opportunities.pkl'
    ):
    df_all_odds = pd.read_pickle(depends_on)
    # Combine all odds into a single series, removing any NaN values which might disrupt the KDE calculation
    all_odds = pd.concat([df_all_odds['home_win_odds'], df_all_odds['draw_odds'], df_all_odds['away_win_odds']]).dropna()
    # Calculate KDE for the combined odds
    all_odds_x, all_odds_y = kernel_density_estimation(all_odds, bandwidth=1, gridsize=1000)
    # Save the KDE values to a pickle file
    pd.to_pickle((all_odds_x, all_odds_y), produces)