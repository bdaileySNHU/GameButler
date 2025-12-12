print("Starting API module...")
from fastapi import FastAPI, HTTPException, Query, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
import shutil
import pandas as pd
from typing import Optional
from src.data_loader import load_steam_library
from src.recommender import GameRecommender

print("Imports complete.")

app = FastAPI(
    title="GameButler API",
    description="API for recommending Steam games.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev, allow all. In prod, specify domain.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global recommender instance
recommender = None

# Load the initial sample data
DEFAULT_CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_library.csv')

def initialize_recommender(csv_path: str):
    global recommender
    try:
        game_data = load_steam_library(csv_path)
        recommender = GameRecommender(game_data)
        print(f"Data loaded from {csv_path}.")
    except Exception as e:
        print(f"Error loading data: {e}")
        recommender = GameRecommender(pd.DataFrame())

if os.path.exists(DEFAULT_CSV_PATH):
    initialize_recommender(DEFAULT_CSV_PATH)
else:
    print(f"Warning: Default data file not found at {DEFAULT_CSV_PATH}")
    recommender = GameRecommender(pd.DataFrame())

class RecommendationResponse(BaseModel):
    AppID: int
    Name: str
    Playtime_Forever: int
    Genre: str
    Tags: str
    Average_Playtime: Optional[int] = None

@app.get("/")
async def root():
    return {"message": "Welcome to GameButler API! Visit /docs for API documentation."}

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "GameButler API is running."}

@app.post("/upload")
async def upload_library(file: UploadFile = File(...)):
    """
    Upload a new Steam library CSV file.
    """
    temp_file_path = f"temp_{file.filename}"
    
    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Validate and load the new data
        # In a real app, we'd probably save this to a persistent 'user_data' folder
        initialize_recommender(temp_file_path)
        
        # Cleanup
        os.remove(temp_file_path)
        
        return {"message": f"Successfully loaded library from {file.filename}", "games_count": len(recommender.df)}
        
    except Exception as e:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise HTTPException(status_code=400, detail=f"Failed to process file: {str(e)}")

@app.get("/recommend", response_model=RecommendationResponse)
async def recommend_game(
    genre: Optional[str] = None,
    tag: Optional[str] = None,
    unplayed_only: bool = False,
    length: Optional[str] = Query(None, regex="^(short|medium|long)$")
):
    """
    Get a game recommendation based on filters.
    """
    if recommender is None or recommender.df.empty:
        raise HTTPException(status_code=404, detail="No game library loaded. Please upload a CSV file.")

    min_len = None
    max_len = None
    
    if length == 'short':
        max_len = 300
    elif length == 'long':
        min_len = 1200
    elif length == 'medium':
        min_len = 300
        max_len = 1200
        
    game = recommender.recommend(
        genre=genre,
        tag=tag,
        unplayed_only=unplayed_only,
        min_length=min_len,
        max_length=max_len
    )
    
    if game is None:
        raise HTTPException(status_code=404, detail="No suitable game found matching your criteria.")
        
    return game.to_dict()

if __name__ == "__main__":
    print("Starting Uvicorn...")
    uvicorn.run(app, host="0.0.0.0", port=8000)