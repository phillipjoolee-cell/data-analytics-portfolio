DROP TABLE IF EXISTS calibration_check;

CREATE TABLE calibration_check AS
WITH binned AS (
  SELECT
    ROUND(
      CASE WHEN fair_prob < 0 THEN 0.0
           WHEN fair_prob > 1 THEN 1.0
           ELSE fair_prob END * 10.0, 0
    ) / 10.0 AS bin,
    fair_prob,
    won
  FROM side_probs
)
SELECT
  bin,
  printf('%d%%', CAST(bin * 100 AS INT)) AS bin_label,   -- e.g., '60%'
  AVG(fair_prob)                 AS predicted,
  AVG(won)                       AS actual,
  AVG(won) - AVG(fair_prob)      AS calibration_gap,     -- Actual - Predicted
  COUNT(*)                       AS n
FROM binned
GROUP BY bin
ORDER BY bin;
