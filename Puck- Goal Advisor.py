# -*- coding: utf-8 -*-
"""
Created on Sun Mar  2 05:40:17 2025

@author: Guiizo
"""

import requests
import pandas as pd
import time

# Replace with your actual API key from Football-Data.org
API_KEY = '4987c2b6b9cc481e83e588f7cf3669f5'

# Define the base URL for the API endpoint
BASE_URL = 'https://api.football-data.org/v4/matches'

# Define headers with the API key
headers = {
    'X-Auth-Token': API_KEY
}

# List of teams you want to follow
teams_to_follow = ['Bologna FC 1909', 'AC Milan', 'Inter Milan']  # Example: You can add more teams here

# Function to fetch live matches data for Serie A, Bundesliga, and Premier League
def get_live_matches():
    try:
        # Make the request to the API for live matches
        response = requests.get(BASE_URL, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            
            # Check if there are live matches
            if 'matches' in data and data['matches']:
                for match in data['matches']:
                    home_team = match['homeTeam']['name']
                    away_team = match['awayTeam']['name']
                    status = match['status']
                    score_home = match['score']['fullTime']['home']
                    score_away = match['score']['fullTime']['away']

                    # Check if either home or away team is in the list of teams to follow
                    if home_team in teams_to_follow or away_team in teams_to_follow:
                        home_score_display = f"{home_team} {score_home}" if score_home is not None else f"{home_team} 0"
                        away_score_display = f"{away_team} {score_away}" if score_away is not None else f"{away_team} 0"

                        # Check if the score has changed (i.e., a goal was scored)
                        if score_home != match.get('previous_score', {}).get('home', score_home) or \
                           score_away != match.get('previous_score', {}).get('away', score_away):
                            # Save the current score for future comparison
                            match['previous_score'] = {'home': score_home, 'away': score_away}
                            
                            # Notify the user when a goal is scored
                            print(f"Goal Scored! {home_score_display} vs {away_score_display}")
                            print(f"Status: {status}")
                            print("=" * 30)

                        else:
                            print(f"{home_score_display} vs {away_score_display}")
                            print(f"Status: {status}")

            else:
                print("No live matches at the moment.")
        else:
            print(f"Error: Unable to fetch data (Status Code: {response.status_code})")
    
    except requests.exceptions.RequestException as e:
        # Handle any errors that occur during the request
        print(f"Error: An exception occurred: {e}")
    
# Function to keep checking the live matches for updates
def monitor_live_scores():
    while True:
        get_live_matches()  # Fetch and process live matches
        time.sleep(60)  # Wait for 1 minute before checking again (can be adjusted)

# Start monitoring live scores
monitor_live_scores()

