import pandas as pd
import numpy as np
import json
import os
from dotenv import load_dotenv, set_key
from datetime import datetime
from typing import Optional, Dict, Any
import logging
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)

default_match_log_path = "../match_data/match_data.csv"

def read_match_logs(filepath: Optional[str] = None) -> Optional[pd.DataFrame]:
    csv_filepath = default_match_log_path if filepath is None else filepath
    try:
        match_df = pd.read_csv(csv_filepath)
        return match_df
    except FileNotFoundError:
        logging.error("File not found: match_data.csv is missing")
        return None

def load_deck_results(exclude_draw: bool = False) -> Dict[str, Dict[str, int]]:
    deck_result_json = "deck_result_no_draw.json" if exclude_draw else "deck_result.json"

    try:
        last_modified_datetime = modification_date(default_match_log_path)
        load_dotenv()
        last_known_modified_time_str = os.getenv('RESULT_LAST_MODIFIED')

        if last_known_modified_time_str is None:
            logging.warning("Environment variable RESULT_LAST_MODIFIED is not set.")
            last_known_modified_datetime = datetime.min
        else:
            last_known_modified_datetime = datetime.strptime(last_known_modified_time_str, "%Y-%m-%d %H:%M:%S.%f")

        if last_modified_datetime <= last_known_modified_datetime:
            logging.info("Match data has not been modified. Loading from JSON.")
            with open(deck_result_json, 'r') as match_file:
                deck_result_dict = json.load(match_file)
            return deck_result_dict
        else:
            logging.info("Match data has been modified. Recalculating results.")
            deck_result_dict = calc_deck_results(deck_result_json, exclude_draw)
            os.environ['RESULT_LAST_MODIFIED'] = last_modified_datetime.isoformat()
            set_key('.env', 'RESULT_LAST_MODIFIED', last_modified_datetime.isoformat())
            return deck_result_dict
    except IOError:
        logging.error("JSON file for analyzed match not found. Creating new file.")

    return calc_deck_results(deck_result_json, exclude_draw)

def calc_deck_results(deck_result_json: str, exclude_draw: bool = False) -> Dict[str, Dict[str, int]]:
    wins_key = "wins"
    losses_key = "lose"
    match_df = read_match_logs()
    deck_result_dict = {}

    if match_df is None:
        return deck_result_dict

    match_deck_lists = match_df['Decklist'].values
    match_deck_results = match_df['match_result'].values
    for decks, results in zip(match_deck_lists, match_deck_results):
        participated_decks = [deck.strip().lower() for deck in decks.strip().split(",")]
        match_result = [int(x) for x in results.split(",")]

        if exclude_draw and find_draw(match_result):
            continue

        for deck in participated_decks:
            if deck not in deck_result_dict:
                deck_result_dict[deck] = {wins_key: 0, losses_key: 0}

            deck_result_dict[deck][wins_key] += did_deck_win_result(participated_decks, match_result, deck)
            deck_result_dict[deck][losses_key] += did_deck_lose_result(participated_decks, match_result, deck)

    with open(deck_result_json, 'w') as fp:
        json.dump(deck_result_dict, fp, indent=4)
    return deck_result_dict

def did_deck_win_result(deck_list: list, match_result: list, deckname: str) -> int:
    for i, deck in enumerate(deck_list):
        if deckname == deck:
            return match_result[i]
    return 0

def did_deck_lose_result(deck_list: list, match_result: list, deckname: str) -> int:
    for i, deck in enumerate(deck_list):
        if deckname == deck:
            return 1 - match_result[i]
    return 0

def find_draw(match_result: list) -> bool:
    return match_result.count(1) > 2

def modification_date(filename: str) -> datetime:
    t = os.path.getmtime(filename)
    return datetime.fromtimestamp(t)

def read_json_file(filepath: str) -> Optional[Dict[str, Any]]:
    try:
        with open(filepath, 'r') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        logging.error(f"No file found with name: {filepath}")
        return None

def get_all_decks() -> Dict[str, Dict[str, int]]:
    deck_result_json = "deck_result.json"
    result = read_json_file(deck_result_json)
    if result is None:
        logging.info("Calculating win rates.")
        load_deck_results(False)
        result = read_json_file(deck_result_json)
    logging.info(result)
    return result

def get_art_crop_url(card_name):
    # Scryfall API endpoint for searching cards by name
    url = f"https://api.scryfall.com/cards/search?q={card_name}"

    # Make the request to the Scryfall API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Check if there are any results
        if data['data']:
            card = data['data'][0]

            # Check if 'image_uris' is present
            if 'image_uris' in card:
                return card['image_uris'].get('art_crop')

            # Check for double-faced cards
            if 'card_faces' in card:
                for face in card['card_faces']:
                    if 'image_uris' in face:
                        return face['image_uris'].get('art_crop')

            return "Art crop URL not found for this card."
        else:
            return "No cards found with that name."
    else:
        return f"Error: Unable to fetch data (Status code: {response.status_code})"

if __name__ == "__main__":
    print(get_art_crop_url("Tinybones"))