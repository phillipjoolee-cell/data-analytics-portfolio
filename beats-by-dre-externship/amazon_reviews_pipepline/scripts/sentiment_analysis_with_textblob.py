pip install xlsxwriter

import os
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
from pathlib import Path

# 1: set up file paths
IN_PATH = Path("Beats_Scraped_Data_Cleaned.xlsx")
CSV_OUT = Path("Beats_Scraped_Data_sentiment.csv")
XLSX_OUT = Path("Beats_Scraped_Data_sentiment.xlsx")
FIG_DIR = Path("figures")
FIG_DIR.mkdir(exist_ok=True)

# 2: load the dataset
if IN_PATH.suffix == ".csv":
    df = pd.read_csv(IN_PATH)
else:
    df = pd.read_excel(IN_PATH, sheet_name="CLEANED_DATA")

# 3: detect the review text column
CANDIDATES = [
    "content", "review", "review_text", "text", "body", "comment",
    "Review", "Content", "reviewText", "review_body"
]
review_col = next((c for c in CANDIDATES if c in df.columns), None)
if review_col is None:
    for c in df.columns:
        if pd.api.types.is_object_dtype(df[c]):
            review_col = c
            break
if review_col is None:
    raise ValueError("No suitable review column found.")

# drop rows where review text is empty/whitespace
df = df[df[review_col].astype(str).str.strip().ne("")]

# 4: calculate polarity and subjectivity with TextBlob
df["Polarity"] = df[review_col].astype(str).apply(lambda x: TextBlob(x).sentiment.polarity)
df["Subjectivity"] = df[review_col].astype(str).apply(lambda x: TextBlob(x).sentiment.subjectivity)

# round polarity/subjectivity for readability
df["Polarity"] = df["Polarity"].round(4)
df["Subjectivity"] = df["Subjectivity"].round(4)

# 5: categorize sentiment into Positive / Neutral / Negative
def categorize_sentiment(p):
    if p > 0.20:
        return "Positive"
    elif p < -0.20:
        return "Negative"
    else:
        return "Neutral"

df["Sentiment"] = df["Polarity"].apply(categorize_sentiment)

# 6: build a summary table
summary = (
    df["Sentiment"]
    .value_counts(dropna=False)
    .rename_axis("Sentiment")
    .to_frame("Count")
    .sort_index()
)
summary["Percentage"] = (summary["Count"] / len(df) * 100).round(2)

# 7: create visuals (histogram, scatter, bar chart)
hist_path = FIG_DIR / "polarity_hist.png"
bins = max(10, min(40, len(df) // 50))  # auto-scale bins
plt.figure()
df["Polarity"].dropna().hist(bins=bins)
plt.title("Distribution of Polarity Scores")
plt.xlabel("Polarity")
plt.ylabel("Frequency")
plt.savefig(hist_path, dpi=150, bbox_inches="tight")
plt.close()

scatter_path = FIG_DIR / "polarity_vs_subjectivity.png"
plt.figure()
plt.scatter(df["Polarity"], df["Subjectivity"], alpha=0.5)
plt.title("Polarity vs Subjectivity")
plt.xlabel("Polarity")
plt.ylabel("Subjectivity")
plt.savefig(scatter_path, dpi=150, bbox_inches="tight")
plt.close()

bar_path = FIG_DIR / "sentiment_bar.png"
plt.figure()
summary["Count"].plot(kind="bar")
plt.title("Sentiment Categories")
plt.xlabel("Sentiment")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(bar_path, dpi=150, bbox_inches="tight")
plt.close()

# 8: save results to CSV and Excel with embedded visuals
df.to_csv(CSV_OUT, index=False)

with pd.ExcelWriter(XLSX_OUT, engine="xlsxwriter") as writer:
    df.to_excel(writer, sheet_name="Data_with_Sentiment", index=False)
    summary.reset_index().to_excel(writer, sheet_name="Sentiment_Summary", index=False)

    ws = writer.book.add_worksheet("Visuals")
    ws.write("A1", "Distribution of Polarity Scores")
    ws.insert_image("A3", str(hist_path))
    ws.write("A33", "Polarity vs Subjectivity")
    ws.insert_image("A35", str(scatter_path))

# 9: done
print("Detected review column:", review_col)
print("Saved files:", CSV_OUT, XLSX_OUT, hist_path, scatter_path)
