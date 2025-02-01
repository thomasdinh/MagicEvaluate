import pandas as pd
import numpy as np

default_match_log_path = "./match_data/match_data.csv"
match_df = []

def read_match_logs(filepath = None):
    csv_filepath = default_match_log_path if filepath is None else filepath
    print("Reading matchlogs")
    try:
        match_df = pd.read_csv(csv_filepath)
        print(match_df)
    except FileNotFoundError:
        print("file not found: match_data.csv is missing")

    return 0

def top_deck_wr(ranks = 1, exclude_draw = False):
    return

if __name__ == "__main__":
    read_match_logs()