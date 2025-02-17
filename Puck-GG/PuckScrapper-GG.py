# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 02:01:25 2025

@author: Guiizo
"""

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import os
import time

# Create the directory if it doesn't exist
save_directory = 'C:/data'
os.makedirs(save_directory, exist_ok=True)

# Function to convert values safely to float
def safe_float(value):
    try:
        return float(value)
    except ValueError:
        return None  # Return None if conversion fails

# Function to scrape match data from a given URL
def scrape_league_data(league_name, league_url):
    # Request the league page
    data = requests.get(league_url)
    soup = bs(data.text, 'lxml')

    # Find the relevant table with class 'stats_table'
    schedule_table = soup.find('table', {'class': 'stats_table'})

    # Check if table exists
    if not schedule_table:
        print(f"Could not find table for {league_name}")
        return

    # Extract data from rows of the table, skipping the header
    rows = schedule_table.find_all('tr')[1:]  # Skip the header row

    # List to store match data
    matches = []

    for row in rows:
        cells = row.find_all(['th', 'td'])  # Include both header and data cells
        if len(cells) >= 9:  # Ensure there are at least 9 valid columns
            wk = pd.to_numeric(cells[0].get_text(), errors='coerce')
            day = cells[1].get_text().strip()
            date = cells[2].get_text().strip()
            time = cells[3].get_text().strip()
            home_team = cells[4].get_text().strip()

            # Ensure xG values are correctly parsed as floats
            xg_home = safe_float(cells[5].get_text().strip())  
            xg_away = safe_float(cells[7].get_text().strip())  

            # Extract and split score
            score = cells[6].get_text().strip()
            if '–' in score:  # Ensure valid score format
                try:
                    home_score, away_score = map(int, score.split('–'))
                except ValueError:
                    home_score, away_score = None, None  # Handle missing or invalid scores
            else:
                home_score, away_score = None, None  # Handle missing scores
            
            away_team = cells[8].get_text().strip()

            # Append the cleaned data to the matches list
            matches.append({
                'Wk': wk,
                'Day': day,
                'Date': date,
                'Time': time,
                'Home Team': home_team,
                'xG Home': xg_home,   # Converted to float safely
                'Home Score': home_score,  # Converted to int
                'Away Score': away_score,  # Converted to int
                'xG Away': xg_away,   # Converted to float safely
                'Away Team': away_team
            })

    # Convert the list of matches to a DataFrame
    df_matches = pd.DataFrame(matches)

    # Check if DataFrame is empty before saving
    if df_matches.empty:
        print(f"No match data found for {league_name}")
        return

    # Save cleaned DataFrame to Excel
    output_path = os.path.join(save_directory, f'{league_name}_matches_cleaned.xlsx')
    df_matches.to_excel(output_path, index=False, engine='openpyxl')

    print(f"Cleaned data for {league_name} successfully saved to {output_path}")

# List of leagues and their URLs
leagues = {
    'MLS': 'https://fbref.com/en/comps/22/schedule/Major-League-Soccer-Scores-and-Fixtures',
    'La Liga': 'https://fbref.com/en/comps/12/schedule/La-Liga-Scores-and-Fixtures',
    'Premier League': 'https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures',
    'Bundesliga': 'https://fbref.com/en/comps/20/schedule/Bundesliga-Scores-and-Fixtures',
    'Ligue 1': 'https://fbref.com/en/comps/13/schedule/Ligue-1-Scores-and-Fixtures',
    'Serie A': 'https://fbref.com/en/comps/11/schedule/Serie-A-Scores-and-Fixtures'
}

# Loop through each league and scrape the data
for league_name, league_url in leagues.items():
    print(f"Scraping data for {league_name}...")
    scrape_league_data(league_name, league_url)

    # Add a delay between requests to avoid getting blocked
    time.sleep(5)

