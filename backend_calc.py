import pandas as pd
import numpy as np
import json

default_match_log_path = "./match_data/match_data.csv"
top_wr_dic = {}
top_wr_decklist = []


def read_match_logs(filepath = None):
    csv_filepath = default_match_log_path if filepath is None else filepath
    #print("Reading matchlogs")
    try:
        match_df = pd.read_csv(csv_filepath)
        #clearprint(match_df)
    except FileNotFoundError:
        print("file not found: match_data.csv is missing")

    return match_df

def calc_deck_wr( exclude_draw = False):
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
      
    # print(wr_dict)
    return wr_dict


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

win_rates = {}

def find_best_decks(least_matches = 3, top_placements = 1):
    results = ''
    wr_dict = calc_deck_wr()
    for player, result in wr_dict.items():
        wins = result['wins']
        lose = result['lose']
        total_games = wins + lose
        if total_games == 0:
            win_rate = 0
        else:
            win_rate = wins/total_games
        if total_games >= least_matches:
            win_rates[player] = win_rate *100
        # Print the win rates
    # Sort the dictionary by win rate in descending order   
    sorted_win_rates = dict(sorted(win_rates.items(), key=lambda item: item[1], reverse=True))
    '''for player, win_rate in sorted_win_rates.items():
        print(f"{player}: {win_rate:.2f}")
    '''
    print(f"Top {top_placements} decks by win rate:")
    top_decks_list = list(sorted_win_rates.items())[:top_placements]
    for player, win_rate in top_decks_list:
        print(f'Deck: {player}, WR: {win_rate}')
        results+=(f'Deck: {player}, WR: {win_rate}\n')
    return results


    

if __name__ == "__main__":
    find_best_decks(3,3)