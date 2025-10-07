#!/usr/bin/env python3
"""
Test script for ML models functionality
"""

import requests
import json
import sys

# Test configuration
BASE_URL = "http://localhost:8000"
ML_ENDPOINT = "/ml/predict"

def test_ml_model_manual_input():
    """Test ML model with manual KOI feature input"""
    print("Testing ML model with manual KOI features...")
    
    # Test data with KOI features
    test_request = {
        "model": "gb",
        "datasource": "manual",
        "kepid": "3219037",
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
        response = requests.post(f"{BASE_URL}{ML_ENDPOINT}", json=test_request)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("Response:")
            print(json.dumps(result, indent=2))
            
            # Validate response format
            if "candidate_probability" in result and "non_candidate_probability" in result:
                print("✅ Response format is correct!")
                print(f"Candidate probability: {result['candidate_probability']}")
                print(f"Non-candidate probability: {result['non_candidate_probability']}")
            else:
                print("❌ Response format is incorrect")
        else:
            print(f"❌ Request failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error during request: {str(e)}")

def test_ml_model_test_data():
    """Test ML model with test data source"""
    print("\nTesting ML model with test data source...")
    
    test_request = {
        "model": "svm",
        "datasource": "test",
        "kepid": "3219037",
        "predict": True
    }
    
    try:
        response = requests.post(f"{BASE_URL}{ML_ENDPOINT}", json=test_request)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("Response:")
            print(json.dumps(result, indent=2))
            
            # Validate response format
            if "candidate_probability" in result and "non_candidate_probability" in result:
                print("✅ Response format is correct!")
                print(f"Candidate probability: {result['candidate_probability']}")
                print(f"Non-candidate probability: {result['non_candidate_probability']}")
            else:
                print("❌ Response format is incorrect")
        else:
            print(f"❌ Request failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error during request: {str(e)}")

def test_models_endpoint():
    """Test the models listing endpoint"""
    print("\nTesting /ml/models endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/ml/models")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("Available models:")
            print(json.dumps(result, indent=2))
        else:
            print(f"❌ Request failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error during request: {str(e)}")

def test_features_endpoint():
    """Test the features listing endpoint"""
    print("\nTesting /ml/features endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/ml/features")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("Required features:")
            print(json.dumps(result, indent=2))
        else:
            print(f"❌ Request failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error during request: {str(e)}")

if __name__ == "__main__":
    print("🧪 Testing ML Models Functionality")
    print("=" * 50)
    
    # Test all endpoints
    test_models_endpoint()
    test_features_endpoint()
    test_ml_model_manual_input()
    test_ml_model_test_data()
    
    print("\n" + "=" * 50)
    print("🏁 Test completed!")