import pytest
import pandas as pd
import os
from src.data_loader import load_steam_library

# Get absolute path to the sample data
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLE_CSV_PATH = os.path.join(BASE_DIR, 'data', 'sample_library.csv')
REAL_CSV_PATH = os.path.join(BASE_DIR, 'data', 'real_library_sample.csv')

def test_load_steam_library_success():
    """Test loading a valid internal format CSV file."""
    df = load_steam_library(SAMPLE_CSV_PATH)
    assert not df.empty
    assert 'Name' in df.columns
    assert 'AppID' in df.columns

def test_load_real_library_format():
    """Test loading the user's specific export format."""
    df = load_steam_library(REAL_CSV_PATH)
    assert not df.empty
    assert 'Name' in df.columns
    assert 'AppID' in df.columns
    assert 'Playtime_Forever' in df.columns
    
    # Check normalization
    assert df.iloc[0]['Name'] == '(the) Gnorp Apologue'
    # Hours was empty in csv -> 0 -> 0 mins
    assert df.iloc[0]['Playtime_Forever'] == 0 
    assert df.iloc[0]['Genre'] == 'Unknown'

def test_load_steam_library_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_steam_library("non_existent_file.csv")