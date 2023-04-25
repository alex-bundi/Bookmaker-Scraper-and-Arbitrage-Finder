from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd
import numpy as np

def main():
    parsed_data = read_data(sp_file= "sp_basketball.csv", bw_file=  "bw_basketball.csv")
    home_column = get_column(sp_data= parsed_data[0], bw_data= parsed_data[1])

    matched_teams = match_teams(dataframe_data= home_column)
    create_matched_csv(betway_df= parsed_data[1], matched_data= matched_teams)
    merge_data(df= parsed_data)

def read_data(sp_file, bw_file) -> set:
    """ Reads csv files created by the scraper files
    
        Args:
            sp_file -> generated csv file by sp_bb_scraper.py
            bw_file -> generated csv file by bw_bb_scraper.py
    """

    sp_df = pd.read_csv(sp_file)
    bw_df = pd.read_csv(bw_file)
    sp_df.drop_duplicates(subset= None, inplace= True)
    bw_df.drop_duplicates(subset= None, inplace= True)
    return sp_df, bw_df

def get_column(sp_data, bw_data) -> list:
    """ Converts home_team column into a list for both dataframes.
        
        Args:
            sp_data -> data read from the csv files
            bw_data ->  data read from the csv files

    """
        
    first_df = list(sp_data.home_team)
    second_df = list(bw_data.home_team)
    column_data = [first_df, second_df]
    return column_data

def match_teams(dataframe_data) -> list:
    """ 
    Iterates through the sportpesa home_team column and matches each
    iteration to the list of betway home_team column. It only appends
    if returned score is greater than 70
    
    Args:
        dataframe_data -> return value of get_column fuction which is a list of lists
    """
    response = []
    for teams in dataframe_data[0]:
        closest_match, score= process.extractOne(teams, dataframe_data[1]) # returns a tuple (string, score)
        if score > 70:
            row = (teams, closest_match)
            response.append(row)
    return response

def create_matched_csv(betway_df, matched_data) -> None:
    """
    Creates a csv that matches the home_team column of sp_basketball.csv to that of
    bw_basketball.csv by adding a new column i.e closest_match.
    
    Args:
        betway_df -> bw_df a pandas dataframe
        matched_data -> return value of match_teams function
    """
    betway_df["closest_match"] = "N/A" # Initialize the "closest_match" column with a default value
    for data in matched_data:
        # Update with new match if it exists else leave default value
        betway_df["closest_match"] = np.where(betway_df["home_team"] == data[1], data[0], betway_df["closest_match"])

    betway_df.to_csv("bw_basketball.csv", index=False)
    print(f"Re-write successful\n")

def merge_data(df) -> None:
    """ 
    Merges the two dataframes into then calculates the arbitrage

    Args:
        df -> pandas dataframe
    """
    merge_df = pd.merge(df[0], df[1], left_on= "home_team", right_on="closest_match")
    merge_df["1_arb"] = ((1/merge_df["ht_1_x"]) + (1/merge_df["at_2_y"]))
    merge_df["2_arb"] = ((1/merge_df["ht_1_y"]) + (1/merge_df["at_2_x"]))
    results_df = merge_df[(merge_df["1_arb"] < 1) | (merge_df["2_arb"] < 1)]
    print(results_df)

if __name__ == "__main__":
    main()
