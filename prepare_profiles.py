"""
Language Data Preparer

This script downloads or loads sentence data for all specified languages,
filters and cleans it, and saves each as a `.txt` file in the `data/` folder.
THis is especially useful for collecting parallel or monolingual text for new scripts.

Edit the 'languages' and 'non_latin' sets to cover more languages as needed.
"""

from datasets import load_dataset, get_dataset_config_names
import os
import re
from lang_utils import clean_text, languages

# Set of Languages that dont use the latin alphabet
non_latin_langs = {
    "zh", "ja", "ko", "ar", "hi", "bn", "pa", "ur", "el", "he", "ru", "th", 
    "bg", "ta", "te", "kn", "gu", "ml", "mr", "or", "as", "si", "ne", "my"
}

def is_mostly_non_latin(text):
    """
    Returns True if less than half the characters are Latin letters.
    this is useful to filter out the non-Latin-script sentences when preparing profiles.
    """
    latin_chars = re.findall(r"[a-zA-Z]", text)
    return len(latin_chars) / max(1, len(text)) < 0.5

def get_data(lang_code, max_samples=1500):
    """
    Downloads or loads parallel text from HuggingFace Datasets (opus100),
    cleans and filters sentences, and saves a .txt file for each language.

    Skips English (source language). Gives a warning if not enough samples are found.
    """
    try:
        if lang_code == "en":
            print("Skipping English (used as source only)")
            return

        configs = get_dataset_config_names("opus100")
        config1 = f"en-{lang_code}"
        config2 = f"{lang_code}-en"

        if config1 in configs:
            selected_pair = config1
            extract_lang = lang_code
        elif config2 in configs:
            selected_pair = config2
            extract_lang = lang_code
        else:
            print(f"❌ No data was found for {lang_code} ({languages.get(lang_code, lang_code)})")
            return

        print(f"Fetching {lang_code} ({languages.get(lang_code, lang_code)}) data from {selected_pair}...")

        ds = load_dataset("opus100", selected_pair, split="train", streaming=True)
        iterator = iter(ds)
        samples = []
        #Buffering for extra filtering by trying 5 times more sqamples than needed
        for _ in range(max_samples * 5):  
            try:
                item = next(iterator)
                if "translation" in item and extract_lang in item["translation"]:
                    text = clean_text(item["translation"][extract_lang])
                    if len(text) >= 10:
                        if lang_code in non_latin_langs:
                            if is_mostly_non_latin(text):
                                samples.append(text)
                        else:
                            samples.append(text)
                if len(samples) >= max_samples:
                    break
            except StopIteration:
                break
        
        # Saving samples to file
        os.makedirs("data", exist_ok=True)
        out_path = os.path.join("data", f"{lang_code}.txt")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write('\n'.join(samples))
        print(f"✅ Saved {len(samples)} lines for {lang_code}")

        if len(samples) < max_samples:
            print(f"⚠️ Only {len(samples)} samples for {lang_code}. You may want to find more data.")
    except Exception as e:
        print(f"Error fetching data for {lang_code}: {e}")

        with open(f"data/{lang_code}.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(samples))

        print(f"✅ Saved {len(samples)} lines for '{lang_code}'")

    except Exception as e:
        print(f"❌ Error for {lang_code}: {e}")

if __name__ == "__main__":
    print("=" * 55)
    print("Preparing the raw language data for trigram profile building.")
    print("You can edit 'languages' or 'non_latin' in this script to add new languages/scripts.")
    print("=" * 55)
    for code in languages:
        get_data(code)
    print("All data files are ready. \n Next: run build_profiles.py to create language profiles.")