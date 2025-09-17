!pip install -U google-generativeai

pip install xlsxwriter

#1: Paths
from pathlib import Path
import pandas as pd
import re

SENTIMENT_XLSX = Path("Beats_Scraped_Data_sentiment (1).xlsx")
OUT_XLSX       = Path("Beats_Reviews_Gemini_analysis.xlsx")  # will overwrite/create

#2: Load Data
def load_dataset(path: Path = SENTIMENT_XLSX) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Sentiment file not found: {path}")
    df = pd.read_excel(path)
    # normalize expected columns
    for col in ["content", "brand", "product_attributes", "title", "product_id", "short_name", "rating", "Sentiment"]:
        if col not in df.columns:
            df[col] = ""
    df["content"] = df["content"].fillna("").astype(str)
    return df

#3: Product Mapping
def build_product_mapping(df: pd.DataFrame) -> pd.DataFrame:
    def infer_short_brand(row):
        text = f"{row.get('product_attributes','')} {row.get('title','')} {row.get('content','')}".lower()
        if ("beats" in text) or ("pill" in text):
            return "Beats Pill+", "Beats"
        if ("flip 6" in text) or ("jbl" in text):
            return "JBL Flip 6", "JBL"
        if ("soundlink" in text) or ("bose" in text):
            return "Bose SoundLink", "Bose"
        if ("sony" in text) or (" xb" in text):
            return "Sony XB Series", "Sony"
        if ("soundcore" in text) or ("anker" in text):
            return "Anker Soundcore", "Anker"
        # fallback
        return row.get("product_id") or "Unknown", "Unknown"

    mapped = [infer_short_brand(r) for _, r in df.iterrows()]
    df = df.copy()
    df["short_name"], df["brand"] = zip(*mapped)
    return df

#4: Themes & Helpers
THEMES = {
    "battery": r"(?:battery|charge|charging|power|life|lasts)",
    "price": r"(?:price|expensive|cost|value|worth)",
    "durability": r"(?:durab|quality|broke|break|defect|return|replace|sturdy|build)",
    "connectivity": r"(?:connect|connection|disconnect|bluetooth|pair|pairing|drop)",
    "sound": r"(?:sound|bass|audio|volume|clarity|loud|quality)",
    "design": r"(?:design|look|style|aesthetic|color)"
}

def count_mentions(subdf: pd.DataFrame, pattern: str) -> int:
    return subdf["content"].str.contains(pattern, flags=re.IGNORECASE, regex=True, na=False).sum()

def top_examples(subdf: pd.DataFrame, pattern: str, k: int = 2, width: int = 140) -> str:
    hits = subdf[subdf["content"].str.contains(pattern, flags=re.IGNORECASE, regex=True, na=False)]["content"].head(k).tolist()
    cleaned = []
    for h in hits:
        txt = re.sub(r"\s+", " ", str(h)).strip()
        cleaned.append(f"“{txt[:width]}...”")
    return " | ".join(cleaned)

#5: Build Beats Summary (3 pain points, 3 strengths, 3 recommendations)
def build_summary_table_beats(df: pd.DataFrame) -> pd.DataFrame:
    beats_df = df[df["brand"].str.lower() == "beats"].copy()
    beats_n = len(beats_df)

    counts = {k: count_mentions(beats_df, patt) for k, patt in THEMES.items()}
    freqs  = {k: (round(100 * counts[k] / beats_n, 1) if beats_n else 0.0) for k in counts}

    pain_candidates = ["battery", "price", "durability", "connectivity"]
    pain_ranked = sorted(pain_candidates, key=lambda k: counts.get(k, 0), reverse=True)[:3]

    strength_candidates = ["sound", "design"]
    # choose third strength as highest remaining
    remaining = [k for k in THEMES.keys() if k not in pain_ranked + strength_candidates]
    strengths = ["sound", "design"]
    remaining_sorted = sorted(remaining, key=lambda k: counts.get(k, 0), reverse=True)
    for cand in remaining_sorted:
        if len(strengths) >= 3:
            break
        strengths.append(cand)

    rows = []
    for key in pain_ranked:
        rows.append({
            "Category": "Pain Point",
            "Finding": f"{key.capitalize()} concerns",
            "Supporting Evidence": f"{counts[key]} Beats reviews mention {key}",
            "Frequency/Impact": f"{freqs[key]}% of Beats reviews",
            "Examples": top_examples(beats_df, THEMES[key], k=2)
        })
    for key in strengths[:3]:
        rows.append({
            "Category": "Strength",
            "Finding": f"{key.capitalize()} praised",
            "Supporting Evidence": f"{counts[key]} Beats reviews mention {key}",
            "Frequency/Impact": f"{freqs[key]}% of Beats reviews",
            "Examples": top_examples(beats_df, THEMES[key], k=2)
        })

    rec_map = {
        "battery": "Enhance battery life (cells, power mgmt)",
        "price": "Offer value/bundles (e.g., Apple Music) or tiered trims",
        "durability": "Improve durability & QC messaging (materials/testing)",
        "connectivity": "Strengthen Bluetooth stack, pairing reliability",
        "sound": "Add tuning/EQ presets to widen appeal",
        "design": "Offer premium design variants/colors"
    }
    for key in pain_ranked[:3]:
        rows.append({
            "Category": "Recommendation",
            "Finding": rec_map.get(key, f"Improve {key}"),
            "Supporting Evidence": f"{counts[key]} mentions of {key} among Beats reviews",
            "Frequency/Impact": f"{freqs[key]}% of Beats reviews",
            "Examples": ""
        })
    return pd.DataFrame(rows)

#6: Beats vs Competitors
def beats_vs_competitors_tables(df: pd.DataFrame):
    beats_df = df[df["brand"].str.lower() == "beats"].copy()
    comp_df  = df[df["brand"].str.lower() != "beats"].copy()

    def theme_block(subdf: pd.DataFrame, label: str) -> pd.DataFrame:
        n = len(subdf)
        counts = {k: count_mentions(subdf, patt) for k, patt in THEMES.items()}
        freqs  = {k: (round(100 * counts[k] / n, 1) if n else 0.0) for k in counts}
        rows = [{"segment": label, "theme": k, "mentions": counts[k], "share_%": freqs[k]} for k in THEMES.keys()]
        return pd.DataFrame(rows)

    # overall Beats vs all competitors
    overall = pd.concat([
        theme_block(beats_df, "Beats"),
        theme_block(comp_df, "All Competitors")
    ], ignore_index=True)

    # top competitor by volume
    top_comp = ""
    if not comp_df.empty and "short_name" in comp_df.columns:
        comp_counts = comp_df.groupby("short_name")["content"].count().sort_values(ascending=False)
        if not comp_counts.empty:
            top_comp = comp_counts.index[0]

    per_product = pd.DataFrame()
    if top_comp:
        top_df = comp_df[comp_df["short_name"] == top_comp]
        per_product = theme_block(top_df, f"{top_comp}")

    # brand-level competitor summaries
    brand_blocks = []
    for brand, g in comp_df.groupby("brand"):
        brand_blocks.append(theme_block(g, f"{brand}"))
    brand_table = pd.concat(brand_blocks, ignore_index=True) if brand_blocks else pd.DataFrame(columns=["segment","theme","mentions","share_%"])

    # compact pivot (% matrix)
    combined = [overall] + ([per_product] if not per_product.empty else []) + ([brand_table] if not brand_table.empty else [])
    joined = pd.concat(combined, ignore_index=True) if combined else overall
    matrix = joined.pivot_table(index="theme", columns="segment", values="share_%", aggfunc="first").reset_index()

    return overall, per_product, brand_table, matrix

#7: Survey Details (counts, averages, sentiment dist)
def build_survey_details(df: pd.DataFrame):
    total_reviews = len(df)
    brands = df["brand"].replace("", "Unknown")
    products = df["short_name"].replace("", "Unknown")

    by_brand = (df.assign(brand=brands)
                  .groupby("brand")
                  .agg(reviews=("content", "count"),
                       avg_rating=("rating", "mean"))
                  .sort_values("reviews", ascending=False)
                  .reset_index())

    by_product = (df.assign(short_name=products)
                    .groupby("short_name")
                    .agg(brand=("brand", "first"),
                         reviews=("content", "count"),
                         avg_rating=("rating", "mean"))
                    .sort_values("reviews", ascending=False)
                    .reset_index())

    if "Sentiment" in df.columns:
        sent_overall = (df["Sentiment"].value_counts(normalize=True) * 100).round(1).reset_index()
        sent_overall.columns = ["Sentiment", "Share_%"]
        sent_by_brand = (df.assign(brand=brands)
                           .pivot_table(index="brand", columns="Sentiment", values="content", aggfunc="count", fill_value=0))
        sent_by_brand = (sent_by_brand.div(sent_by_brand.sum(axis=1), axis=0) * 100).round(1).reset_index()
    else:
        sent_overall = pd.DataFrame(columns=["Sentiment", "Share_%"])
        sent_by_brand = pd.DataFrame()

    return by_brand, by_product, sent_overall, sent_by_brand, total_reviews

#8: Export to Excel & CSV
def export_excel(df: pd.DataFrame, beats_summary: pd.DataFrame,
                 overall: pd.DataFrame, per_product: pd.DataFrame,
                 brand_table: pd.DataFrame, matrix: pd.DataFrame,
                 by_brand: pd.DataFrame, by_product: pd.DataFrame,
                 sent_overall: pd.DataFrame, sent_by_brand: pd.DataFrame,
                 total_reviews: int, out_xlsx: Path = OUT_XLSX):
    with pd.ExcelWriter(out_xlsx, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="enriched")
        beats_summary.to_excel(writer, index=False, sheet_name="summary_table_beats")
        overall.to_excel(writer, index=False, sheet_name="beats_vs_competitors")
        if not per_product.empty:
            per_product.to_excel(writer, index=False, sheet_name="top_competitor_only")
        if not brand_table.empty:
            brand_table.to_excel(writer, index=False, sheet_name="competitors_by_brand")
        matrix.to_excel(writer, index=False, sheet_name="beats_vs_comp_matrix")
        # Survey details sheet with multiple blocks
        start = 0
        pd.DataFrame({"Metric": ["Total Reviews"], "Value": [total_reviews]}).to_excel(writer, index=False, sheet_name="survey_details", startrow=start)
        start += 3
        by_brand.to_excel(writer, index=False, sheet_name="survey_details", startrow=start)
        start += len(by_brand) + 2
        by_product.to_excel(writer, index=False, sheet_name="survey_details", startrow=start)
        start += len(by_product) + 2
        if not sent_overall.empty:
            sent_overall.to_excel(writer, index=False, sheet_name="survey_details", startrow=start)
            start += len(sent_overall) + 2
        if not sent_by_brand.empty:
            sent_by_brand.to_excel(writer, index=False, sheet_name="survey_details", startrow=start)

        out_dir = out_xlsx.parent / "csv_outputs"
        out_dir.mkdir(exist_ok=True)

        df.to_csv(out_dir / "enriched.csv", index=False)
        beats_summary.to_csv(out_dir / "summary_table_beats.csv", index=False)
        overall.to_csv(out_dir / "beats_vs_competitors.csv", index=False)
        if not per_product.empty:
            per_product.to_csv(out_dir / "top_competitor_only.csv", index=False)
        if not brand_table.empty:
            brand_table.to_csv(out_dir / "competitors_by_brand.csv", index=False)
        matrix.to_csv(out_dir / "beats_vs_comp_matrix.csv", index=False)
        by_brand.to_csv(out_dir / "survey_by_brand.csv", index=False)
        by_product.to_csv(out_dir / "survey_by_product.csv", index=False)
        if not sent_overall.empty:
            sent_overall.to_csv(out_dir / "survey_sent_overall.csv", index=False)
        if not sent_by_brand.empty:
            sent_by_brand.to_csv(out_dir / "survey_sent_by_brand.csv", index=False)

#9: Main
def main():
    df = load_dataset()
    df = build_product_mapping(df)
    beats_summary = build_summary_table_beats(df)
    overall, per_product, brand_table, matrix = beats_vs_competitors_tables(df)
    by_brand, by_product, sent_overall, sent_by_brand, total_reviews = build_survey_details(df)
    export_excel(df, beats_summary, overall, per_product, brand_table, matrix,
                 by_brand, by_product, sent_overall, sent_by_brand, total_reviews, OUT_XLSX)
    print(f"[OK] Wrote Excel to: {OUT_XLSX}")

if __name__ == "__main__":
    main()
