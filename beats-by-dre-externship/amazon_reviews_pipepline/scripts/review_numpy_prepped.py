import numpy as np
import pandas as pd

INPUT_XLSX = "Beats_Scraped_Data_Cleaned.xlsx"   # must be in the same folder
SHEET_NAME = "CLEANED_DATA"
OUT_XLSX   = "Beats_Scraped_Data_NumPy_Prepped.xlsx"
OUT_CSV    = "Beats_Scraped_Data_NumPy_Prepped.csv"

df = pd.read_excel(INPUT_XLSX, sheet_name=SHEET_NAME)

# Try exact names first (simplest)
rating_col = "Rating" if "Rating" in df.columns else None
text_col   = "Review" if "Review" in df.columns else None

# Minimal fallback: pick the first column whose lowercase string contains a keyword
def _pick(cols, keywords):
    for c in cols:
        lc = str(c).lower()
        for k in keywords:
            if k in lc:
                return c
    return None

if rating_col is None:
    rating_col = _pick(df.columns, ["rating", "stars"])
if text_col is None:
    text_col = _pick(df.columns, ["review", "content", "body", "text"])

if rating_col is None:
    raise ValueError("Could not find a rating column. Expected 'Rating' or something like it.")

ratings = pd.to_numeric(df[rating_col], errors="coerce").to_numpy()
mean_rating = np.nanmean(ratings)
ratings = np.where(np.isnan(ratings), mean_rating, ratings)

mask_valid = (ratings >= 0) & (ratings <= 5)
df = df.loc[mask_valid].copy()
ratings = ratings[mask_valid]

if text_col is not None and text_col in df.columns:
    # convert to string safely; count words; treat NaN/"nan" as 0-length
    reviews = df[text_col].astype(str).to_numpy()
    review_lengths = np.array([len(x.split()) if x and x.lower() != "nan" else 0 for x in reviews])
    df["review_length_words"] = review_lengths

rmin, rmax = np.min(ratings), np.max(ratings)
den = (rmax - rmin) if (rmax - rmin) != 0 else 1.0
df[rating_col] = ratings.astype(float)
df["rating_norm_0_1"] = (ratings - rmin) / den

df.to_excel(OUT_XLSX, index=False)
df.to_csv(OUT_CSV, index=False)

print("NumPy prep complete")
print("Saved:", OUT_XLSX, "and", OUT_CSV)
print(f"Columns present: {list(df.columns)}")
print(f"Rows after cleaning: {len(df)}")
