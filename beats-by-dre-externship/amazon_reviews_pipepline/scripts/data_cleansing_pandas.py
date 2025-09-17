import pandas as pd
import numpy as np
from pathlib import Path

INPUT_PATH = Path("Beats_Scraped_Data.csv")                # change if needed
EXCEL_OUT = Path("Beats_Scraped_Data_Cleaned.xlsx")        # output path

def to_snake(s: str) -> str:
    s = str(s).strip()
    for a,b in [("/", " "), ("-", " "), (".", " "), ("(", ""), (")", ""), ("%", " pct "), ("&", " and ")]:
        s = s.replace(a, b)
    s = " ".join(s.lower().split())
    return s.replace(" ", "_")

def find_col(cols, candidates):
    # Return the first column whose name contains any candidate substring
    for cand in candidates:
        for col in cols:
            if cand in col:
                return col
    return None

def shorten_example(val, maxlen=120):
    s = "" if val is None else str(val)
    s = " ".join(s.split())
    return (s[:maxlen] + "…") if len(s) > maxlen else s

def main():
    # 1) Load dataset
    df_raw = pd.read_csv(INPUT_PATH, encoding="utf-8", low_memory=False)
    raw_head = df_raw.head(5)

    # 2) Standardize column names
    df = df_raw.copy()
    df.columns = [to_snake(c) for c in df.columns]

    # 3) Strip text columns
    for c in df.select_dtypes(include=["object"]).columns:
        df[c] = df[c].astype(str).str.strip()

    # 4) Remove duplicates
    before_dups = len(df)
    df = df.drop_duplicates()
    dups_removed = before_dups - len(df)

    # 5) Identify key columns
    cols = list(df.columns)
    rating_col = find_col(cols, ["rating", "stars"])
    title_col = find_col(cols, ["title"])
    review_text_col = find_col(cols, ["review", "content", "body", "text"])
    date_col = find_col(cols, ["date"])
    product_col = find_col(cols, ["product", "asin", "item"])
    verified_col = find_col(cols, ["verified"])
    author_col = find_col(cols, ["author", "user", "profile"])

    # 6) Convert dtypes
    if rating_col:
        df[rating_col] = pd.to_numeric(df[rating_col], errors="coerce")
        # Normalize if out of 100 etc.
        max_rating = df[rating_col].max()
        if pd.notna(max_rating) and max_rating > 10:
            df[rating_col] = (df[rating_col] / 20.0).round(1)  # heuristic
        df[rating_col] = df[rating_col].clip(lower=1, upper=5)

    if date_col:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    if verified_col:
        df[verified_col] = (
            df[verified_col]
            .astype(str)
            .str.lower()
            .map({"true": True, "yes": True, "y": True, "1": True,
                  "false": False, "no": False, "n": False, "0": False})
        )

    # 7) Keep rows that have at least rating OR review text
    rows_before = len(df)
    mask_useful = pd.Series(False, index=df.index)
    if rating_col:
        mask_useful = mask_useful | df[rating_col].notna()
    if review_text_col:
        mask_useful = mask_useful | df[review_text_col].notna()
    df = df[mask_useful]
    removed_unuseful = rows_before - len(df)

    # 8) Fill minor missing text with "N/A" except key columns
    key_cols = {c for c in [rating_col, review_text_col, date_col, verified_col, product_col, title_col, author_col] if c}
    for c in df.columns:
        if c not in key_cols and df[c].dtype == "O":
            df[c] = df[c].replace({"nan": np.nan}).fillna("N/A")

    # 9) Helper columns
    if review_text_col:
        df["review_length_chars"] = df[review_text_col].astype(str).str.len()
    if date_col:
        df["review_year"] = df[date_col].dt.year

    # 10) Cleaning log + data dictionary
    clean_log = pd.DataFrame([
        ["Loaded rows", len(df_raw)],
        ["Columns (original)", len(df_raw.columns)],
        ["Duplicate rows removed", dups_removed],
        ["Removed rows missing both rating and review text", removed_unuseful],
        ["Final rows", len(df)],
        ["Final columns", len(df.columns)],
        ["Rating column", rating_col or "Not found"],
        ["Review text column", review_text_col or "Not found"],
        ["Date column", date_col or "Not found"],
        ["Product column", product_col or "Not found"],
        ["Verified column", verified_col or "Not found"],
    ], columns=["action", "value"])

    data_dict = pd.DataFrame({
        "column": df.columns,
        "dtype": [str(t) for t in df.dtypes],
        "example": [
            shorten_example(df[c].dropna().iloc[0]) if df[c].notna().any() else ""
            for c in df.columns
        ],
    })

    # 11) Save to Excel (pandas only)
    with pd.ExcelWriter(EXCEL_OUT) as writer:
        raw_head.to_excel(writer, sheet_name="RAW_SAMPLE", index=False)
        clean_log.to_excel(writer, sheet_name="CLEANING_LOG", index=False)
        data_dict.to_excel(writer, sheet_name="DATA_DICTIONARY", index=False)
        df.to_excel(writer, sheet_name="CLEANED_DATA", index=False)

if __name__ == "__main__":
    main()
