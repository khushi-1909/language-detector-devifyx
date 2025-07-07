"""
Hybrid Language Detection: Cosine Similarity + Naive Bayes Ensemble

This script combines the trigram cosine similarity and the Naive Bayes Model predictions
to make an even more accurate language detection decision.
Outputs are in JSON, with all the key scores and logic explained.
"""

import json
from lang_utils import load_language_profiles, languages
import joblib
from detect_language_cosine import detect_language as detect_language_cosine


def predict_language_bayes(sentence):
    model = joblib.load("bayes_model.joblib")
    vectorizer = joblib.load("vectorizer.joblib")
    X = vectorizer.transform([sentence])
    predicted = model.predict(X)[0]
    probs = model.predict_proba(X)[0]
    lang_probs = dict(zip(model.classes_, probs))
    return predicted, lang_probs

def ensemble_predict(sentence, profiles):
    cosine_lang, cosine_score, _ = detect_language_cosine(sentence, profiles)
    bayes_lang, bayes_probs = predict_language_bayes(sentence)
    bayes_score = bayes_probs.get(bayes_lang, 0)

    if cosine_lang == bayes_lang:
        final_lang = cosine_lang
        ensemble_confidence = (cosine_score + bayes_score) / 2
        decision_note = "Both models agree"
    else:
        if cosine_score >= bayes_score:
            final_lang = cosine_lang
            ensemble_confidence = cosine_score
            decision_note = "Models disagree; cosine model chosen"
        else:
            final_lang = bayes_lang
            ensemble_confidence = bayes_score
            decision_note = "Models disagree; bayes model chosen"

    return {
        "language": languages.get(final_lang, "Unknown"),
        "iso_code": final_lang,
        "confidence": ensemble_confidence,
        "cosine_language": cosine_lang,
        "cosine_confidence": round(cosine_score, 4),
        "bayes_language": bayes_lang,
        "bayes_confidence": round(bayes_score, 4),
        "decision_note": decision_note
    }

if __name__ == "__main__":
    print("=" * 55)
    print("Welcome to the Hybrid Language Detector (Cosine + Bayes)!")
    print("Type a sentence and press Enter to detect its language.")
    print("Type 'exit' and press Enter to quit.\n")
    print("=" * 55)

    profiles = load_language_profiles("profiles")

    while True:
        sentence = input("Enter a sentence: ").strip()
        if sentence.lower() == "exit":
            print("👋 Goodbye and thank you for using the detector!")
            break

        result = ensemble_predict(sentence, profiles)

        print("\nPredicted language (Ensemble):")
        print(json.dumps({
            "language": result["language"],
            "iso_code": result["iso_code"],
            "confidence": round(result["confidence"], 2)
        }, ensure_ascii=False, indent=2))

        print("\nDetails:")
        print(f"Cosine: {result['cosine_language']} ({result['cosine_confidence']:.4f})")
        print(f"Bayes: {result['bayes_language']} ({result['bayes_confidence']:.4f})")
        print(f"Note: {result['decision_note']}")
        print("-" * 55)
