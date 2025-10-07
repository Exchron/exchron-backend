"""
Final verification test for both API formats
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_manual_format():
    """Test the manual format (backward compatibility)"""
    print("🧪 Testing MANUAL format...")
    
    data = {
        "model": "svm",
        "datasource": "manual",
        "features": {
            "koi_period": 10.005,
            "koi_time0bk": 136.83,
            "koi_impact": 0.148,
            "koi_duration": 3.481,
            "koi_depth": 143.3,
            "koi_incl": 89.61,
            "koi_model_snr": 11.4,
            "koi_count": 2,
            "koi_bin_oedp_sig": 0.461,
            "koi_steff": 5912.0,
            "koi_slogg": 4.453,
            "koi_srad": 0.924,
            "koi_smass": 0.884,
            "koi_kepmag": 14.634
        },
        "predict": True
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/ml/predict", json=data, timeout=15)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Manual format: SUCCESS")
            print(f"   Candidate Probability: {result['candidate_probability']:.4f}")
            return True
        else:
            print(f"❌ Manual format failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Manual format error: {e}")
        return False

def test_preloaded_format():
    """Test the new pre-loaded format"""
    print("\n🧪 Testing PRE-LOADED format...")
    
    data = {
        "model": "svm",
        "datasource": "pre-loaded",
        "data": "kepler",
        "predict": True
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/ml/predict", json=data, timeout=15)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Pre-loaded format: SUCCESS")
            print(f"   Average Candidate Prob: {result['candidate_probability']:.4f}")
            print(f"   Individual predictions: {len([k for k in result.keys() if k not in ['candidate_probability', 'non_candidate_probability']])} records")
            return True
        else:
            print(f"❌ Pre-loaded format failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Pre-loaded format error: {e}")
        return False

def check_server():
    """Check if server is running"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running")
            return True
    except:
        print("❌ Server not responding")
        return False

if __name__ == "__main__":
    print("🚀 Final API Verification Test")
    print("=" * 40)
    
    if not check_server():
        print("\n❌ Server is not running. Please start with:")
        print("uvicorn app.main:app --reload --host 127.0.0.1 --port 8000")
        exit(1)
    
    manual_ok = test_manual_format()
    preloaded_ok = test_preloaded_format()
    
    print("\n" + "=" * 40)
    if manual_ok and preloaded_ok:
        print("🎉 ALL TESTS PASSED! API is working correctly.")
        print("\n📋 For Swagger UI, use the examples in SWAGGER_TROUBLESHOOTING.md")
    else:
        print("⚠️  Some tests failed. Check the error messages above.")