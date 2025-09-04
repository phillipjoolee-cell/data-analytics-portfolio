# Scripts — Amazon Reviews Pipeline

This folder has all the Python scripts I used to take raw Amazon reviews (Beats + competitors) and turn them into insights. If you run them in order, they’ll recreate the whole pipeline from cleaning, prepping, and EDA all the way through to visuals, correlations, sentiment, and Gemini AI.

## Run Order

1. **`data_cleansing_pandas.py`**  
   Cleans the raw OxyLabs export. Standardizes columns, removes duplicates, normalizes ratings, and adds helper fields like review length and year. Outputs a multi-sheet Excel file with samples, a cleaning log, data dictionary, and cleaned dataset.
2. **`review_numpy_prepped.py`**  
   Takes the cleaned Excel file and makes it ready for analysis. Handles missing values, filters invalid ratings, adds word counts, normalizes ratings to 0–1, and saves both Excel and CSV.
3. **`panda_eda.py`**  
   Runs exploratory data analysis. Produces summary stats, missing value checks, outlier detection, categorical breakdowns (like verified purchases), and a correlation matrix. Exports to Excel and CSV.
4. **`matplotlib_seaborn_visualizations.py`**  
   Creates visualizations and a KPI block: ratings distributions, product comparisons, boxplots, and monthly trends. Saves PNGs and embeds them into an Excel dashboard.
5. **`correlation_matrix.py`**  
   Builds a correlation matrix, finds the strongest relationships, flags values with |r| ≥ 0.5, and generates a heatmap. Saves everything to Excel, CSV, and PNG.
6. **`sentiment_analysis_with_textblob.py`**  
   Runs sentiment analysis on review text. Calculates polarity and subjectivity, assigns Positive/Neutral/Negative labels, and outputs Excel and CSV files with summary tables and charts.
7. **`gemini_api.py`** (optional, last step)  
   Uses Gemini AI to pull themes and strategy-level insights from reviews. Organizes language into business-friendly takeaways. Requires a Gemini API key and quota.

## I/O

- Starting file: `Beats_Scraped_Data.csv` (the raw OxyLabs export)  
- Intermediate files:  
  - Cleaned: `Beats_Scraped_Data_Cleaned.xlsx`  
  - NumPy-prepped: `Beats_Scraped_Data_NumPy_Prepped.xlsx` / `.csv`  
  - EDA: `Beats_Scraped_Data_Pandas_EDA.xlsx` / `.csv`  
- Final deliverables:  
  - Excel dashboards with visuals  
  - Correlation matrix (Excel, CSV, and PNG)  
  - Sentiment results (Excel, CSV, and charts)  
  - Gemini insights workbook (optional)

If you’re using `raw/`, `interim/`, and `processed/` folders, you may need to adjust file paths inside the scripts. By default, the scripts assume everything is in the same working directory.

---

## How to Run

### Local (Python 3.10+)

1. Install dependencies:
   ```bash
   pip install pandas numpy matplotlib openpyxl xlsxwriter textblob google-generativeai

Note: google-generativeai is only needed if you run gemini_api.py and all of the code was compiled and ran through Google Colab.
