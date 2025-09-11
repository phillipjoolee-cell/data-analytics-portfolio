# SQL Scripts

This folder contains all SQL transformations from raw Kaggle data → clean analysis tables.  

## Scripts
- `01_nba_games_cleaned.sql`  
  - Builds `games` from raw CSV.  
  - Creates `game_analyze` view (implied probs, overround, fair probs, win flag).  
  - Exports to `nba_games_clean`.  

- `02_season_summary.sql`  
  - Aggregates by season.  
  - Calculates average margin, win rate, game counts.  
  - Exports `season_summary.csv`.  

- `03_side_prob.sql`  
  - Flattens each game into two rows (home/away).  
  - Adds raw/fair probs and outcome.  
  - Exports `side_probs.csv`.  

- `04_side_summary.sql`  
  - Summarizes Home vs Away (predicted vs actual, calibration gap).  
  - Exports `side_summary.csv`.  

- `05_calibration_check.sql`  
  - Groups sides into probability bins (0.0, 0.1, …, 1.0).  
  - Outputs predicted, actual, calibration gap, and counts.  
  - Exports `calibration_check.csv`.  

## How to Run
1. Import the Kaggle raw dataset into SQLite (or another SQL engine).  
2. Run scripts 01 - 05 in order.  
3. Export resulting tables to CSV and place them in `/data`.  
