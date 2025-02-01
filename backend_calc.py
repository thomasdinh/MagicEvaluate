import pandas as pd
import numpy as np

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

def top_deck_wr(ranks = 1, exclude_draw = False):
    match_df = read_match_logs()
    selected_col = ['Decklist','match_result']
    match_results = match_df[selected_col]
    first_data = match_results.values[0][0]
    print(first_data)
    return 0

if __name__ == "__main__":
    top_deck_wr()