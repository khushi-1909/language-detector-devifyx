"""
Trigram Profile Builder

This script reads all .txt language files in 'data/', builds normalized trigram frequency
profiles for each, and saves them as .json files in the 'profiles/' directory.

Run this script whenever you add new data or new languages!
"""

import os
import json
from lang_utils import build_trigram_profile, clean_text

def build_all_profiles(data_dir="data", output_dir="profiles", top_k=300):
    """
    For each .txt file in the data directory:
    - Read all lines and join them into one text blob
    - Clean the text
    - Build trigram profile (which are optionally limited to top_k)
    - Save as .json in output directory
    """
    os.makedirs(output_dir, exist_ok=True)
    for file in os.listdir(data_dir):
        if file.endswith(".txt"):
            lang_code = file[:-4]
            with open(os.path.join(data_dir, file), encoding="utf-8") as f:
                text = f.read().replace("\n", " ")
            text = clean_text(text)
            profile = build_trigram_profile(text, top_k=top_k)
            output_path = os.path.join(output_dir, f"{lang_code}.json")
            with open(output_path, "w", encoding="utf-8") as out:
                json.dump(profile, out, ensure_ascii=False, indent=2)
            print(f"✅ Profile saved for {lang_code} ({len(profile)} trigrams)")

if __name__ == "__main__":
    print("=" * 50)
    print("Building trigram language profiles for all the languages in 'data/'...")
    print("=" * 50)
    build_all_profiles()
    print("All profiles are built! You can now run the detectors.")