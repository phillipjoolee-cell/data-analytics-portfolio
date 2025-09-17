pip install xlsxwriter

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# 1: set up file paths
IN_PATH = Path("Beats_Scraped_Data_Pandas_EDA.xlsx")
CSV_OUT = Path("correlation_matrix.csv")
XLSX_OUT = Path("Beats_Scraped_Data_correlation_matrix.xlsx")
HEATMAP_PNG = Path("correlation_heatmap.png")

# 2: load the dataset
df = pd.read_excel(IN_PATH)

# 3: make sure review_length_words is numeric if it exists
if 'review_length_words' in df.columns:
    df['review_length_words'] = pd.to_numeric(df['review_length_words'], errors='coerce')

# 4: grab numeric columns that actually have data and variation
num = df.select_dtypes(include=[np.number])

non_null_counts = num.notna().sum()
nunique_counts  = num.nunique(dropna=True)

usable_cols = num.columns[(non_null_counts > 0) & (nunique_counts > 1)]

# exclude engineered duplicates like normalized ratings
EXCLUDE_FROM_CORR = {"rating_norm_0_1"}   # add more if needed
usable_cols = [c for c in usable_cols if c not in EXCLUDE_FROM_CORR]

dropped = num.columns[~num.columns.isin(usable_cols)]
if len(dropped):
    print("Excluded from correlation:", list(dropped))

if len(usable_cols) == 0:
    raise ValueError("No usable numeric columns (non-empty & non-constant) for correlation.")

# 5: build the correlation matrix
corr = num[usable_cols].corr(method="pearson")
corr.to_csv(CSV_OUT, index=True)

# 6: figure out the top absolute correlations (only take upper triangle to avoid dupes)
mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
corr_ut = corr.where(mask)

pairs = (
    corr_ut.stack()  # (row,col) -> value for upper triangle
    .rename("corr")
    .to_frame()
)
pairs["abs_corr"] = pairs["corr"].abs()
top_pairs_df = pairs.sort_values("abs_corr", ascending=False).head(10).reset_index()
top_pairs_df.columns = ["var1", "var2", "corr", "abs_corr"]

# 7: check for any "strong" correlations (|r| ≥ 0.5)
# if none, just leave a message so the sheet isn’t blank
THRESH = 0.50
sig_pairs = pairs[pairs["abs_corr"] >= THRESH].sort_values("abs_corr", ascending=False)

if sig_pairs.empty:
    sig_pairs_df = pd.DataFrame(
        [["No correlations meet the |r| ≥ 0.5 threshold", "", "", ""]],
        columns=["var1", "var2", "corr", "abs_corr"]
    )
else:
    sig_pairs_df = sig_pairs.reset_index()
    sig_pairs_df.columns = ["var1", "var2", "corr", "abs_corr"]


# 8: create a heatmap of the correlation matrix
plt.figure(figsize=(10, 8))
im = plt.imshow(corr.values, vmin=-1, vmax=1)
plt.title("Correlation Matrix Heatmap")
plt.xticks(np.arange(len(corr.columns)), corr.columns, rotation=45, ha="right")
plt.yticks(np.arange(len(corr.index)), corr.index)

for i in range(corr.shape[0]):
    for j in range(corr.shape[1]):
        plt.text(j, i, f"{corr.values[i, j]:.2f}", ha="center", va="center", fontsize=7)

plt.colorbar(im, fraction=0.046, pad=0.04)
plt.tight_layout()
plt.savefig(HEATMAP_PNG, dpi=200)
plt.close()

# 9: save everything to Excel, including the heatmap image
with pd.ExcelWriter(XLSX_OUT, engine="xlsxwriter") as writer:
    df.to_excel(writer, sheet_name="Data", index=False)
    corr.to_excel(writer, sheet_name="Correlation_Matrix", index=True)
    top_pairs_df.to_excel(writer, sheet_name="Top_Correlations", index=False)
    sig_pairs_df.to_excel(writer, sheet_name="Significant_Only", index=False)

    # add heatmap to excel
    ws = writer.book.add_worksheet("Heatmap")
    ws.insert_image("B2", str(HEATMAP_PNG))

print("Saved files:", CSV_OUT, XLSX_OUT, HEATMAP_PNG)
