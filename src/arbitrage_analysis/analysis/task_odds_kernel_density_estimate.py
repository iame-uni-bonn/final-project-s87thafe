from arbitrage_analysis.config import BLD_data, BLD_figures
import pandas as pd
import numpy as np

def kernel_density_estimation(all_odds_path, bandwidth=0.5, gridsize=1000):
    """
    Loads odds data from a specified path and calculates the kernel density estimate (KDE) using a Gaussian kernel. 
    The KDE is computed for combined home win, draw, and away win odds, and is normalized appropriately.

    Args:
        all_odds_path (Path): Path to the pickle file containing the DataFrame of all odds (home win, draw, away win).
        bandwidth (float, optional): Bandwidth for the kernel, controlling the smoothness of the estimate. Defaults to 0.5.
        gridsize (int, optional): Number of points where the KDE is evaluated, determining the resolution. Defaults to 1000.

    Returns:
        tuple: A tuple (grid, kde_vals) where:
              - grid (numpy.ndarray): Array of points at which the KDE is evaluated.
              - kde_vals (numpy.ndarray): Values of the KDE at the points in the grid.
    """
    df_all_odds = pd.read_pickle(all_odds_path)

    # Combine all odds into a single series, removing any NaN values which might disrupt the KDE calculation
    all_odds = pd.concat([df_all_odds['home_win_odds'], df_all_odds['draw_odds'], df_all_odds['away_win_odds']]).dropna()

    # Calculate KDE for the combined odds
    grid = np.linspace(all_odds.min(), all_odds.max(), gridsize)
   
    kde_vals = np.zeros(gridsize)
   
    n = len(all_odds)
   
    for value in all_odds:
        kernel = np.exp(-0.5 * ((grid - value) / bandwidth) ** 2) / (bandwidth * np.sqrt(2 * np.pi))
        kde_vals += kernel / (n * bandwidth)
    
    return grid, kde_vals

def task_odds_kernel_density_estimate(
    depends_on = BLD_data / 'all_odds_merged.pkl',
    produces = BLD_data / 'odds_kde_with_arbitrage_opportunities.pkl'
    ):
    # Calculate KDE for the combined odds
    all_odds_x, all_odds_y = kernel_density_estimation(all_odds_path=depends_on, bandwidth=1, gridsize=1000)
    # Save the KDE values to a pickle file
    pd.to_pickle((all_odds_x, all_odds_y), produces)