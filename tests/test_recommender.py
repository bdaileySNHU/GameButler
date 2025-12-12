import pytest
import pandas as pd
from src.recommender import GameRecommender

@pytest.fixture
def sample_df():
    data = {
        'AppID': [1, 2, 3, 4, 5],
        'Name': ['Short Game', 'Long Game', 'Medium Game', 'Zero Length', 'Just Right'],
        'Playtime_Forever': [100, 50, 0, 20, 30],
        'Average_Playtime': [60, 3000, 600, 0, 1200], # Minutes: 1h, 50h, 10h, 0h, 20h
        'Genre': ['Action', 'RPG', 'Action', 'Puzzle', 'Action'],
        'Tags': ['Indie', 'Story', 'Shooter', 'Logic', 'FPS']
    }
    return pd.DataFrame(data)

def test_recommend_random(sample_df):
    recommender = GameRecommender(sample_df)
    game = recommender.recommend_random()
    assert game is not None

def test_recommend_by_length_short(sample_df):
    recommender = GameRecommender(sample_df)
    # Filter for games <= 1 hour (60 mins)
    game = recommender.recommend(max_length=60)
    assert game is not None
    assert game['Average_Playtime'] <= 60
    # Should likely match 'Short Game' or 'Zero Length'
    assert game['Name'] in ['Short Game', 'Zero Length']

def test_recommend_by_length_long(sample_df):
    recommender = GameRecommender(sample_df)
    # Filter for games >= 40 hours (2400 mins)
    game = recommender.recommend(min_length=2400)
    assert game is not None
    assert game['Average_Playtime'] >= 2400
    assert game['Name'] == 'Long Game'

def test_recommend_by_length_range(sample_df):
    recommender = GameRecommender(sample_df)
    # Between 5 and 15 hours (300 - 900 mins)
    game = recommender.recommend(min_length=300, max_length=900)
    assert game is not None
    assert 300 <= game['Average_Playtime'] <= 900
    assert game['Name'] == 'Medium Game'
