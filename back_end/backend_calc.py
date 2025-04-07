import os
import json
import logging
import csv
from datetime import datetime
from typing import Optional, Dict, Any

import pandas as pd
import requests
from dotenv import load_dotenv, set_key
from match_log import generate_match_result

# Configure logging
logging.basicConfig(level=logging.INFO)

# Constants
DEFAULT_MATCH_LOG_PATH = "../match_data/match_data.csv"
DECK_RESULT_JSON = "deck_result.json"
DECK_RESULT_NO_DRAW_JSON = "deck_result_no_draw.json"
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"

def read_match_logs(filepath: Optional[str] = None) -> Optional[pd.DataFrame]:
    """Read match logs from a CSV file."""
    csv_filepath = filepath or DEFAULT_MATCH_LOG_PATH
    try:
        return pd.read_csv(csv_filepath)
    except FileNotFoundError:
        logging.error("File not found: %s", csv_filepath)
        return None

def load_deck_results(exclude_draw: bool = False) -> Dict[str, Dict[str, int]]:
    """Load deck results from a JSON file or recalculate if the match data has been modified."""
    deck_result_json = DECK_RESULT_NO_DRAW_JSON if exclude_draw else DECK_RESULT_JSON
    last_modified_datetime = modification_date(DEFAULT_MATCH_LOG_PATH)

    load_dotenv()
    last_known_modified_time_str = os.getenv('RESULT_LAST_MODIFIED')
    last_known_modified_datetime = datetime.strptime(last_known_modified_time_str, DATE_FORMAT) if last_known_modified_time_str else datetime.min

    if last_modified_datetime <= last_known_modified_datetime:
        logging.info("Match data has not been modified. Loading from JSON.")
        return load_json_file(deck_result_json)

    logging.info("Match data has been modified. Recalculating results.")
    deck_result_dict = calc_deck_results(deck_result_json, exclude_draw)
    update_last_modified_time(last_modified_datetime)
    return deck_result_dict

def calc_deck_results(deck_result_json: str, exclude_draw: bool = False) -> Dict[str, Dict[str, int]]:
    """Calculate deck results and save to a JSON file."""
    match_df = read_match_logs()
    if match_df is None:
        return {}

    deck_result_dict = process_match_results(match_df, exclude_draw)
    save_json_file(deck_result_json, deck_result_dict)
    return deck_result_dict

def strip_brackets(result: str) -> str:
    """Strip brackets from the match result string."""
    return result.strip('[]')

def process_match_results(match_df: pd.DataFrame, exclude_draw: bool) -> Dict[str, Dict[str, int]]:
    """Process match results to calculate wins and losses for each deck."""
    deck_result_dict = {}
    for decks, results in zip(match_df['Decklist'], match_df['match_result']):
        participated_decks = [deck.strip().lower() for deck in decks.split(",")]
        stripped_results = strip_brackets(results)
        match_result = list(map(int, stripped_results.split(",")))

        if exclude_draw and find_draw(match_result):
            continue

        for deck in participated_decks:
            if deck not in deck_result_dict:
                deck_result_dict[deck] = {"wins": 0, "lose": 0}

            deck_result_dict[deck]["wins"] += did_deck_win_result(participated_decks, match_result, deck)
            deck_result_dict[deck]["lose"] += did_deck_lose_result(participated_decks, match_result, deck)

    return deck_result_dict

def did_deck_win_result(deck_list: list, match_result: list, deckname: str) -> int:
    """Determine if a deck won the match."""
    for i, deck in enumerate(deck_list):
        if deckname == deck:
            return match_result[i]
    return 0

def did_deck_lose_result(deck_list: list, match_result: list, deckname: str) -> int:
    """Determine if a deck lost the match."""
    for i, deck in enumerate(deck_list):
        if deckname == deck:
            return 1 - match_result[i]
    return 0

def find_draw(match_result: list) -> bool:
    """Check if the match result indicates a draw."""
    return match_result.count(1) > 2

def modification_date(filename: str) -> datetime:
    """Get the last modification date of a file."""
    return datetime.fromtimestamp(os.path.getmtime(filename))

def load_json_file(filepath: str) -> Optional[Dict[str, Any]]:
    """Load data from a JSON file."""
    try:
        with open(filepath, 'r') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        logging.error("No file found with name: %s", filepath)
        return None

def save_json_file(filepath: str, data: Dict[str, Any]) -> None:
    """Save data to a JSON file."""
    with open(filepath, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def update_last_modified_time(last_modified_datetime: datetime) -> None:
    """Update the last modified time in the environment variables."""
    os.environ['RESULT_LAST_MODIFIED'] = last_modified_datetime.isoformat()
    set_key('.env', 'RESULT_LAST_MODIFIED', last_modified_datetime.isoformat())

def get_all_decks() -> Dict[str, Dict[str, int]]:
    """Get all decks and their results."""
    result = load_json_file(DECK_RESULT_JSON)
    if result is None:
        logging.info("Calculating win rates.")
        load_deck_results(False)
        result = load_json_file(DECK_RESULT_JSON)
    logging.info(result)
    return result

def get_art_crop_url(card_name: str) -> str:
    """Get the art crop URL for a card from the Scryfall API."""
    url = f"https://api.scryfall.com/cards/search?q={card_name}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data['data']:
            card = data['data'][0]
            if 'image_uris' in card:
                return card['image_uris'].get('art_crop')
            if 'card_faces' in card:
                for face in card['card_faces']:
                    if 'image_uris' in face:
                        return face['image_uris'].get('art_crop')
            return "Art crop URL not found for this card."
        return "No cards found with that name."
    return f"Error: Unable to fetch data (Status code: {response.status_code})"

def count_lines_file(file_path: str) -> int:
    """Count the number of lines in a file."""
    with open(file_path, 'r') as file:
        return sum(1 for _ in file)

def append_row_to_csv(file_path: str, row: list) -> None:
    """Append a row to a CSV file."""
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(row)

def get_current_date() -> str:
    """Get the current date in the format DD.MM.YY."""
    return datetime.now().strftime("%d.%m.%y")

def add_match(decklist: str, result: Optional[int] = None, filepath: Optional[str] = None, group_id: int = 0) -> None:
    """Add a new match to the CSV file."""
    decks = [deck.strip() for deck in decklist.split(',')]
    if not decks:
        logging.error("No Decklist found!")
        return

    decks_count = len(decks)
    match_result = generate_match_result(decks_count) if result is None else result
    csv_filepath = filepath or DEFAULT_MATCH_LOG_PATH
    date = get_current_date()

    try:
        id = count_lines_file(csv_filepath)
        new_match_entry = [id, decklist, match_result, date, group_id, ""]
        append_row_to_csv(csv_filepath, new_match_entry)
        logging.info(f"Added Match to group_id {group_id}")
    except FileNotFoundError:
        logging.error("File not found: %s", csv_filepath)

def find_top_deck(top_rank = 3,min_matches = 3) -> str:
    decks= []
    deck_data = get_all_decks()
    for name, stats in deck_data.items():
        wins = stats['wins']
        lose = stats['lose']
        total_games = wins + lose

        if total_games < min_matches:
            continue

        winrate = (wins / total_games) * 100 if total_games > 0 else 0

        deck_info = {
            'name' : name,
            'wins' : wins,
            'loses': lose,
            'winrate': winrate,
            'total matches': total_games
        }
        decks.append(deck_info)
    
    sorted_decks = sorted(decks, key=lambda x: x['winrate'], reverse=True)
    top_decks_string = "\n".join(
        f"Name: {deck['name'].ljust(30)} Winrate: {deck['winrate']:.2f}%"
        for deck in sorted_decks[:top_rank]
    )

    return top_decks_string


if __name__ == "__main__":
    load_deck_results(False)
    
