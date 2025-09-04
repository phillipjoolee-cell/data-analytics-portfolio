# Scraped Amazon Reviews Analysis – Wireless Speakers (Beats vs Competitors)  

## Overview  
This project scraped and analyzed Amazon reviews for Beats and four competitors. Using Python (pandas, NumPy, Seaborn, Matplotlib, TextBlob, Gemini AI), I built a pipeline to clean raw review data, explore patterns, run sentiment scoring, and surface AI-driven insights.  

## Workflow  
- **Scraping & Cleaning** – started with raw JSON/CSV reviews, removed duplicates, standardized fields, and created helper columns (review length, year).  
- **NumPy Prep** – handled missing/invalid values, normalized ratings, and staged the dataset for numerical work.  
- **EDA** – summarized distributions, identified outliers, and broke down verified purchase trends.  
- **Visualization** – built charts for ratings, product comparisons, and time-based trends.  
- **Correlation Analysis** – created a correlation matrix across numeric variables (no strong correlations, confirming review sentiment is subjective).  
- **Sentiment Analysis** – added polarity and subjectivity scores with TextBlob; positives highlight sound/design, negatives focus on price/battery.  
- **Gemini AI Layer** – clustered customer themes, compared Beats vs competitors, and generated strategy-oriented takeaways.  

## What It Shows  
- Consumers consistently praise Beats for sound quality and design, but call out battery life and pricing as weaknesses.  
- The pipeline demonstrates how raw, unstructured reviews can be transformed into structured datasets, visualizations, and insights using Python, sentiment analysis, and AI. 
