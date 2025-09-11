# Sportsbook SQL & Power BI – NBA Odds Analysis (2007–2025)

This project is about actually showing SQL + Power BI skills with real data instead of just saying I know them.  
I worked with an NBA betting dataset (October 2007 – June 2025) that has game results, moneyline odds, spreads, and totals.  

The point wasn’t to overcomplicate things—it was to take raw sportsbook data, clean it, transform it entirely in SQL, and then tell the story in Power BI.

## What I wanted to find out
- Do sportsbook “implied probabilities” actually match what happens on the court?  
- How big is the vig/overround (margin) from year to year?  
- Are home teams priced correctly?

## What I built
### SQL
- **Games table (`games`)** – structured from raw CSV, filtered to games with both home & away odds.  
- **Analysis view (`game_analyze`)** – added all the important calculations:  
  - Implied probabilities from American odds  
  - Overround (vig / margin)  
  - De-vigged fair probabilities (normalize to sum = 1)  
  - Outcome flag (did the home team win?)  
- **Flat table (`nba_games_clean`)** – one place with everything for export into BI.  
- **Season summary (`season_summary`)** – aggregated margin, win rates, and counts per season.  
- **Side-level (`side_probs`)** – broke games into one row per side (home/away) to compare predicted vs actual outcomes.  
- **Side summary (`side_summary`)** – averaged calibration results for Home vs Away.  
- **Calibration (`calibration_check`, `calibration_overall`)** – bin-level and weighted calibration tables to see if markets line up with results.

### Power BI
- **Executive Summary** – trends in sportsbook margin (overround − 1) and home win rate by season.  
- **Calibration** – predicted vs actual win rates in probability bins, plus weighted overall calibration.  
- **Bookmaker Comparison / Drilldown** – interactive table of games with filters for season and team.  
  > Note: Team slicer built in Power BI (unpivoted Home/Away), not materialized in SQL.

## Main Findings
- Average margin (vig) across seasons sits around X–Y% (varies by year).  
- Home teams won roughly Z% of the time. Fair probabilities and actual results lined up decently—sportsbooks are generally well-calibrated.  
- By probability bin (e.g., “60% chance”), actual win rates came close. Markets weren’t perfect, but efficient enough.

## Why this matters
The project shows I can:
- Take a messy, real-world dataset.  
- Transform and enrich it fully in SQL (not just pandas/Python).  
- Push it into Power BI and design a dashboard that communicates clearly.  

It’s one thing to *know SQL* it’s another to build a pipeline, check assumptions, and make the outputs understandable to others. This repo is me doing exactly that.
