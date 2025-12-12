import pandas as pd
from typing import Optional

class GameRecommender:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def recommend(self, 
                  genre: Optional[str] = None, 
                  tag: Optional[str] = None, 
                  unplayed_only: bool = False,
                  min_length: Optional[int] = None,
                  max_length: Optional[int] = None
                  ) -> Optional[pd.Series]:
        """
        Returns a random game matching the criteria.
        
        Args:
            genre: Substring to match in the Genre column (case-insensitive).
            tag: Substring to match in the Tags column (case-insensitive).
            unplayed_only: If True, only considers games with 0 playtime.
            min_length: Minimum Average_Playtime (minutes).
            max_length: Maximum Average_Playtime (minutes).
        """
        if self.df.empty:
            return None
            
        filtered_df = self.df.copy()
        
        # Filter by playtime
        if unplayed_only:
            filtered_df = filtered_df[filtered_df['Playtime_Forever'] == 0]
            
        # Filter by genre
        if genre:
            filtered_df = filtered_df[filtered_df['Genre'].astype(str).str.contains(genre, case=False, na=False)]
            
        # Filter by tag
        if tag:
            filtered_df = filtered_df[filtered_df['Tags'].astype(str).str.contains(tag, case=False, na=False)]

        # Filter by length (Time to Beat)
        # Ensure the column exists before filtering
        if 'Average_Playtime' in filtered_df.columns:
            if min_length is not None:
                filtered_df = filtered_df[filtered_df['Average_Playtime'] >= min_length]
            if max_length is not None:
                filtered_df = filtered_df[filtered_df['Average_Playtime'] <= max_length]
            
        if filtered_df.empty:
            return None
            
        return filtered_df.sample(n=1).iloc[0]

    def recommend_random(self) -> Optional[pd.Series]:
        """Returns a random game from the library."""
        return self.recommend()

    def recommend_unplayed(self) -> Optional[pd.Series]:
        """Returns a random game with 0 playtime."""
        return self.recommend(unplayed_only=True)
