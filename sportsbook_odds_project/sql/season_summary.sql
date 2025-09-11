DROP TABLE IF EXISTS season_summary;

CREATE TABLE season_summary AS
SELECT season,
       AVG(overround - 1.0) AS avg_overround,
       AVG(p_home_fair) AS avg_p_home_fair,
       AVG(home_won)    AS home_win_rate,
       COUNT(*)         AS n_games
FROM game_analyze
GROUP BY season
ORDER BY season;
