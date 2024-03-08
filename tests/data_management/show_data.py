import pandas as pd
from arbitrage_analysis.config import SRC, BLD_data

df_the_odds_api_path = BLD_data / "all_odds_the_odds_api.pkl"
df_rapid_api_path = BLD_data / "all_odds_rapid_api.pkl"
df_the_odds_api = pd.read_pickle(df_the_odds_api_path)
df_rapid_api = pd.read_pickle(df_rapid_api_path)
print(df_the_odds_api)
# print(df_rapid_api.head())