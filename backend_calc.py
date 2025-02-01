import pandas as pd
import numpy as np

default_match_path = "./match_data/match_data.csv"

def read_match_logs():
    print("Reading matchlogs")
    try:
        with open ('./match_data/match_data.csv','r') as match_log_file:
            content = match_log_file.read()
            print(content)
    except FileNotFoundError:
        print("file not found")

    return 0

if __name__ == "__main__":
    read_match_logs()