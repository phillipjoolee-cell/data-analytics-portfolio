## Scraped Amazon Reviews Analysis – Wireless Speakers (Beats by Dre vs Competitors)
# Executive Summary

This project evaluates whether Beats by Dre should launch a new high-fidelity wireless speaker. The analysis shows that a launch is viable if the price remains in the $129–$199 range and battery life is at least 15 hours. Fans consistently praise sound quality and Apple ecosystem integration, while complaints center on battery performance, durability, and pricing. The recommended strategy is to extend battery life, bundle with Apple Music, and offer premium design variants to justify higher pricing. The work combines Python, Pandas, NumPy, Seaborn, Matplotlib, TextBlob, and Gemini AI.

# Project Overview

I gathered Amazon reviews for five wireless speaker products, including Beats and four competitors. Starting with raw JSON data, I built a pipeline that cleans, analyzes, and interprets reviews to generate insights that inform business strategy.

# Workflow

The project began with scraping and cleaning the reviews. Data was standardized, duplicates removed, and helper fields created for review length and year. NumPy was used to handle missing and invalid values, normalize ratings, and prepare the dataset for numerical work. Exploratory data analysis provided descriptive statistics, identified outliers, and summarized categorical features such as verified purchases.

I then created visualizations to show key patterns: ratings distributions, product comparisons, and trends over time. A correlation matrix was built to check for relationships across numeric variables, though no strong correlations emerged, reinforcing that review sentiment is subjective.

Sentiment analysis with TextBlob added polarity and subjectivity scores, revealing that positive reviews often emphasize sound quality and design, while negative reviews focus on price and battery issues. Finally, Gemini AI built on top of this by organizing customer language into themes, comparing Beats against competitors, and suggesting strategy-oriented recommendations. This layered approach distilled why customers feel the way they do and transformed raw reviews into executive-ready insights.

# Key Insights

The wireless speaker market is already mature and competitive, with high ownership rates. Beats polarizes consumers: it wins on brand, sound, and design, but loses ground on battery life and pricing. The data suggests that a launch can succeed if Beats positions the product carefully, balancing practical value with brand strengths.

# Final Takeaways

Beats should move forward with a launch only if pricing falls between $129 and $199 and battery life meets or exceeds 15 hours. Bundling services and offering premium design editions can strengthen the business case. By combining EDA, sentiment analysis, and AI-generated insights, this project demonstrates how raw consumer feedback can be transformed into clear, strategic guidance.
