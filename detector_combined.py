import os
import json
import math
import re
from collections import Counter
import joblib

def load_language_profiles(folder='profiles'):
    profiles={}
    for file in os.listdir(folder):
        if file.endswith('.json'):
            lang=file[:-5]
            with open(os.path.join(folder,file), encoding='utf-8') as f:
                profiles[lang]=json.load(f)
    return profiles

def clean_text(text):
    text=re.sub(r'[^\w\s]', '', text, flags=re.UNICODE)
    return text.lower().strip()

def generate_trigram_profile(text):
    text=clean_text(text)
    trigrams=[text[i:i+3] for i in range(len(text)-2)]
    counts=Counter(trigrams)
    total= sum(counts.values())
    return {k:v/total for k, v in counts.items()} if total>0 else {}

def cosine_similarity(profile1, profile2):
    intersection=set(profile1) | set(profile2)
    if not intersection:
        return 0.0
    numerator=sum(profile1.get(k,0) * profile2.get(k,0) for k in intersection)
    sum1=sum(v**2 for v in profile1.values())
    sum2=sum(v**2 for v in profile2.values())
    denominator=math.sqrt(sum1) * math.sqrt(sum2)
    return numerator / denominator if denominator else 0.0

def detect_language_cosine(text, profiles):
    input_profile=generate_trigram_profile(text)
    similarities={
        lang: cosine_similarity(input_profile, profile)
        for lang, profile in profiles.items()
    }
    best_match=max(similarities, key=similarities.get)
    return best_match, similarities[best_match], similarities

def predict_language_bayes(sentence, model_path='bayes_model.joblib', vectorizer_path='vectorizer.joblib'):
    model=joblib.load(model_path)
    vectorizer=joblib.load(vectorizer_path)
    X=vectorizer.transform([sentence])
    predicted=model.predict(X)[0]
    probab=model.predict_proba(X)[0]
    lang_probab=dict(zip(model.classes_, probab))
    return predicted, lang_probab

def combined_detector(sentence, profiles):

    cosine_lang, cosine_score, cosine_scores= detect_language_cosine(sentence, profiles)
    bayes_lang, bayes_probab= predict_language_bayes(sentence)

    if cosine_lang == bayes_lang:
        final_lang=cosine_lang
        ensemble_confindence= (cosine_score + bayes_probab[final_lang]) / 2
        decision_note='Both the methods agree on the language.'
    else:
        if cosine_score > bayes_probab[bayes_lang]:
            final_lang=cosine_lang
            ensemble_confindence=cosine_score
            decision_note='Cosine similarity method is more confident.'
        else:
            final_lang=bayes_lang
            ensemble_confindence=bayes_probab[final_lang]
            decision_note='Naive Bayes method is more confident.'
    
    return {
        'input_text': sentence,
        'final_language': final_lang,
        'ensemble_confidence': ensemble_confindence,
        'cosine_language': cosine_lang,
        'cosine_confidence': cosine_score,
        'bayes_language': bayes_lang,
        'bayes_confidence': bayes_probab,   
        'decision_note': decision_note
        }

if __name__ == '__main__':
    profiles = load_language_profiles('profiles')
    print("🌍 Combined Language Detector Ready (Cosine + Naive Bayes)! (Type 'exit' to quit)\n")
    
    while True:
        sentence = input('Enter a sentence to detect language: ').strip()
        if sentence.lower() == 'exit':
            print('goodbye!')
            break
        
        result = combined_detector(sentence, profiles)
        
        print(f"\nPredicted language: {result['final_language']}")
        print(f"Ensemble confidence: {result['ensemble_confidence']:.4f}")
        print(f"Cosine similarity method: {result['cosine_language']} ({result['cosine_confidence']:.4f})")
        print(f"Naive Bayes method: {result['bayes_language']} ({result['bayes_confidence']})")
        print(f"Decision note: {result['decision_note']}\n")

        



    
