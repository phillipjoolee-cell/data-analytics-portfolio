DROP TABLE IF EXISTS side_probs;

CREATE TABLE side_probs AS
SELECT game_id, season, date, home, away,
       'home' AS side, p_home_fair AS fair_prob, p_home_raw AS raw_prob, home_won AS won
FROM game_analyze
UNION ALL
SELECT game_id, season, date, home, away,
       'away' AS side, p_away_fair AS fair_prob, p_away_raw AS raw_prob, 1 - home_won AS won
FROM game_analyze;