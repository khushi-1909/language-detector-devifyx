"""
Language Detection with Cosine Similarity

This script detects the language of a given text using cosine similarity on trigram profiles.
It supports quick testing and interactive use.
"""

import json
import math
from lang_utils import load_language_profiles, build_trigram_profile,languages

def cosine_similarity(profile1, profile2):
    """
    This function calculates the cosine similarity between two trigram frequency profiles.
    It return a score between 0 (no similarity) and 1 (exact match)."""
    intersection = set(profile1) & set(profile2)
    if not intersection:
        return 0.0
    numerator = sum(profile1.get(k, 0) * profile2.get(k, 0) for k in intersection)
    sum1 = sum(v ** 2 for v in profile1.values())
    sum2 = sum(v ** 2 for v in profile2.values())
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    return numerator / denominator if denominator else 0.0

def detect_language(text, profiles):
    """
    Given an Input sentence and a dictionary of trigram profiles,
    this function returns the language code wth the highest similarity,
    the confidence score, and all the other scores for transparency."""
    input_profile = build_trigram_profile(text)
    similarities = {
        lang: cosine_similarity(input_profile, profile)
        for lang, profile in profiles.items()
    }
    best_match = max(similarities, key=similarities.get)
    return best_match, similarities[best_match], similarities

if __name__ == "__main__":
    print('=' * 55)
    print('Welcome to the Trigram Cosine Similarity Language Detector!')
    print('Type a sentece and press Enter to detects its language.')
    print("Type 'exit' and press Enter to quit.\n" )
    print('=' * 55)

    #Load precomputed trigram profiles from JSON files
    profiles = load_language_profiles('profiles')
    
    while True:
        sentence = input('Enter a sentence: ').strip()
        if sentence.lower() == 'exit':
            print("👋 Goodbye and thank you for using the detector!")
            break

        lang, score, all_scores = detect_language(sentence, profiles)
        
        #Printing the results as required
        result={
            'language': languages[lang],
            'iso_code': lang,
            'confidence': round(score, 4),
        }
        print('\nPredicted Language(Cosine Similarity): ')
        print(json.dumps(result, ensure_ascii=False, indent=4))

        #Showing the top 3 languages with their scores for transparency
        print("\nTop 3 languages (by confidence):")
        for code in sorted(all_scores, key=all_scores.get, reverse=True)[:3]:
            print(f"{code}: {all_scores[code]:.4f}")
        print('=' * 55)
        


