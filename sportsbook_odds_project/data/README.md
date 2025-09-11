# Data

This folder contains CSV outputs from the SQL scripts.  

## Files
- `nba_2008-2025_raw.csv` – original Kaggle dataset (seasons 2007–2025).
- `games.csv` – cleaned game-level table with odds and results (intermediate).  
- `game_analyze.csv` – enriched table with implied probs, overround, fair probs, and outcomes.  
- `nba_games_clean.csv`: game-level dataset (moneylines, implied probs, overround, fair probs, outcomes).  
- `season_summary.csv`:season aggregates (avg margin, win rate, counts).  
- `side_probs.csv`: one row per team per game (raw + fair probs, outcome).  
- `side_summary.csv`: home vs away averages (predicted vs actual, calibration gap, games).  
- `calibration_check.csv`: bin-level calibration (predicted, actual, gap, counts).  

## Notes
- Original raw dataset was the [NBA Betting Data (2007–2025) on Kaggle](https://www.kaggle.com/).  
- All CSVs here come from running the SQL scripts in `/sql`.  
- These CSVs were used directly in Power BI (see `/dashboard`). 
