from datasets import load_dataset, get_dataset_config_names
import os
import re

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
}

non_latin_langs = {
    "zh", "ja", "ko", "ar", "hi", "bn", "pa", "ur", "el", "he", "ru", "th", "bg"
}

os.makedirs("data", exist_ok=True)

def clean_text(text):
    text = re.sub(r"[^\w\s]", "", text)  # remove punctuation
    return text.strip().lower()

def is_mostly_non_latin(text):
    latin_chars = re.findall(r"[a-zA-Z]", text)
    return len(latin_chars) / max(1, len(text)) < 0.5

def fetch_and_save(lang_code, max_samples=1500):
    try:
        if lang_code == "en":
            print("Skipping English (used as source only)")
            return

        configs = get_dataset_config_names("opus100")
        pair1 = f"en-{lang_code}"
        pair2 = f"{lang_code}-en"

        if pair1 in configs:
            selected_pair = pair1
            extract_lang = lang_code
        elif pair2 in configs:
            selected_pair = pair2
            extract_lang = lang_code
        else:
            print(f"❌ No config found for {lang_code}")
            return

        print(f"✅ Using {selected_pair} → extracting '{extract_lang}'")

        ds = load_dataset("opus100", selected_pair, split="train", streaming=True)
        iterator = iter(ds)

        samples = []
        for _ in range(max_samples * 5):  # oversample buffer
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

        with open(f"data/{lang_code}.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(samples))

        print(f"✅ Saved {len(samples)} lines for '{lang_code}'")

    except Exception as e:
        print(f"❌ Error for {lang_code}: {e}")

if __name__ == "__main__":
    for code in languages:
        fetch_and_save(code)
