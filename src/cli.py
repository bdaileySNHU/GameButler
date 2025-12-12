import argparse
import sys
import os
from src.data_loader import load_steam_library
from src.recommender import GameRecommender

def main():
    parser = argparse.ArgumentParser(description="GameButler: Your personal game recommender.")
    parser.add_argument('--csv', type=str, default='data/sample_library.csv', help='Path to your Steam library CSV file.')
    
    # Filter arguments
    parser.add_argument('--mode', choices=['random', 'unplayed'], default='random', help='Recommendation mode (basic).')
    parser.add_argument('--genre', type=str, help='Filter by genre (e.g., "Action").')
    parser.add_argument('--tag', type=str, help='Filter by tag (e.g., "Sci-Fi").')
    parser.add_argument('--length', choices=['short', 'medium', 'long'], help='Filter by game length (Short < 5h, Long > 20h).')
    parser.add_argument('--unplayed', action='store_true', help='Only recommend unplayed games (overrides --mode).')
    
    args = parser.parse_args()
    
    csv_path = args.csv
    if not os.path.exists(csv_path):
        print(f"Error: File not found at {csv_path}")
        sys.exit(1)
        
    try:
        df = load_steam_library(csv_path)
    except Exception as e:
        print(f"Error loading library: {e}")
        sys.exit(1)
        
    recommender = GameRecommender(df)
    
    # Determine unplayed status
    unplayed_only = args.unplayed or (args.mode == 'unplayed' and not args.genre and not args.tag and not args.length)
    if args.mode == 'unplayed':
        unplayed_only = True

    # Determine length constraints
    min_len = None
    max_len = None
    
    if args.length == 'short':
        max_len = 300  # < 5 hours
    elif args.length == 'long':
        min_len = 1200 # > 20 hours
    elif args.length == 'medium':
        min_len = 300
        max_len = 1200

    game = recommender.recommend(
        genre=args.genre, 
        tag=args.tag, 
        unplayed_only=unplayed_only,
        min_length=min_len,
        max_length=max_len
    )
        
    if game is not None:
        print("\n" + "="*40)
        print("GameButler Recommends:")
        print("="*40)
        print(f"Title:    {game['Name']}")
        print(f"Genre:    {game['Genre']}")
        print(f"Tags:     {game['Tags']}")
        if 'Average_Playtime' in game:
            print(f"Est. Len: {game['Average_Playtime']} mins")
        print(f"Playtime: {game['Playtime_Forever']} minutes")
        print("="*40 + "\n")
    else:
        print("\nNo suitable game found matching your criteria.\n")

if __name__ == "__main__":
    main()
