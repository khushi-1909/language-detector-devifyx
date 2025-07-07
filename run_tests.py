import json
from lang_utils import load_language_profiles
from detector_combined import ensemble_predict

def run_tests():
    # Load test cases
    with open("test_cases.json", "r", encoding="utf-8") as f:
        test_cases = json.load(f)

    profiles = load_language_profiles("profiles")
    
    correct = 0
    total = len(test_cases)
    
    print("="*60)
    print(f"{'Input':30} | {'Expected':8} | {'Predicted':8} | Result")
    print("="*60)

    for case in test_cases:
        input_text = case["input"]
        expected = case["expected_iso"]
        
        try:
            result = ensemble_predict(input_text, profiles)
            predicted = result["iso_code"]
        except Exception as e:
            predicted = "ERR"
            print(f"❌ Error for input: {input_text}\n{str(e)}")

        status = "✅" if predicted == expected else "❌"
        if predicted == expected:
            correct += 1

        print(f"{input_text[:30]:30} | {expected:8} | {predicted:8} | {status}")
    
    accuracy = correct / total * 100
    print("="*60)
    print(f"✅ Accuracy: {correct}/{total} = {accuracy:.2f}%")
    print("="*60)

if __name__ == "__main__":
    run_tests()
