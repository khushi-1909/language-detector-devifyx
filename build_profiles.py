import os
import json
from collections import Counter
from pathlib import Path

def get_trigrams(text):
    text=text.replace(' ', '')
    return [text[i:i+3] for i in range(len(text) - 2)]

def build_profile(text, top_k=300):
    trigrams=get_trigrams(text)
    counter=Counter(trigrams)
    total=sum(counter.values())
    profile={k:v/total for k, v in counter.most_common(top_k)}
    return profile

def main():
    data_dir=Path("data")
    output_dir=Path('profiles')
    output_dir.mkdir(exist_ok=True)

    for file in data_dir.glob("*.txt"):
        lang_code = file.stem
        with file.open(encoding="utf-8") as f:
            text = f.read().replace("\n", " ")
        profile = build_profile(text)
        with open(output_dir / f"{lang_code}.json", "w", encoding="utf-8") as out:
            json.dump(profile, out, ensure_ascii=False, indent=2)
        print(f"✅ Profile saved for {lang_code}")

if __name__ == "__main__":
    main()