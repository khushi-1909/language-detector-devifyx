"""
Language Detection with Naive Bayes

This script detects the language of input sentences using a 
character trigram-based Naive Bayes classifier (MultinomialNB).
If the model is not found, it is trained from scratch using all .txt files in the 'data' folder.
Outputs are printed in JSON format.
"""

from lang_utils import clean_text, languages
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
import os
import json

def load_training_data(folder="data"):
    """
    This function loads sentences aqnd labels from all the .txt files in the data folder.
    Each line in the file is treated as one sentence.
    """
    texts, labels = [], []
    for file in os.listdir(folder):
        if file.endswith(".txt"):
            lang = file[:-4]
            with open(os.path.join(folder, file), encoding="utf-8") as f:
                for line in f:
                    clean = clean_text(line.strip())
                    if len(clean) > 5:
                        texts.append(clean)
                        labels.append(lang)
    return texts, labels

def get_vectorizer_and_features(texts):
    """
    This function fits a character trigram vectorizer to the training texts.
    """
    vectorizer = CountVectorizer(analyzer='char', ngram_range=(3, 3), lowercase=True)
    X = vectorizer.fit_transform(texts)
    return vectorizer, X

def train_bayes_model():
    """
    Here we train and save the Naive bayes language detection model and its vectorizer.
    """
    print('Training the naive Bayes Model....')
    texts, labels = load_training_data("data")
    vectorizer, X = get_vectorizer_and_features(texts)
    model = MultinomialNB()
    model.fit(X, labels)
    joblib.dump(model, "bayes_model.joblib")
    joblib.dump(vectorizer, "vectorizer.joblib")
    print("✅ Naive Bayes model for language detection has been trained and saved!")

def predict_language(sentence):
    """
    Loads the trained Bayes model, vectorizes the sentence,
    and predicts the most likely language and probabilities for each.
    """
    model = joblib.load("bayes_model.joblib")
    vectorizer = joblib.load("vectorizer.joblib")
    X = vectorizer.transform([sentence])
    predicted = model.predict(X)[0]
    probs = model.predict_proba(X)[0]
    lang_probs = dict(zip(model.classes_, probs))
    return predicted, lang_probs

if __name__ == "__main__":
    print("=" * 55)
    print("Welcome to the Naive Bayes Language Detector!")
    print("Type a sentence and press Enter to detect its language.")
    print("Type 'exit' (and press Enter) to quit.\n")
    print("=" * 55)

    #Auto train model if not found
    if not os.path.exists("bayes_model.joblib") or not os.path.exists("vectorizer.joblib"):
        train_bayes_model()

    while True:
        sentence = input('Enter a sentenc: ').strip()
        if sentence.lower() == 'exit':
            print("👋 Goodbye and thank you fro using the detector!")
            break
        lang, probs = predict_language(sentence)
        
        result = {
            'language': languages[lang],
            'iso_code': lang,
            'confidence': round(probs[lang], 4)
        }
        print("\nPredicted language (Naive Bayes):")
        print(json.dumps(result, ensure_ascii=False, indent=2))

        print("\nTop 3 languages (by confidence):")
        for code in sorted(probs, key=probs.get, reverse=True)[:3]:
            print(f"{code}: {probs[code]:.4f}")
        print("-" * 55)
