DROP TABLE IF EXISTS side_summary;

CREATE TABLE side_summary AS
SELECT
  side,
  AVG(fair_prob) AS avg_fair_prob,
  AVG(won)       AS actual_win_rate,
  AVG(won) - AVG(fair_prob) AS calibration_gap_pp,
  COUNT(*)       AS games
FROM side_probs
GROUP BY side;