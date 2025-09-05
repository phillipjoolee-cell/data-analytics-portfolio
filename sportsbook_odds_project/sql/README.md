# SQL Folder

This folder contains the SQL scripts used to transform the raw NBA betting data.

## Scripts
- **01_build_tables_and_view.sql**  
  - Builds the `games` table from the raw import.  
  - Creates `game_analyze` view with implied probabilities, overround, de-vig fair probabilities, and win flag.  
  - Exports everything into `nba_games_clean` for convenience.  

- **02_season_summary.sql**  
  - Aggregates by season.  
  - Calculates average overround, average fair probabilities, home win rate, and game counts.  
  - Outputs `season_summary`.  

- **03_side_probs.sql**  
  - Flattens each game into two rows (home and away).  
  - Adds probabilities (raw and fair) and the actual win/loss outcome for each side.  
  - Outputs `side_probs`.  

## How to Run
1. Import the Kaggle raw dataset into SQLite (or another SQL engine).  
2. Run `01_build_tables_and_view.sql`.  
3. Run `02_season_summary.sql`.  
4. Run `03_side_probs.sql`.  
5. Export the resulting tables to CSV and place them in `/data`.  
