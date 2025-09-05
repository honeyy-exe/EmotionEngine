import string
import os
import re
import requests
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize, sent_tokenize

# -----------------------------
# FOLDER PATHS
# -----------------------------
INPUT_URL_FILE = "Input-urls.txt"
OUTPUT_FOLDER = "Articles"
STOPWORDS_FOLDER = "StopWords"
MASTER_DICT_FOLDER = "MasterDictionary"

# -----------------------------
# 1️⃣ Save Articles from URLs
# -----------------------------
def save_articles_from_txt(file_path, output_folder):
    """
    Reads URLs from a text file and saves each article as a separate .txt file.
    """
    os.makedirs(output_folder, exist_ok=True)
    with open(file_path, "r") as f:
        urls = [line.strip() for line in f if line.strip()]

    for idx, url in enumerate(urls, start=1):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")

            title_tag = soup.find("h1")
            title = title_tag.get_text(strip=True) if title_tag else ""
            content_tag = soup.find("article")
            if not content_tag:
                content_tag = soup.find("div", class_="content")
            text = content_tag.get_text(strip=True) if content_tag else ""
            full_text = f"{title}\n{text}"

            file_name = os.path.join(output_folder, f"URL_{idx}.txt")
            with open(file_name, "w", encoding="utf-8") as file:
                file.write(full_text)

            print(f"Saved article {idx} from {url}")

        except Exception as e:
            print(f"Failed to process {url}: {e}")

# -----------------------------
# 2️⃣ Text Cleaning & Tokenization
# -----------------------------
def clean_text(text):
    text = re.sub(r'[^A-Za-z\s\-+]', '', text)
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def tokenize_text(text):
    return word_tokenize(text)

def load_word_list(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        return set(line.lower().strip() for line in f if line.strip())

def load_stopwords(folder):
    stopwords = set()
    for file in os.listdir(folder):
        with open(os.path.join(folder, file), "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                stopwords.update([word for word in line.strip().lower().split("|") if word])
    return stopwords

def remove_stopwords_from_text(text, stopwords):
    tokens = word_tokenize(text.lower())
    return [t for t in tokens if t not in stopwords and t not in string.punctuation]

# -----------------------------
# 3️⃣ Complexity / Readability Metrics
# -----------------------------
def count_syllables(word):
    word = word.lower()
    vowels = "aeiou"
    count = 0
    if len(word) <= 3:
        return 1
    if word.endswith(('es', 'ed')):
        word = word[:-2]
    for i, letter in enumerate(word):
        if letter in vowels and (i == 0 or word[i-1] not in vowels):
            count += 1
    return count if count > 0 else 1

def text_complexity_metrics(text):
    sentences = sent_tokenize(text)
    words = tokenize_text(text)
    alpha_words = [w for w in words if w.isalpha()]
    avg_sent_len = len(alpha_words) / len(sentences) if sentences else 0
    complex_words = sum(1 for w in alpha_words if count_syllables(w) > 2)
    perc_complex = complex_words / len(alpha_words) if alpha_words else 0
    avg_word_len = sum(len(w) for w in alpha_words) / len(alpha_words) if alpha_words else 0
    syll_per_word = sum(count_syllables(w) for w in alpha_words) / len(alpha_words) if alpha_words else 0
    return avg_sent_len, perc_complex, avg_word_len, syll_per_word, complex_words

def fog_index(avg_sent_len, perc_complex):
    return 0.4 * (avg_sent_len + perc_complex * 100)

def personal_pronouns_count(text):
    pronoun_pattern = r'\b(I|we|my|ours|us)\b'
    matches = re.findall(pronoun_pattern, text, flags=re.I)
    return len([m for m in matches if not (m.upper() == "US" and m == m.upper())])

# -----------------------------
# 4️⃣ Sentiment Scoring
# -----------------------------
def calculate_positive_score(words, pos_words):
    return sum(1 for w in words if w in pos_words)

def calculate_negative_score(words, neg_words):
    return sum(1 for w in words if w in neg_words)

def calculate_neutral_score(words, pos_words, neg_words):
    return sum(1 for w in words if w not in pos_words and w not in neg_words)

def calculate_sentiment_ratio(pos_score, neg_score):
    return pos_score / (neg_score + 1e-6)

def calculate_polarity_score(pos_score, neg_score):
    return (pos_score - neg_score) / (pos_score + neg_score + 1e-6)

def calculate_subjectivity_score(pos_score, neg_score, word_count):
    return (pos_score + neg_score) / (word_count + 1e-6)

def calculate_weighted_polarity(words, pos_words, neg_words, tech_words):
    score = 0
    for w in words:
        if w in pos_words:
            score += 2 if w in tech_words else 1
        elif w in neg_words:
            score -= 2 if w in tech_words else 1
    return score / (len(words) + 1e-6)

def calculate_tech_score(words, tech_words):
    return sum(1 for w in words if w in tech_words)

# -----------------------------
# 5️⃣ MAIN WORKFLOW
# -----------------------------
# Step 1: Save articles from URLs
save_articles_from_txt(INPUT_URL_FILE, OUTPUT_FOLDER)

# Step 2: Load dictionaries and stopwords
positive_words = load_word_list(os.path.join(MASTER_DICT_FOLDER, "positive-words.txt"))
negative_words = load_word_list(os.path.join(MASTER_DICT_FOLDER, "negative-words.txt"))
tech_words = load_word_list(os.path.join(MASTER_DICT_FOLDER, "tech-words.txt"))
stopwords = load_stopwords(STOPWORDS_FOLDER)

# Step 3: Process each article
results = []

for filename in os.listdir(OUTPUT_FOLDER):
    if filename.endswith(".txt"):
        with open(os.path.join(OUTPUT_FOLDER, filename), "r", encoding="utf-8", errors="ignore") as f:
            raw_text = f.read()
            cleaned_text = clean_text(raw_text)
            tokens = remove_stopwords_from_text(cleaned_text, stopwords)

            # Complexity / Readability
            avg_sent_len, perc_complex, avg_word_len, syll_per_word, comp_word_cnt = text_complexity_metrics(cleaned_text)
            fog = fog_index(avg_sent_len, perc_complex)
            pers_pronouns = personal_pronouns_count(cleaned_text)

            # Sentiment
            pos_score = calculate_positive_score(tokens, positive_words)
            neg_score = calculate_negative_score(tokens, negative_words)
            neutral_score = calculate_neutral_score(tokens, positive_words, negative_words)
            polarity_score = calculate_polarity_score(pos_score, neg_score)
            subjectivity_score = calculate_subjectivity_score(pos_score, neg_score, len(tokens))
            weighted_polarity = calculate_weighted_polarity(tokens, positive_words, negative_words, tech_words)
            sentiment_ratio = calculate_sentiment_ratio(pos_score, neg_score)
            tech_score = calculate_tech_score(tokens, tech_words)
            word_count = len(tokens)

        results.append({
            "URL_ID": filename.replace(".txt",""),
            "POSITIVE SCORE": pos_score,
            "NEGATIVE SCORE": neg_score,
            "NEUTRAL SCORE": neutral_score,
            "POLARITY SCORE": polarity_score,
            "WEIGHTED POLARITY": weighted_polarity,
            "SUBJECTIVITY SCORE": subjectivity_score,
            "SENTIMENT RATIO": sentiment_ratio,
            "TECH WORD SCORE": tech_score,
            "AVG SENTENCE LENGTH": avg_sent_len,
            "PERCENTAGE OF COMPLEX WORDS": perc_complex,
            "FOG INDEX": fog,
            "AVG WORD LENGTH": avg_word_len,
            "SYLLABLE PER WORD": syll_per_word,
            "COMPLEX WORD COUNT": comp_word_cnt,
            "PERSONAL PRONOUNS": pers_pronouns,
            "WORD COUNT": word_count
        })

# Step 4: Save all analysis to a single TXT file
output_file = "Final_Analysis.txt"

with open(output_file, "w", encoding="utf-8") as f:
    for res in results:
        for key, value in res.items():
            f.write(f"{key}: {value}\n")
        f.write("-" * 60 + "\n")  # Separator between articles

print(f"✅ Analysis complete! Check {output_file}")
