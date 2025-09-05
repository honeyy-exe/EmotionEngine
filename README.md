# EmotionEngine
📌 Overview

This project is all about text mining, sentiment analysis, and readability scoring.
Given a set of URLs, it scrapes the articles, cleans the text, and performs a complete linguistic analysis — from sentiment scores to readability metrics.

Instead of letting an assignment gather dust, I decided to push it here and turn it into something useful for anyone curious about text analytics.

🎯 The Backstory

I originally built this as part of an internship assignment. After submitting, the person who gave me the task… vanished (yep, ghosted).

But instead of letting that discourage me, I decided:
👉 Why waste a good project?
👉 Why not expand it and make it public?

So, I took publicly available tech articles, ran them through my pipeline, and here we are.

🛠️ What It Does

Scrapes and saves each article into its own .txt file

Cleans and preprocesses the text (removes stopwords, punctuation, etc.)

Runs sentiment analysis using a custom dictionary of positive/negative words

Computes readability metrics like Fog Index, Avg Sentence Length, % Complex Words

Extracts linguistic features like pronouns, syllables, avg word length

Exports everything neatly into one final analysis file

📂 Project Structure

MasterDictionary/ → Positive & Negative word lists

StopWords/ → General stopwords for text cleaning

Articles/ → Raw text files scraped from the URLs

Input_Urls.txt → The starting point (list of article links to process)

final_analysis.txt → Consolidated output with all metrics

⚡ Extra Features

I intentionally left in some bonus functions (like pronoun counter, syllable counter, readability formulas).
These weren’t strictly required, but they’re handy if you want to extend the analysis further.

Think of it like extra tools in the toolbox.

🤓 Skills Demonstrated

Web Scraping with BeautifulSoup4

Natural Language Processing with NLTK

Text cleaning & regex tricks

Sentiment analysis using dictionary-based scoring

Readability and linguistic feature extraction

File handling & project structuring for GitHub

🔮 Future Ideas

Add visualizations (graphs for sentiment trends, readability comparisons, etc.)

Build a Flask/Django app for live analysis from any URL

Expand dictionaries with domain-specific keywords for deeper insights

👨‍💻 TL;DR

Built as an internship assignment → became my portfolio project

Scrapes, cleans, and analyzes tech articles

Outputs a final analysis file with sentiment + readability scores

Shows skills in data analysis, NLP, and Python automation

Input: Input_Urls.txt | Output: final_analysis.txt

🔥 This isn’t just a “college assignment dump.”
It’s proof that I can take an unfinished task, own it, and ship it as a real, working project.
