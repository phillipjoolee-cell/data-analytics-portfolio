# Sportsbook SQL & Power BI – NBA Odds Analysis (2007–2025)

This project is me showing that I can actually work with SQL and Power BI using real data instead of just talking about it. I used an NBA betting dataset (October 2007 – June 2025) with game results, moneyline odds, spreads, and totals. The point wasn’t to build the craziest or most complicated pipeline, but to prove I can load raw sports betting data, clean it, transform it in SQL, and then visualize the results in Power BI.  

At the end of the day, this project is simple: I wanted to see how well sportsbook moneylines lined up with reality. Do their “implied probabilities” actually match what happens on the court? How big is the vig/overround (the book’s margin) year to year? And are home teams really priced correctly?  

## What I built

### SQL
- **Table building**: I took the raw CSV from Kaggle and structured it into a proper `games` table. I only kept games that had both home and away moneyline odds.  
- **Game analysis view (`game_analyze`)**:  Added all the important calculations:
  - Implied probability from American odds  
  - Overround (the vig, showing book margin)  
  - De-vigged fair probabilities (normalize to sum = 1)  
  - Outcome flag (did the home team win?)  
- **Export table (`nba_games_clean`)**: A flat table with everything in one place so it’s easy to analyze or move to BI.  
- **Season summary (`season_summary`)**: Aggregated overround, average probabilities, win rates, and game counts per season.  
- **Side-level table (`side_probs`)**: Broke it down to one row per team per game, so I could compare predicted fair probability vs actual outcome.

### Power BI
I didn’t just want numbers on a SQL console, I built a dashboard to tell the story visually:
1. **Executive Summary**: Trends in overround (margin) and home win rate over the years.  
2. **Calibration Page**: Compared predicted fair probabilities vs actual win rates in bins. This basically shows if the market was “honest” about how often teams should win.  
3. **Game/Team Drilldown**: A table you can filter by season or team to see the actual odds, probabilities, and outcomes for individual games.  


## Findings
- The average overround (vig) across seasons sits around X–Y% (varies by year). That’s the book’s edge.  
- Home teams won roughly Z% of the time, and the fair probabilities lined up decently with those outcomes — sportsbooks are generally well-calibrated.  
- When I binned probabilities (e.g., games where a side had a 60% chance), the actual win rates were pretty close. The market was not perfect, but close enough to show efficiency.  

## Connection
I didn’t set out to reinvent sports analytics here. My goal was to prove I can:
- Take a messy real-world dataset (not just fake data I made up).  
- Transform and enrich it entirely in SQL, not just in Python/pandas.  
- Push it into Power BI and make it digestible in a dashboard.  

It’s one thing to “know SQL” and another to show that you can run queries, check assumptions, export clean tables, and then communicate insights in a BI tool. This project is me doing exactly that.
