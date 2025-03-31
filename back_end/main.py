
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from backend_calc import get_all_decks,get_art_crop_url, find_top_deck
from uuid import uuid4 
import httpx
import uvicorn

app = FastAPI()

match_logs = []
default_group_id = 0


class MatchLogModel(BaseModel):
    decklist: List[str]
    match_result: List[int]
    group_id: int
    match_id: int

class Deck(BaseModel):
    id: str
    name: str
    url: str
    winrate: float
    

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/get_best_wr_deck")
async def calc_best_wr_deck():
    return await find_top_deck(1,3)

@app.get("/all_decks", response_model=List[Deck])
async def all_decks():
    decks = []

    deck_data = get_all_decks()

    for name, stats in deck_data.items():
        wins = stats['wins']
        lose = stats['lose']
        total_games = wins + lose
        winrate = (wins / total_games) * 100 if total_games > 0 else 0

        # Generate a unique ID for each deck
        deck_id = str(uuid4())  # Use uuid4 to generate a unique ID

        art_url = get_art_crop_url(name)

        deck_info = {
            'id': deck_id,
            'name': name,
            'url':  art_url,
            'winrate': winrate
            
        }

        decks.append(deck_info)

    return decks


@app.post("/add_match_log")
def add_match_log(match: MatchLogModel):
    match_logs.append(match)
    return match_logs


@app.post("/matches/")
async def create_match_log(match: MatchLogModel):
    match_logs.append(match)
    return match_logs


@app.delete("/reset_match_log")
def add_match_log():
    match_logs.clear()
    return match_logs


def get_best_wr_deck(top_ranks=1, group_id=None):
    return "Load"


if __name__ == "main":
    uvicorn.run(app, host="0.0.0.0", port=8000)
