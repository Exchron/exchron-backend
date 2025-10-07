"""
Complete test of the ML API functionality
"""
import requests
import json

BASE_URL = "http://localhost:8001"

def test_manual_prediction():
    """Test ML model with manual KOI features"""
    print("🧪 Testing ML Prediction with Manual KOI Features")
    print("=" * 60)
    
    # Test request with the exact format specified
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
    
    print("Request:")
    print(json.dumps(test_request, indent=2))
    
    try:
        response = requests.post(f"{BASE_URL}/ml/predict", json=test_request)
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ SUCCESS - Response:")
            print(json.dumps(result, indent=2))
            
            # Validate response format matches specification
            if "candidate_probability" in result and "non_candidate_probability" in result:
                print(f"\n✅ Response format matches specification!")
                print(f"📊 Candidate probability: {result['candidate_probability']}")
                print(f"📊 Non-candidate probability: {result['non_candidate_probability']}")
                
                # Verify probabilities sum to ~1
                total_prob = result['candidate_probability'] + result['non_candidate_probability']
                print(f"📊 Total probability: {total_prob:.6f}")
                
                if abs(total_prob - 1.0) < 0.001:
                    print("✅ Probabilities sum to 1.0 correctly!")
                else:
                    print("⚠️  Probabilities don't sum to 1.0")
            else:
                print("❌ Response format incorrect - missing required fields")
        else:
            print(f"❌ Request failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error during request: {str(e)}")

def test_svm_prediction():
    """Test SVM model with manual KOI features"""
    print("\n\n🧪 Testing SVM Model")
    print("=" * 60)
    
    test_request = {
        "model": "svm",
        "datasource": "manual",
        "features": {
            "koi_period": 2.42186898,
            "koi_time0bk": 132.7886605,
            "koi_impact": 0.0,  # NaN in original, using 0
            "koi_duration": 6.22,
            "koi_depth": 0.0,   # NaN in original, using 0
            "koi_incl": 0.0,    # NaN in original, using 0
            "koi_model_snr": 0.0,  # NaN in original, using 0
            "koi_count": 1,
            "koi_bin_oedp_sig": 0.0,  # NaN in original, using 0
            "koi_steff": 0.0,   # NaN in original, using 0
            "koi_slogg": 0.0,   # NaN in original, using 0
            "koi_srad": 0.0,    # NaN in original, using 0
            "koi_smass": 0.0,   # NaN in original, using 0
            "koi_kepmag": 13.583
        },
        "predict": True
    }
    
    try:
        response = requests.post(f"{BASE_URL}/ml/predict", json=test_request)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SVM Response:")
            print(json.dumps(result, indent=2))
        else:
            print(f"❌ Request failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error during request: {str(e)}")

def test_test_datasource():
    """Test using test datasource with kepid from KOI data"""
    print("\n\n🧪 Testing Test Datasource")
    print("=" * 60)
    
    test_request = {
        "model": "gb",
        "datasource": "test",
        "kepid": "3219037",  # This should exist in KOI data
        "predict": True
    }
    
    try:
        response = requests.post(f"{BASE_URL}/ml/predict", json=test_request)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Test Datasource Response:")
            print(json.dumps(result, indent=2))
        else:
            print(f"❌ Request failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error during request: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting Complete ML API Test")
    print("=" * 80)
    
    test_manual_prediction()
    test_svm_prediction()
    test_test_datasource()
    
    print("\n" + "=" * 80)
    print("🏁 Complete test finished!")
    print("\nExpected Response Format:")
    print('{')
    print('  "candidate_probability": 0.051923830062150955,')
    print('  "non_candidate_probability": 0.948076169937849')
    print('}')