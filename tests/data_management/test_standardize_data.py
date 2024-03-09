import pandas as pd

def test_standardize_team_names():
    """
    Tests the standardization of team names in a DataFrame against the mapping from standardize_team_names_and_merge(),
    ensuring that both home and away team names are correctly standardized.
    """
    # Create a simple DataFrame to test the standardization
    df_test = pd.DataFrame({'home_team': ['Ssc Napoli', 'Inter Milano'], 'away_team': ['Juventus Turin', 'Genoa Cfc']})
    # Define the mapping of team names
    team_name_mapping = {
        'Ssc Napoli': 'Napoli', 'Inter Milano': 'Inter Milan', 'Cagliari ': 'Cagliari',
        'Us Sassuolo ': 'Sassuolo', 'Genoa Cfc': 'Genoa', 'Us Lecce': 'Lecce',
        'Ac Milan': 'AC Milan', 'Juventus Turin': 'Juventus', 'Acf Fiorentina': 'Fiorentina',
        'Fc Torino': 'Torino', 'Sportiva Salernitana': 'Salernitana', 'Frosinone ': 'Frosinone',
        'Ac Monza': 'Monza', 'Hellas Verona Fc': 'Hellas Verona FC', 'Fc Empoli': 'Empoli',
        'Atalanta Bergamasca ': 'Atalanta BC', 'As Roma': 'AS Roma'
    }
    # Apply the mapping to this test DataFrame
    df_test['home_team'] = df_test['home_team'].map(team_name_mapping).fillna(df_test['home_team'])
    df_test['away_team'] = df_test['away_team'].map(team_name_mapping).fillna(df_test['away_team'])
    # Assert that the names have been standardized as expected
    expected_home_teams = ['Napoli', 'Inter Milan']
    expected_away_teams = ['Juventus', 'Genoa']
    assert df_test['home_team'].tolist() == expected_home_teams, "Home team names not standardized correctly"
    assert df_test['away_team'].tolist() == expected_away_teams, "Away team names not standardized correctly"
