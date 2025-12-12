import pandas as pd
import os
import numpy as np

def load_steam_library(file_path: str) -> pd.DataFrame:
    """
    Loads the Steam library from a CSV file.
    Supports both the internal sample format and the user's provided export format.
    
    Args:
        file_path (str): Path to the CSV file.
        
    Returns:
        pd.DataFrame: DataFrame containing the game library with normalized columns:
                      [AppID, Name, Playtime_Forever, Genre, Tags, Average_Playtime]
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' was not found.")
    
    try:
        df = pd.read_csv(file_path)
        
        # Check for User Export Format (game, id, hours, ...)
        if 'game' in df.columns and 'id' in df.columns:
            # Rename columns
            df = df.rename(columns={
                'game': 'Name',
                'id': 'AppID',
                'hours': 'Playtime_Forever'
            })
            
            # Normalize Playtime
            # 'hours' column might be NaN. Fill with 0.
            df['Playtime_Forever'] = df['Playtime_Forever'].fillna(0)
            
            # Convert hours to minutes for consistency with internal logic
            # Assuming the input is in hours (float)
            df['Playtime_Forever'] = df['Playtime_Forever'] * 60
            
            # Add missing columns with defaults
            if 'Genre' not in df.columns:
                df['Genre'] = 'Unknown'
            if 'Tags' not in df.columns:
                df['Tags'] = 'Unknown'
            if 'Average_Playtime' not in df.columns:
                df['Average_Playtime'] = 0 # No time-to-beat data in this export
                
        # Basic cleaning for standard format
        # Ensure Playtime is numeric
        if 'Playtime_Forever' in df.columns:
             df['Playtime_Forever'] = pd.to_numeric(df['Playtime_Forever'], errors='coerce').fillna(0)

        # Ensure required columns exist
        required_cols = ['AppID', 'Name']
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")
                
        return df
    except Exception as e:
        raise ValueError(f"Error reading CSV file: {e}")