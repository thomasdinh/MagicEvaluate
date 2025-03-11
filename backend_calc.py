import pandas as pd
import numpy as np
import json
import os
from dotenv import load_dotenv, set_key
from datetime import datetime

default_match_log_path = "./match_data/match_data.csv"


def read_match_logs(filepath = None):
    csv_filepath = default_match_log_path if filepath is None else filepath
    #print("Reading matchlogs")
    try:
        match_df = pd.read_csv(csv_filepath)
        #clearprint(match_df)
    except FileNotFoundError:
        print("file not found: match_data.csv is missing")

    return match_df

def load_deck_results(exclude_draw=False):
    
    deck_result_json = "deck_result.json"
    
    if exclude_draw:
        deck_result_json = "deck_result_no_draw.json"
    try:

        # Load the data
        match_file = open(deck_result_json, 'r+')
        load_dotenv()

        # Get the last modified time of the file
        #last_match_date = find_date_last_entry_match_csv()
        last_modified_time = modification_date(deck_result_json)
        last_modified = datetime.fromisoformat(f'{last_modified_time}')
        print(last_modified)

        # Get the last known modified time from the .env file
        last_known_modified_time_str = os.getenv('RESULT_LAST_MODIFIED')
        # Convert the string to a datetime object
        last_known_modified_datetime = datetime.strptime(last_known_modified_time_str, "%Y-%m-%d %H:%M:%S")


        if last_known_modified_time_str is None:    
            print("Environment variable RESULT_LAST_MODIFIED is not set or loaded from .env file.")
        else:
            # Convert the string to a datetime object
            print("Last known modified time:", last_known_modified_datetime)

        #last_known_modified_datetime = datetime.fromisoformat(f'{last_known_modified_time_str}')

        if( last_modified > last_known_modified_datetime):
            print(f'The json has not been changed since the last time')
            print("found json file - loading data from json...")
            deck_result_dict = json.load(match_file)
            print("skipped calc")
            return deck_result_dict
        else:
            print(f'The json has been changed since the last time. Recalculating')
            deck_result_dict = calc_deck_results(deck_result_json, exclude_draw= exclude_draw)   
            return deck_result_dict
    except IOError:
        print("json file for analyzed match not found. creating new file")
        
    deck_result_dict = calc_deck_results(deck_result_json, exclude_draw= exclude_draw)   
    return deck_result_dict

def calc_deck_results(deck_result_json, exclude_draw=False):
    wins_key = "wins"
    losses_key = "lose"
    match_df = read_match_logs()
    deck_result_dict = {}

    match_deck_lists = match_df['Decklist'].values
    match_deck_results = match_df['match_result'].values
    for decks, results in zip(match_deck_lists, match_deck_results):
        participated_decks = [deck.strip().lower() for deck in decks.strip().split(",")]
        match_result = [int(x) for x in results.split(",")]
        
        if exclude_draw and find_draw(match_result):
                continue  # Skip the rest of the loop for this match
        
        for deck in participated_decks:
            
            if deck not in deck_result_dict:
                deck_result_dict[deck] = {wins_key: 0, losses_key: 0}

            deck_result_dict[deck][wins_key] += did_deck_win_result(participated_decks, match_result, deck)
            deck_result_dict[deck][losses_key] += did_deck_lose_result(participated_decks, match_result, deck)
        
    with open(deck_result_json, 'w') as fp:
        json.dump(deck_result_dict, fp, indent=4)    
    return deck_result_dict

def convert_str_to_date(date):
    try:
        date_object = datetime.strptime(date, "%d.%m.%y")
        print(date_object)
        return date_object
    except ValueError:
        print("Invalid date format.")

def did_deck_win_result(deck_list, match_result , deckname):
    for i in range(len(deck_list)):
        if deckname == deck_list[i]:
            return match_result[i]
    return 0

def did_deck_lose_result(deck_list, match_result, deckname):
    for i in range(len(deck_list)):
        if deckname == deck_list[i]:
            return 1 - match_result[i] 
    return 0

def find_draw(match_result):
    occurrence = match_result.count(1)
    if occurrence > 2:
        return True
    return False

def find_date_last_entry_match_csv(csv_file = None):
    match_df = read_match_logs(csv_file)
    match_dates = match_df['date'].values
    return match_dates[-1]



win_rates = {}

def find_best_decks(min_matches=3, top_placements=1,exclude_draw = False):
    win_rates = {}
    top_deck_dict = load_deck_results(exclude_draw=exclude_draw)

    # Calculate win rates for players with at least `min_matches` games
    for deck, result in top_deck_dict.items():
        wins = result['wins']
        losses = result['lose']
        total_games = wins + losses

        if total_games >= min_matches:
            win_rate = (wins / total_games) * 100 if total_games > 0 else 0
            win_rates[deck] = win_rate

    # Sort the dictionary by win rate in descending order
    sorted_win_rates = dict(sorted(win_rates.items(), key=lambda item: item[1], reverse=True))

    # Prepare the results string
    results = f"Top {top_placements} decks by win rate:\n"
    top_decks_list = list(sorted_win_rates.items())[:top_placements]

    for deck, win_rate in top_decks_list:
        deck_info = f'Deck: {deck.capitalize().ljust(18)} WR: {win_rate:.2f}%'
        print(deck_info)
        results += deck_info + '\n'

    return results


def read_json_file(filepath):
    try:
        with open(filepath) as json_file:
            json_data = json.load(json_file)
            print("json_data")
            return json_data
    except:
        print(f"No File found with name: {filepath}!")

# https://stackoverflow.com/questions/237079/how-do-i-get-file-creation-and-modification-date-times    
def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.fromtimestamp(t)

if __name__ == "__main__":
    print(convert_str_to_date("03.03.25"))
    read_json_file("deck_result.json")
    find_best_decks(3,40,True)