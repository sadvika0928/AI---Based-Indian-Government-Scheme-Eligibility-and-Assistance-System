import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

# Load the CSV relative to this file
current_dir = os.path.dirname(__file__)
csv_path = os.path.join(current_dir, 'schemes.csv')

# Load your existing CSV
df = pd.read_csv(csv_path)

# Combine name and description for matching
df['full_text'] = df['name'] + " " + df['description']

# TF-IDF Vectorizer
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df['full_text'])

def get_matches(user_input, top_k=3):
    user_vec = vectorizer.transform([user_input])
    scores = cosine_similarity(user_vec, tfidf_matrix).flatten()
    k = min(top_k, len(scores))
    top_indices = scores.argsort()[-k:][::-1]

    matches = []
    for i in top_indices:
        matches.append({
            'name': df.iloc[i]['name'],
            'description': df.iloc[i]['description'],
            'eligibility': df.iloc[i]['eligibility'],
            'documents': df.iloc[i]['documents'],
            'apply': df.iloc[i]['apply'],
            'score': round(scores[i], 2)
        })

    return matches
