# -*- coding: utf-8 -*-
"""
Created on Sun Mar  2 06:02:27 2025

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

        # Initialize a dictionary to hold the classification data for each team
        classification_data = []

        # Loop through each team in the league
        for team in teams:
            team_df = df[(df["Home Team"] == team) | (df["Away Team"] == team)].copy()

            # Calculate goals scored for each team
            team_df["Goals Scored"] = team_df.apply(lambda row: row["Home Score"] if row["Home Team"] == team else row["Away Score"], axis=1)

            # Calculate goals received for each team
            team_df["Goals Received"] = team_df.apply(lambda row: row["Away Score"] if row["Home Team"] == team else row["Home Score"], axis=1)

            # Calculate xG for each team (based on whether it's the home or away team)
            team_df["xG"] = team_df.apply(
                lambda row: row["xG Home"] if row["Home Team"] == team else (row["xG Away"] if row["Away Team"] == team else 0),
                axis=1
            )

            # Calculate xG Received for each team (based on whether it's the home or away team)
            team_df["xG Received"] = team_df.apply(
                lambda row: row["xG Away"] if row["Home Team"] == team else (row["xG Home"] if row["Away Team"] == team else 0),
                axis=1
            )

            # Only calculate match result for games that have a score (exclude games not played)
            team_df["Match Result"] = team_df.apply(
                lambda row: "Win" if (row["Home Score"] > row["Away Score"] and row["Home Team"] == team) or
                            (row["Away Score"] > row["Home Score"] and row["Away Team"] == team) else
                            ("Draw" if row["Home Score"] == row["Away Score"] else "Not Played"),
                axis=1
            )

            # Calculate points based on match result, exclude "Not Played" games
            team_df["Points"] = team_df["Match Result"].apply(lambda result: 3 if result == "Win" else (1 if result == "Draw" else 0))

            # Sum the totals for the team, excluding "Not Played" games
            total_goals_scored = team_df["Goals Scored"].sum()
            total_goals_received = team_df["Goals Received"].sum()
            total_xg = team_df["xG"].sum()
            total_xg_received = team_df["xG Received"].sum()
            total_points = team_df["Points"].sum()

            # Add classification data (team, points, goals scored, goals received, xG, xG received)
            classification_data.append({
                "Team": team,
                "Points": total_points,
                "Goals Scored": total_goals_scored,
                "Goals Received": total_goals_received,
                "xG": total_xg,
                "xG Received": total_xg_received
            })

            # Store the team's DataFrame in the dictionary
            team_dfs[team] = team_df

        # Convert the classification data into a DataFrame and sort by points
        classification_df = pd.DataFrame(classification_data)
        classification_df = classification_df.sort_values(by=["Points", "Goals Scored"], ascending=False).reset_index(drop=True)

        # Save the classification table to an Excel file
        classification_file_path = os.path.join(league_output_folder, "Classification.xlsx")
        classification_df.to_excel(classification_file_path, index=False)

        # Save each team's DataFrame as an Excel file in the respective league folder
        for team, team_df in team_dfs.items():
            team_file_path = os.path.join(league_output_folder, f"{team}.xlsx")
            team_df.to_excel(team_file_path, index=False)

        print(f"Processed {file_name} and saved team data and classification table to {league_output_folder}")

