# -*- coding: utf-8 -*-
"""
Created on Sun Mar  2 05:33:45 2025

@author: Guiizo
"""

import requests
import pandas as pd

# Replace with your actual API key from Football-Data.org
API_KEY = '4987c2b6b9cc481e83e588f7cf3669f5'

# Define the base URL for the API endpoint
BASE_URL = 'https://api.football-data.org/v4/matches'

# Define headers with the API key
headers = {
    'X-Auth-Token': API_KEY
}

# Function to fetch live matches data for Serie A, Bundesliga, and Premier League
def get_live_matches():
    # Make the request to the API for live matches
    response = requests.get(BASE_URL, headers=headers)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        
        # Initialize an empty list to store the match data
        match_data = []

        # Check if there are live matches
        if 'matches' in data and data['matches']:
            print("Live Matches (Serie A, Bundesliga, Premier League):")
            for match in data['matches']:
                # Check if the match is part of Serie A (2019), Bundesliga (2002), or Premier League (2021)
                if match['competition']['id'] in [2019, 2002, 2021]:
                    try:
                        home_team = match['homeTeam']['name']
                        away_team = match['awayTeam']['name']
                        status = match['status']
                        score_home = match['score']['fullTime']['home']
                        score_away = match['score']['fullTime']['away']
                        
                        # Format the score with team names
                        home_score_display = f"{home_team} {score_home}" if score_home is not None else f"{home_team} 0"
                        away_score_display = f"{away_team} {score_away}" if score_away is not None else f"{away_team} 0"

                        # Append match information to the list
                        match_data.append({
                            'Home Team': home_score_display,
                            'Away Team': away_score_display,
                            'Status': status
                        })

                        # Print match info
                        print(f"{home_score_display} vs {away_score_display}")
                        print(f"Status: {status} (Score: {home_score_display}-{away_score_display})")
                        print("="*30)

                    except KeyError as e:
                        print(f"Error accessing match data: {e}")
                        continue
        else:
            print("No live matches at the moment.")
        
        # If there is match data, convert it to a DataFrame
        if match_data:
            df = pd.DataFrame(match_data)
            # Save DataFrame to Excel
            df.to_excel('live_matches_with_teams.xlsx', index=False)
            print(f"Live match data saved to 'live_matches_with_teams.xlsx'.")

    else:
        print(f"Error: Unable to fetch data (Status Code: {response.status_code})")

# Call the function to fetch live Serie A, Bundesliga, and Premier League matches
get_live_matches()

