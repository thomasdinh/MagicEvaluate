import pandas as pd
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from match_log import match_log


app = FastAPI()

match_logs = []
default_group_id = 0

class MatchLogModel(BaseModel):
    decklist: List[str]
    match_result: List[int]
    group_id: int
    match_id: int


@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/get_best_wr_deck")
def calc_best_wr_deck():
    return{"deck": "Edgar Markov"}


@app.post("/add_match_log")
def add_match_log(match_log: BaseModel):
    match_logs.append(match_log)
    return match_logs

@app.delete("/reset_match_log")
def add_match_log():
    match_logs.clear()
    return match_logs

def get_best_wr_deck(top_ranks, group_id = None):
    return "My deck"