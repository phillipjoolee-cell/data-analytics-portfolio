# Data
This folder contains CSV outputs from SQL scripts.

## Files
- `nba_games_cleaned.csv` – game-level dataset (moneylines, implied probs, overround, fair probs, outcomes).  
- `season_summary.csv` – season aggregates (avg margin, win rate, counts).  
- `side_probs.csv` – one row per team per game (raw + fair probs, outcome).  
- `side_summary.csv` – home vs away averages (predicted vs actual, calibration gap, games).  
- `calibration_check.csv` – bin-level calibration (predicted, actual, gap, counts).

## Notes
- Original raw dataset was the [NBA Betting Data (2007–2025) on Kaggle](https://www.kaggle.com/).  
- All CSVs in this folder come from running the SQL scripts in `/sql`.  
- Use these CSVs directly in Power BI (see `/dashboard`).  
