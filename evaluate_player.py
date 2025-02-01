import pandas as pd


default_path = "./player_data/player_data.csv"

def read_csv(filepath = None):
    csv_filepath = filepath
    print("Reading matchlogs")
    try:
        csv_df = pd.read_csv(csv_filepath)
        #print(csv_df)
    except FileNotFoundError:
        print(f"file not found: {filepath}.csv is missing")

    return csv_df




if __name__ == "__main__":
   print(read_csv(default_path))

   