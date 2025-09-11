DROP VIEW IF EXISTS game_analyze;
DROP TABLE IF EXISTS games;
DROP TABLE IF EXISTS nba_games_clean;

CREATE TABLE games AS
SELECT
  ROW_NUMBER() OVER ()         AS game_id,
  CAST(season AS INT)          AS season,
  date,
  home,
  away,
  CAST(score_home     AS INT)  AS score_home,
  CAST(score_away     AS INT)  AS score_away,
  CAST(moneyline_home AS REAL) AS moneyline_home,
  CAST(moneyline_away AS REAL) AS moneyline_away,
  CAST(spread         AS REAL) AS spread,
  CAST(total          AS REAL) AS total
FROM "nba_2008-2025_raw"
WHERE moneyline_home IS NOT NULL
  AND moneyline_away IS NOT NULL;

-- Enriched view (implied probs, vig/overround, de-vig fair probs, outcome)
CREATE VIEW game_analyze AS
SELECT
  game_id,
  season,
  date,
  home,
  away,
  score_home,
  score_away,
  spread,
  total,
  moneyline_home,
  moneyline_away,

  CASE WHEN moneyline_home > 0
       THEN 100.0 / (moneyline_home + 100.0)
       ELSE (-1.0 * moneyline_home) / ((-1.0 * moneyline_home) + 100.0)
  END AS p_home_raw,

  CASE WHEN moneyline_away > 0
       THEN 100.0 / (moneyline_away + 100.0)
       ELSE (-1.0 * moneyline_away) / ((-1.0 * moneyline_away) + 100.0)
  END AS p_away_raw,

  (CASE WHEN moneyline_home > 0
        THEN 100.0 / (moneyline_home + 100.0)
        ELSE (-1.0 * moneyline_home) / ((-1.0 * moneyline_home) + 100.0)
   END
   +
   CASE WHEN moneyline_away > 0
        THEN 100.0 / (moneyline_away + 100.0)
        ELSE (-1.0 * moneyline_away) / ((-1.0 * moneyline_away) + 100.0)
   END) AS overround,

  (CASE WHEN moneyline_home > 0
        THEN 100.0 / (moneyline_home + 100.0)
        ELSE (-1.0 * moneyline_home) / ((-1.0 * moneyline_home) + 100.0)
   END)
  /
  ((CASE WHEN moneyline_home > 0
         THEN 100.0 / (moneyline_home + 100.0)
         ELSE (-1.0 * moneyline_home) / ((-1.0 * moneyline_home) + 100.0)
    END)
   +
   (CASE WHEN moneyline_away > 0
         THEN 100.0 / (moneyline_away + 100.0)
         ELSE (-1.0 * moneyline_away) / ((-1.0 * moneyline_away) + 100.0)
    END)) AS p_home_fair,

  (CASE WHEN moneyline_away > 0
        THEN 100.0 / (moneyline_away + 100.0)
        ELSE (-1.0 * moneyline_away) / ((-1.0 * moneyline_away) + 100.0)
   END)
  /
  ((CASE WHEN moneyline_home > 0
         THEN 100.0 / (moneyline_home + 100.0)
         ELSE (-1.0 * moneyline_home) / ((-1.0 * moneyline_home) + 100.0)
    END)
   +
   (CASE WHEN moneyline_away > 0
         THEN 100.0 / (moneyline_away + 100.0)
         ELSE (-1.0 * moneyline_away) / ((-1.0 * moneyline_away) + 100.0)
    END)) AS p_away_fair,

  CASE WHEN score_home > score_away THEN 1 ELSE 0 END AS home_won
FROM games;

-- Flat export table
CREATE TABLE nba_games_clean AS
SELECT * FROM game_analyze;