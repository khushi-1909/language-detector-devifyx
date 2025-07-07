"""
Shared Utilities for the Language Detection Assignment

This module provides text cleaning, trigram extraction, and profile loading functions.
All the main scripts (cosine, bayes and combined) import these functions from here.
"""

import re
from collections import Counter
import unicodedata
import json
import os

def clean_text(text):
    """
    Cleans input text:
    - Removes punctuation using Unicode rules
    - Converts to lowercase
    - Strips leading/trailing whitespace

    Args:
        text (str): Input sentence

    Returns:
        str: Cleaned sentence
    """
    text = re.sub(r'[^\w\s]', '', text, flags=re.UNICODE)
    return text.lower().strip()

def normalize_trigram(trigram):
    """
    Normalizes a trigram using Unicode NFC form.

    This ensures that all the character sequences (including those with combining marks) are
    consistently represented. For example, 'é' always matches 'é', even if composed differently.

    Args:
        trigram (str): 3-character sequence

    Returns:
        str: Unicode-normalized trigram
    """
    return unicodedata.normalize("NFC", trigram)

def get_trigrams(text, top_k=None):
    """
    This function generates all overlapping trigrams from the input text, removing spaces.

    Args:
        text (str): Cleaned sentence

    Returns:
        list: List of trigrams (strings)
    """
    text = text.replace(' ', '')
    return [normalize_trigram(text[i:i+3]) for i in range(len(text) - 2)]

def build_trigram_profile(text, top_k=None):
    """
    Here we build a normalized frequency profile (dictionary) of trigrams in the text.

    Args:
        text (str): Cleaned sentence or combined document
        top_k (int, optional): If set, keeps only the top_k most common trigrams

    Returns:
        dict: {trigram: relative frequency}
    """
    trigrams = get_trigrams(text)
    counts = Counter(trigrams)
    total = sum(counts.values())
    items = counts.most_common(top_k) if top_k else counts.items()
    return {k: v / total for k, v in items} if total > 0 else {}

def load_language_profiles(folder="profiles"):
    """
    This function Loads trigram frequency profiles from all .json files in the profiles folder.

    Args:
        folder (str): Path to folder of language profile .json files

    Returns:
        dict: {lang_code: profile_dict}
    """
    profiles = {}
    for file in os.listdir(folder):
        if file.endswith(".json"):
            lang = file[:-5]
            with open(os.path.join(folder, file), encoding="utf-8") as f:
                raw_profile = json.load(f)
                profile = {normalize_trigram(k): v for k, v in raw_profile.items()}
                profiles[lang] = profile
    return profiles

# #Dictionary of supported language codes and names
languages = {
    "en": "English",
    "fr": "French",
    "de": "German",
    "es": "Spanish",
    "it": "Italian",
    "pt": "Portuguese",
    "ru": "Russian",
    "zh": "Chinese",
    "ja": "Japanese",
    "ko": "Korean",
    "ar": "Arabic",
    "hi": "Hindi",
    "bn": "Bengali",
    "pa": "Punjabi",
    "ur": "Urdu",
    "vi": "Vietnamese",
    "th": "Thai",
    "tr": "Turkish",
    "id": "Indonesian",
    "fi": "Finnish",
    "no": "Norwegian",
    "da": "Danish",
    "nl": "Dutch",
    "pl": "Polish",
    "cs": "Czech",
    "hu": "Hungarian",
    "ro": "Romanian",
    "el": "Greek",
    "he": "Hebrew",
    "bg": "Bulgarian",
    "ta": "Tamil",
    "te": "Telugu",
    "gu": "Gujarati",
    "kn": "Kannada",
    "ml": "Malayalam",
    "mr": "Marathi",
    "or": "Odia",
    "as": "Assamese",
    "si": "Sinhala",
    "ne": "Nepali",
    "my": "Burmese"
}

