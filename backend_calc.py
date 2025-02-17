import pandas as pd
import numpy as np
import json

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

def calc_deck_wr(ranks = 1, exclude_draw = False):
    # You can define the 'wins' and 'lose' as strings
    wins = "wins"
    lose = "lose"
    match_df = read_match_logs()
    wr_dict = {}
    #selected_col = ['Decklist','match_result']
    match_deck_list = match_df['Decklist'].values
    match_deck_wr = match_df['match_result'].values
    for i in range(len(match_deck_list)):
        # print(f'Match {i}:\---------------------')
        # print(match_deck_list[i])
        participated_decks = [match.strip().lower() for match in match_deck_list[i].strip().split(",")]
        match_result =[int(x) for x in match_deck_wr[i].split(",")]
        for deck in participated_decks:
            
            if deck in wr_dict:
                #print(f'Update entry after Match {i}:')
                #print(f'Deck: {deck}:wr_dict[{deck}]')
                #print(wr_dict[deck])
                wr_dict[deck][wins] += did_deck_win_result(participated_decks, match_result, deck )
                wr_dict[deck][lose] += did_deck_lose_result(participated_decks, match_result, deck )
                #print(f'Updated results of Deck: {deck}')
                #print(wr_dict[deck])
            if deck not in wr_dict:
                #print(f'New entry for Deck: {deck}:wr_dict[{deck}]')
                wr_dict[deck] = {wins: did_deck_win_result(participated_decks, match_result, deck ), lose :did_deck_lose_result(participated_decks, match_result, deck ) } 
                #print(f'Updated results of Deck: {deck}:wr_dict{deck}')
                #print(wr_dict[deck])
        
    print(wr_dict)
    return 0


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

    

if __name__ == "__main__":
    calc_deck_wr()