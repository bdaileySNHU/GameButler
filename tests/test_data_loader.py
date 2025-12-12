import pytest
import pandas as pd
import os
from src.data_loader import load_steam_library

# Get absolute path to the sample data
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLE_CSV_PATH = os.path.join(BASE_DIR, 'data', 'sample_library.csv')

def test_load_steam_library_success():
    """Test loading a valid CSV file."""
    df = load_steam_library(SAMPLE_CSV_PATH)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert 'Name' in df.columns
    assert 'AppID' in df.columns
    assert len(df) >= 10  # We put 10 items in the sample

def test_load_steam_library_file_not_found():
    """Test that loading a non-existent file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        load_steam_library("non_existent_file.csv")
