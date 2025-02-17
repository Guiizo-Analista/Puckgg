# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 07:49:14 2025

@author: Guiizo
"""

import pandas as pd
import os

# Specify the directory where the files are stored
data_folder = "C:/data"  # Folder where your league files are stored

# Loop through all files in the directory and process each one
for file_name in os.listdir(data_folder):
    if file_name.endswith("_matches_cleaned.xlsx"):  # Only process relevant files
        league_name = file_name.split("_")[0]  # Extract the league name from the file
        file_path = os.path.join(data_folder, file_name)

        # Define the output folder for each league
        league_output_folder = os.path.join(data_folder, league_name)
        os.makedirs(league_output_folder, exist_ok=True)  # Create the league folder if it doesn't exist

        # Load the Excel file into a Pandas DataFrame
        df = pd.read_excel(file_path, usecols=["Wk", "Day", "Date", "Time", "Home Team", "xG Home", "Home Score", "Away Score", "xG Away", "Away Team"])

        # Create a dictionary to store DataFrames for each team
        teams = set(df["Home Team"]).union(set(df["Away Team"]))
        team_dfs = {}

        # Loop through each team in the league
        for team in teams:
            team_df = df[(df["Home Team"] == team) | (df["Away Team"] == team)].copy()

            # Calculate goals scored for each team
            team_df["Goals Scored"] = team_df.apply(lambda row: row["Home Score"] if row["Home Team"] == team else row["Away Score"], axis=1)

            # Calculate match result (Win, Draw, Loss)
            def get_result(row, team):
                if row["Home Team"] == team:
                    if row["Home Score"] > row["Away Score"]:
                        return "Win"
                    elif row["Home Score"] < row["Away Score"]:
                        return "Loss"
                    else:
                        return "Draw"
                elif row["Away Team"] == team:
                    if row["Away Score"] > row["Home Score"]:
                        return "Win"
                    elif row["Away Score"] < row["Home Score"]:
                        return "Loss"
                    else:
                        return "Draw"
                return "Not Played"

            team_df["Match Result"] = team_df.apply(lambda row: get_result(row, team), axis=1)

            # Calculate points based on match result
            team_df["Points"] = team_df["Match Result"].map({"Win": 3, "Draw": 1, "Loss": 0})

            # Add xG calculation for each team (based on whether it's the home or away team)
            team_df["xG"] = team_df.apply(
                lambda row: row["xG Home"] if row["Home Team"] == team else (row["xG Away"] if row["Away Team"] == team else 0),
                axis=1
            )

            # Add xG Received calculation for each team (based on whether it's the home or away team)
            team_df["xG Received"] = team_df.apply(
                lambda row: row["xG Away"] if row["Home Team"] == team else (row["xG Home"] if row["Away Team"] == team else 0),
                axis=1
            )

            # Add Goals Received calculation for each team (based on whether it's the home or away team)
            team_df["Goals Received"] = team_df.apply(
                lambda row: row["Away Score"] if row["Home Team"] == team else (row["Home Score"] if row["Away Team"] == team else 0),
                axis=1
            )

            # Store the team's DataFrame in the dictionary
            team_dfs[team] = team_df

        # Save each team's DataFrame as an Excel file in the respective league folder
        for team, team_df in team_dfs.items():
            team_file_path = os.path.join(league_output_folder, f"{team}.xlsx")
            team_df.to_excel(team_file_path, index=False)

        print(f"Processed {file_name} and saved team data to {league_output_folder}")
