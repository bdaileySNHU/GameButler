# GameButler Backlog

## Epic 1: MVP CLI Game Recommender
**Goal:** A local command-line tool that ingests a Steam CSV and suggests a game to play.
- [x] **Story 1.1: Project Skeleton & Environment**
  - Create project structure.
  - Set up virtual environment and `requirements.txt`.
  - Create a sample/mock Steam CSV file for testing.
- [x] **Story 1.2: Data Ingestion**
  - Implement a Python module to parse the CSV file using Pandas.
  - Clean and normalize data (e.g., handle missing playtimes).
- [x] **Story 1.3: Recommendation Engine (Basic)**
  - Implement logic to select a game.
  - criteria: "Random Unplayed" or "Random from Backlog".
- [x] **Story 1.4: CLI Interface**
  - Create a main entry point (`main.py` or similar).
  - Allow user to specify CSV path via arguments.
  - Print the recommendation clearly.

## Epic 2: Recommendation Engine Improvements
**Goal:** Smarter recommendations based on more data points.
- [x] **Story 2.1: Genre & Tag Filtering**
  - specificy "RPG" or "Action".
- [x] **Story 2.2: Time-to-Beat Integration**
  - Filter by "Short" (< 5 hrs) vs "Long" (> 20 hrs).

## Epic 3: Web API (Backend)
**Goal:** Expose the recommendation logic via a REST API.
- [x] **Story 3.1: API Framework Setup**
  - Initialize FastAPI (or Flask).
- [x] **Story 3.2: Upload Endpoint**
  - Allow uploading the CSV file.
- [x] **Story 3.3: Recommendation Endpoint**
  - Return JSON response with game details.

## Epic 4: Web UI (Frontend)
**Goal:** A modern web interface for the butler.
- [x] **Story 4.1: React App Setup**
  - Initialize Vite/React project.
- [x] **Story 4.2: UI Implementation**
  - File upload zone.
  - "Recommend Me a Game" button.
  - Stylish display card for the result.

## Epic 5: Deployment
**Goal:** Deploy to a live environment.
- [ ] **Story 5.1: Dockerization**
  - Create Dockerfile for Backend and Frontend.
- [ ] **Story 5.2: Cloud Deployment**
  - Deploy to a service (e.g., Render, Railway, or VPS).