import pandas as pd
from arbitrage_analysis.config import SRC, BLD_data, BLD_figures

depends_on=pd.read_pickle(BLD_data / "arbitrage_opportunities.pkl")

print(depends_on.head())