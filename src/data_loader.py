import pandas as pd
import os

def load_steam_library(file_path: str) -> pd.DataFrame:
    """
    Loads the Steam library from a CSV file.
    
    Args:
        file_path (str): Path to the CSV file.
        
    Returns:
        pd.DataFrame: DataFrame containing the game library.
        
    Raises:
        FileNotFoundError: If the file does not exist.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' was not found.")
    
    try:
        df = pd.read_csv(file_path)
        # basic cleaning can go here if needed
        return df
    except Exception as e:
        raise ValueError(f"Error reading CSV file: {e}")
