# Data Folder

This folder contains all the data files used or exported in the project.

## Files
- **nba_games_clean.csv**: Full game-level dataset with moneyline odds, implied probabilities, overround, fair probabilities, and results.  
- **season_summary.csv**: Season-level aggregates (average overround, home win rate, average probabilities, game counts).  
- **side_probs.csv**: Side-level dataset with one row per team per game, including fair probability, raw implied probability, and actual result.  

## Notes
- Original raw dataset was the [NBA Betting Data (2007–2025) on Kaggle](https://www.kaggle.com/).  
- All CSVs in this folder come from running the SQL scripts in `/sql`.  
- Use these CSVs directly in Power BI (see `/dashboard`).  
