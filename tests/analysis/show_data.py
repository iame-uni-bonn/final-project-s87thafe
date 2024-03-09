import pandas as pd
from arbitrage_analysis.config import SRC, BLD_data, BLD_figures

depends_on=pd.read_pickle(BLD_data / "best_odds_info.pkl")

print(depends_on)
