import pandas as pd
import json

df_odds = pd.read_csv('C:/Users/hafer/OneDrive/Desktop/Universitatsi/Economics_Bonn/3rd_Semester/Effective_Programming_Practices/final-project-s87thafe/df_odds.csv')

def create_odds_dataframe(bookmakers_json, home_team, away_team):
    bookmakers_data = json.loads(bookmakers_json.replace("'", "\""))
    bookmakers_odds = []

    for bookmaker in bookmakers_data:
        bookmaker_odds = {
            'bookmaker': bookmaker['title'],
            'home_team': home_team,  # Add home team name
            'away_team': away_team,  # Add away team name
            'home_win_odds': None,
            'draw_odds': None,
            'away_win_odds': None
        }
        for market in bookmaker['markets']:
            if market['key'] == 'h2h':
                for outcome in market['outcomes']:
                    if outcome['name'] == home_team:
                        bookmaker_odds['home_win_odds'] = outcome['price']
                    elif outcome['name'] == away_team:
                        bookmaker_odds['away_win_odds'] = outcome['price']
                    elif outcome['name'] == 'Draw':
                        bookmaker_odds['draw_odds'] = outcome['price']
        bookmakers_odds.append(bookmaker_odds)

    return pd.DataFrame(bookmakers_odds)

# Initialize an empty list to store each game's DataFrame
all_games_odds = []

# Iterate over each game in the dataset
for index, row in df_odds.iterrows():
    game_odds_df = create_odds_dataframe(row['bookmakers'], row['home_team'], row['away_team'])
    all_games_odds.append(game_odds_df)

# Concatenate all individual DataFrames into a single DataFrame
df_all_games_odds = pd.concat(all_games_odds, ignore_index=True)

# Display the combined DataFrame
df_all_games_odds.to_csv("df_all_games_odds.csv", index=False)
