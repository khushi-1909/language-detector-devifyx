import os
import json
import math
import re
from collections import Counter
import unicodedata

def normalize_trigram(trigram):
    return unicodedata.normalize("NFC", trigram)


def load_language_profiles(folder="profiles"):
    profiles = {}
    for file in os.listdir(folder):
        if file.endswith(".json"):
            lang = file[:-5]
            with open(os.path.join(folder, file), encoding="utf-8") as f:
                raw_profile = json.load(f)
                # Normalize keys here!
                profile = {normalize_trigram(k): v for k, v in raw_profile.items()}
                profiles[lang] = profile
    return profiles


def clean_text(text):
    text=re.sub(r'[^\w\s]', '', text, flags=re.UNICODE)  # remove punctuation
    return text.strip().lower()

def generate_trigram_profile(text):
    text = clean_text(text)
    trigrams = [normalize_trigram(text[i:i+3]) for i in range(len(text) - 2)]
    counts = Counter(trigrams)
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()} if total > 0 else {}


def cosine_similarity(profile1, profile2):
    intersection = set(profile1) and set(profile2)
    if not intersection:
        return 0.0
    numerator = sum(profile1.get(k, 0) * profile2.get(k, 0) for k in intersection)
    sum1=sum(v**2 for v in profile1.values())
    sum2=sum(v**2 for v in profile2.values())
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    return numerator / denominator if denominator else 0.0

def detect_language(text, profiles):
    input_profile=generate_trigram_profile(text)
    similarities={
        lang: cosine_similarity(input_profile, profile)
        for lang, profile in profiles.items()
    }
    best_match=max(similarities, key=similarities.get)
    return best_match, similarities[best_match], similarities


#example with a sample text
profiles=load_language_profiles('profiles')

if __name__ == '__main__':
    profiles=load_language_profiles('profiles')
    print("🌍 Language Detector Ready! (Type 'exit' to quit)\n")
    while True:
        sentence=input('Enter a sentence to detect language: ').strip()
        if sentence.lower() == 'exit':
            print("👋 Goodbye!")
            break
        lang, score, all_scores = detect_language(sentence, profiles)
        print(f"\nPredicted language: {lang}")
        print(f"Confidence score: {score:.4f}\n")