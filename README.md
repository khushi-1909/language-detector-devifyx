# 🌍 Language Detector — DevifyX ML Developer Intern Submission

**Author:** Khushi Verma  
**Email:** khushi1909@gmail.com  
**Date:** June 2025

---

## 📑 Table of Contents
- [Overview](#overview)
- [Supported Languages](#-supported-languages)
- [Project Folder Structure](#-project-folder-structure)
- [Installation & Usage](#installation--usage)
- [Example Usage](#-example-usage)
- [Sample Test Cases](#sample-test-cases)
- [Adding More Languages](#-adding-more-languages)
- [Output Format](#-output-format)
- [Video Demo](#-video-demo)
- [Design Notes](#-design-notes)
- [Acknowledgements](#acknowledgements)
- [About Me](#-about-me)


##  Overview

This project is my submission for the DevifyX ML Developer Intern assignment.  
The goal: build a language detector from scratch—no third-party detection libraries—supporting 40+ world languages and scripts, including many major Indian languages.

The system uses:
- **Trigram Cosine Similarity:** Matching a sentence to language profiles based on trigram frequency.
- **Naive Bayes Classification:** Machine learning with character trigrams.
- **Hybrid/Ensemble Model:** Combines both for even more robust detection.

All code is original, clearly commented, and modular—so it’s easy to understand, extend, and maintain.

---

## 🌐 Supported Languages

| Code | Language    |
|------|-------------|
| en   | English     |
| fr   | French      |
| de   | German      |
| es   | Spanish     |
| it   | Italian     |
| pt   | Portuguese  |
| ru   | Russian     |
| zh   | Chinese     |
| ja   | Japanese    |
| ko   | Korean      |
| ar   | Arabic      |
| hi   | Hindi       |
| bn   | Bengali     |
| pa   | Punjabi     |
| ur   | Urdu        |
| vi   | Vietnamese  |
| th   | Thai        |
| tr   | Turkish     |
| id   | Indonesian  |
| fi   | Finnish     |
| no   | Norwegian   |
| da   | Danish      |
| nl   | Dutch       |
| pl   | Polish      |
| cs   | Czech       |
| hu   | Hungarian   |
| ro   | Romanian    |
| el   | Greek       |
| he   | Hebrew      |
| bg   | Bulgarian   |
| ta   | Tamil       |
| te   | Telugu      |
| gu   | Gujarati    |
| kn   | Kannada     |
| ml   | Malayalam   |
| mr   | Marathi     |
| or   | Odia        |
| as   | Assamese    |
| si   | Sinhala     |
| ne   | Nepali      |
| my   | Burmese     |

---

## 🗂️ Project Folder Structure

```plaintext
language-detector-devifyx/
│
├── lang_utils.py
├── detect_language_cosine.py
├── detect_language_bayes.py
├── detector_combined.py
├── build_profiles.py
├── prepare_profiles.py
├── data/
├── profiles/
├── bayes_model.joblib
├── vectorizer.joblib
├── requirements.txt
├── README.md
└── test_cases.json (optional)
```

## Installation & Usage
**Step 1.** Install requirements:
```bash
pip install -r requirements.txt
```

**Step 2.** Run any detector:
Cosine Similarity:
```bash
python detect_language_cosine.py
```

Naive Bayes:
```bash
python detect_language_bayes.py
```

Hybrid/Ensemble:
```bash
python detector_combined.py
```
The script will prompt you for a sentence. Type your input and get instant JSON predictions
Type exit to quit.

## 📝 Example Usage
Input:
உங்கள் திட்டம் மிகவும் சிறந்தது!

Output:
{
  "language": "ta",
  "iso_code": "ta",
  "confidence": 0.88
}

## Sample Test Cases
| Input                                 | Expected | Predicted | Confidence |
|----------------------------------------|----------|-----------|------------|
| Good morning, how are you today?       | en       | en        | 0.97       |
| Bonjour tout le monde                  | fr       | fr        | 0.95       |
| Wie spät ist es jetzt?                 | de       | de        | 0.92       |
| ¿Cómo te llamas?                       | es       | es        | 0.96       |
| यह परीक्षा आसान है।                       | hi       | hi        | 0.91       |
| আমি তোমাকে ভালোবাসি                   | bn       | bn        | 0.93       |
| ما اسمك؟                               | ar       | ar        | 0.92       |
| 我喜欢学习新语言                         | zh       | zh        | 0.90       |
| 私の名前はサクラです                     | ja       | ja        | 0.92       |
| Сегодня отличная погода                | ru       | ru        | 0.94       |
| Olá, como vai você?                    | pt       | pt        | 0.96       |
| Ciao, piacere di conoscerti            | it       | it        | 0.94       |
| நான் தமிழில் பேசுகிறேன்             | ta       | ta        | 0.90       |
| నేను తెలుగు మాట్లాడుతాను                | te       | te        | 0.88       |
| मेरा घर पुणे में है                          | mr       | mr        | 0.89       |
| Ich kann ein bisschen Deutsch sprechen | de       | de        | 0.93       |
| मैं गणित सीख रहा हूँ                       | hi       | hi        | 0.91       |
| Ce este numele tău?                    | ro       | ro        | 0.92       |
| איך קוראים לך?                        | he       | he        | 0.90       |
| Πώς είσαι σήμερα;                      | el       | el        | 0.92       |


##  Adding More Languages
- Add a `.txt` file for your new language (named with its ISO code) to `data/`
- Update the languages dictionary in `lang_utils.py`
- Run `build_profiles.py` to generate the new trigram profile
- Retrain the Naive Bayes model (simply run `detect_language_bayes.py`; it auto-trains if needed)
- Done!


##  Retraining the Naive Bayes Model
Whenever you add or update data:
python detect_language_bayes.py

If model files are missing, the script will train and save a new model automatically.

##  Output Format
All models output predictions in the following JSON format:
{
  "language": "fr",
  "iso_code": "fr",
  "confidence": 0.94
}

## 📊 Final Evaluation

Using 40 real-world test sentences—one from each supported language and excluding proper nouns—the ensemble model achieved an overall accuracy of **82.5%**.

=====================================================================================================
Input                                                           | Expected | Predicted | Result
=====================================================================================================
كلا تتحدث وكأن الأمر انتهى                                      | ar       | ar       | ✅
চনকত হৱ পৰত মল পৰতসথপন কৰৰ আগত                          | as       | bn       | ❌
предполагам                                                     | bg       | bg       | ✅
লপ সনকত হয়ছ                                                  | bn       | bn       | ✅
dej mi pokoj                                                    | cs       | pl       | ❌
så let er det ikke                                              | da       | no       | ❌
gab mir gute rückmeldungen ein                                  | de       | de       | ✅
είσαι χάλια                                                     | el       | el       | ✅
protocolo facultativo y enmien                                  | es       | es       | ✅
tässä toinen pitäisitte siitä                                   | fi       | fi       | ✅
le passé et le futur et puis a                                  | fr       | fr       | ✅
શરષઠસરકષત ચલ સથ સરળ રબટ૨                                    | gu       | ar       | ❌
לעזאזל דוסון                                                   | he       | he       | ✅
ashitaka  समरई ironworks पर हम                                 | hi       | hi       | ✅
maga nagyon különös ember                                       | hu       | hu       | ✅
waktu menghitung dan terus men                                  | id       | id       | ✅
nomenclatura dei paesi stabili                                  | it       | it       | ✅
香港　飛行機のエコノミーで16時間                                   | ja       | ja       | ✅
ಪರವನಯಜತ ಸಚತರತ ಗರಫಕಸ ವಯವಸಥಗ ಬದಲ                   | kn       | kn       | ✅
주님의 응벌을 두려워 하는 자들이라                                 | ko       | ko       | ✅
ന കണണടതയരനന അങങരനനകകണട എഴതചച ആ       | ml       | ml       | ✅
सकरल पटट लपव                                                   | mr       | hi       | ❌
s က s အဖစ ပငပနလပပ                                            | my       | cs       | ❌
करम सत कषतरहर                                                  | ne       | hi       | ❌
een domme duitser beschoot me                                    | nl       | nl       | ✅
vi kan ikke dra herfra                                           | no       | no       | ✅
ସଭ ସଚନ ପଠଇବର ଅସମରଥ ସଭ ଅବସଥତ ନହ                            | or       | or       | ✅
ਈਮਜ dvd ਉਤ ਲਖਆ ਜ ਰਹ ਹ                                        | pa       | pa       | ✅
jasne jasne                                                      | pl       | pl       | ✅
preciso de sua assinatura niss                                   | pt       | pt       | ✅
vor să instrui formatori                                         | ro       | ro       | ✅
разговариваете                                                   | ru       | ru       | ✅
කමර දකකන පනනනව අහමබන වග දරකථන                      | si       | si       | ✅
பன தஙகவடட நடடபபறதத அரபகளடம நஙக                  | ta       | ta       | ✅
ఇకకడ ఒపపద వరతల                                              | te       | te       | ✅
ไมไดหรอก เพลงอยในหองฉน                                           | th       | th       | ✅
seni tekrar görmek güzeldi ve                                    | tr       | tr       | ✅
انہوں نے کہا کہ ہم ایک مجرم قو                                 | ur       | ur       | ✅
ở đây chúng tôi không phục vụ                                    | vi       | vi       | ✅
提交人 hst由律师代理                                              | zh       | zh       | ✅
==================================================================================================
✅ Accuracy: 33/40 = 82.50%
==================================================================================================

These results highlight the model’s robustness across Latin and non-Latin scripts and show that even simple trigram-based methods, when combined smartly, can produce strong multilingual classification.


## 📹 Video Demo
A short demo video (under 10 MB) showing all three models in action, including detection of various scripts, is included in this submission as required.

##  Design Notes
-Handles Latin and non-Latin scripts natively (including Indian and East Asian languages).
-All core logic is in lang_utils.py for easy expansion and maintenance.
-No black-box dependencies—transparent code throughout.
-The ensemble model is robust even if the two methods disagree.

##  Acknowledgements
Thank you to the DevifyX team for the engaging challenge.
Working on this project taught me a lot about multilingual NLP and real-world language diversity.

## 👩‍💻 About Me
Built by Khushi Verma
LinkedIn: https://www.linkedin.com/in/khushi-verma-1a44a722b/
For any questions, feel free to email me at ae21b035@smail.iitm.ac.in