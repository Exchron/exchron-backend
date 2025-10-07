"""Comprehensive test of all API functionality"""

import requests
import json

BASE_URL = "http://localhost:8000"

def comprehensive_test():
    """Test all API functionality including new and existing formats"""
    
    print("🚀 Comprehensive API Test")
    print("=" * 50)
    
    # Test 1: New pre-loaded format with GB model
    print("\n1. Testing NEW FORMAT - GB model with pre-loaded Kepler data")
    test1 = {
        "model": "gb",
        "datasource": "pre-loaded",
        "data": "kepler", 
        "predict": True
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/ml/predict", json=test1, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS")
            print(f"   Average Candidate Prob: {result['candidate_probability']:.4f}")
            print(f"   Individual predictions: {len([k for k in result.keys() if k not in ['candidate_probability', 'non_candidate_probability']])} records")
            print(f"   First record KepID: {result['first']['kepid']}")
            print(f"   Last record KepID: {result['tenth']['kepid']}")
        else:
            print(f"❌ FAILED: {response.status_code}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    # Test 2: New format with SVM and TESS
    print("\n2. Testing NEW FORMAT - SVM model with pre-loaded TESS data")
    test2 = {
        "model": "svm",
        "datasource": "pre-loaded", 
        "data": "tess",
        "predict": True
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/ml/predict", json=test2, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS")
            print(f"   Average Candidate Prob: {result['candidate_probability']:.4f}")
        else:
            print(f"❌ FAILED: {response.status_code}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    # Test 3: Traditional manual features (backward compatibility)
    print("\n3. Testing BACKWARD COMPATIBILITY - Manual features")
    test3 = {
        "model": "gb",
        "datasource": "manual",
        "features": {
            "koi_period": 3.5, "koi_time0bk": 132.0, "koi_impact": 0.15,
            "koi_duration": 3.0, "koi_depth": 100.0, "koi_incl": 89.0,
            "koi_model_snr": 15.0, "koi_count": 1, "koi_bin_oedp_sig": 0.5,
            "koi_steff": 5500.0, "koi_slogg": 4.5, "koi_srad": 1.0,
            "koi_smass": 1.0, "koi_kepmag": 14.0
        },
        "predict": True
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/ml/predict", json=test3, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS")
            print(f"   Candidate Prob: {result['candidate_probability']:.4f}")
        else:
            print(f"❌ FAILED: {response.status_code}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    # Test 4: Error handling - missing data field
    print("\n4. Testing ERROR HANDLING - Missing data field")
    test4 = {
        "model": "gb",
        "datasource": "pre-loaded",
        # Missing "data" field
        "predict": True
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/ml/predict", json=test4, timeout=30)
        if response.status_code == 400:
            print("✅ SUCCESS - Proper validation error")
            print(f"   Error message: {response.json()['detail']}")
        else:
            print(f"❌ UNEXPECTED: {response.status_code}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    # Test 5: API endpoints availability
    print("\n5. Testing API ENDPOINTS")
    endpoints = [
        ("/", "Root"),
        ("/health", "Health Check"),
        ("/api/ml/models", "ML Models List"),
        ("/docs", "Documentation")
    ]
    
    for endpoint, name in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
            if response.status_code == 200:
                print(f"   ✅ {name}: Available")
            else:
                print(f"   ❌ {name}: {response.status_code}")
        except Exception as e:
            print(f"   ❌ {name}: Error - {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Comprehensive testing completed!")

if __name__ == "__main__":
    comprehensive_test()