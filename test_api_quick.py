import requests
import json

BASE_URL = "http://localhost:8001"

# Test the models endpoint
try:
    response = requests.get(f"{BASE_URL}/ml/models")
    print("ML Models endpoint:")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*50 + "\n")

# Test the features endpoint
try:
    response = requests.get(f"{BASE_URL}/ml/features")
    print("ML Features endpoint:")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*50 + "\n")

# Test manual input (this will fail due to missing model files, but will show the API structure)
test_manual = {
    "model": "gb",
    "datasource": "manual",
    "features": {
        "koi_period": 10.00506974,
        "koi_time0bk": 136.83029,
        "koi_impact": 0.148,
        "koi_duration": 3.481,
        "koi_depth": 143.3,
        "koi_incl": 89.61,
        "koi_model_snr": 11.4,
        "koi_count": 2,
        "koi_bin_oedp_sig": 0.4606,
        "koi_steff": 5912,
        "koi_slogg": 4.453,
        "koi_srad": 0.924,
        "koi_smass": 0.884,
        "koi_kepmag": 14.634
    },
    "predict": True
}

try:
    response = requests.post(f"{BASE_URL}/ml/predict", json=test_manual)
    print("Manual prediction test:")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")