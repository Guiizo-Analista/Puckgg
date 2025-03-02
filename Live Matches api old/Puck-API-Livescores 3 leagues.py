# -*- coding: utf-8 -*-
"""
Created on Sun Mar  2 05:30:11 2025

@author: Guiizo
"""

import requests
import json

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
        
        # Print raw data for debugging (optional)
        # print(json.dumps(data, indent=4))
        
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
                        
                        # Handling match statuses
                        if status == 'LIVE' or status == 'FINISHED':
                            # Display score if available
                            score_home = match['score']['fullTime']['home']
                            score_away = match['score']['fullTime']['away']
                            print(f"{home_team} vs {away_team}")
                            print(f"Score: {score_home}-{score_away}")
                        elif status == 'IN_PLAY':
                            # If the match is in play, display message about the match being live
                            print(f"{home_team} vs {away_team}")
                            print(f"Status: {status} (Match is live, score: {match['score']['fullTime']['home']}-{match['score']['fullTime']['away']})")
                        else:
                            print(f"{home_team} vs {away_team}")
                            print(f"Status: {status} (Match has not started yet)")
                        
                        print("="*30)
                    except KeyError as e:
                        print(f"Error accessing match data: {e}")
                        continue
        else:
            print("No live matches at the moment.")
    else:
        print(f"Error: Unable to fetch data (Status Code: {response.status_code})")

# Call the function to fetch live Serie A, Bundesliga, and Premier League matches
get_live_matches()
