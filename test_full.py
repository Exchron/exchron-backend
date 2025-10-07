#!/usr/bin/env python3
"""
Comprehensive test script for all API endpoints and functionality
Tests all models with different data sources and scenarios
"""

import requests
import json
import sys
import time
from typing import Dict, Any

# Test configuration
BASE_URL = "http://localhost:8000"
DL_ENDPOINT = "/api/dl/predict"
ML_ENDPOINT = "/api/ml/predict"

# Sample Kepler IDs from available data
SAMPLE_KEPLER_IDS = [
    "10000490", "10002261", "10002866", "10004738", "10006096",
    "10015516", "10016874", "10020423", "10024051", "10026457"
]

# Sample KOI features for manual input
SAMPLE_KOI_FEATURES = {
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
}

# Alternative KOI features for testing variety
ALTERNATIVE_KOI_FEATURES = {
    "koi_period": 9.7423156,
    "koi_time0bk": 122.28385,
    "koi_impact": 0.251,
    "koi_duration": 4.125,
    "koi_depth": 289.7,
    "koi_incl": 87.34,
    "koi_model_snr": 18.7,
    "koi_count": 3,
    "koi_bin_oedp_sig": 0.812,
    "koi_steff": 6142,
    "koi_slogg": 4.298,
    "koi_srad": 1.087,
    "koi_smass": 1.156,
    "koi_kepmag": 13.891
}

def print_section(title: str):
    """Print a formatted section header"""
    print("\n" + "=" * 80)
    print(f" {title}")
    print("=" * 80)

def print_test(test_name: str):
    """Print a formatted test header"""
    print(f"\n🧪 Testing: {test_name}")
    print("-" * 60)

def make_request(endpoint: str, data: Dict[str, Any], test_name: str) -> bool:
    """Make a request and display results"""
    try:
        print(f"📤 Request to: {BASE_URL}{endpoint}")
        print(f"📋 Request data: {json.dumps(data, indent=2)}")
        
        response = requests.post(f"{BASE_URL}{endpoint}", json=data)
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Success! Response:")
            print(json.dumps(result, indent=2))
            
            # Validate expected response structure based on endpoint
            if endpoint == DL_ENDPOINT:
                required_fields = ["candidate_probability", "non_candidate_probability", "kepid", "model_used"]
                if all(field in result for field in required_fields):
                    print("✅ DL Response structure is valid")
                    return True
                else:
                    print("❌ DL Response missing required fields")
                    return False
            elif endpoint == ML_ENDPOINT:
                if "predictions" in result:
                    # Upload response format
                    if "candidate_probability" in result and "predictions" in result:
                        print("✅ Upload ML Response structure is valid")
                        return True
                elif "first" in result:
                    # Pre-loaded response format
                    if "candidate_probability" in result and "first" in result:
                        print("✅ Pre-loaded ML Response structure is valid")
                        return True
                elif "candidate_probability" in result:
                    # Standard ML response format
                    print("✅ Standard ML Response structure is valid")
                    return True
                else:
                    print("❌ ML Response structure is invalid")
                    return False
        else:
            print(f"❌ Request failed with status code: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error details: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Error text: {response.text}")
            return False
                
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Make sure the server is running on localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

def test_basic_endpoints():
    """Test basic informational endpoints"""
    print_section("BASIC ENDPOINT TESTS")
    
    endpoints = [
        "/",
        "/health", 
        "/models",
        "/api/dl/models",
        "/api/dl/available-ids",
        "/api/ml/models",
        "/api/ml/features"
    ]
    
    for endpoint in endpoints:
        print_test(f"GET {endpoint}")
        try:
            response = requests.get(f"{BASE_URL}{endpoint}")
            print(f"📊 Status Code: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print("✅ Success! Response:")
                print(json.dumps(result, indent=2))
            else:
                print(f"❌ Request failed: {response.text}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")

def test_cnn_with_kepler_ids():
    """Test CNN model with Kepler IDs"""
    print_section("CNN MODEL TESTS WITH KEPLER IDs")
    
    for i, kepid in enumerate(SAMPLE_KEPLER_IDS[:3]):  # Test first 3 IDs
        test_name = f"CNN Prediction for Kepler ID {kepid}"
        print_test(test_name)
        
        request_data = {
            "model": "cnn",
            "kepid": kepid,
            "predict": True
        }
        
        success = make_request(DL_ENDPOINT, request_data, test_name)
        if success:
            print(f"✅ CNN test {i+1}/3 passed")
        else:
            print(f"❌ CNN test {i+1}/3 failed")
        
        # Small delay between requests
        time.sleep(1)

def test_dnn_with_kepler_ids():
    """Test DNN model with Kepler IDs"""
    print_section("DNN MODEL TESTS WITH KEPLER IDs")
    
    for i, kepid in enumerate(SAMPLE_KEPLER_IDS[3:6]):  # Test next 3 IDs
        test_name = f"DNN Prediction for Kepler ID {kepid}"
        print_test(test_name)
        
        request_data = {
            "model": "dnn",
            "kepid": kepid,
            "predict": True
        }
        
        success = make_request(DL_ENDPOINT, request_data, test_name)
        if success:
            print(f"✅ DNN test {i+1}/3 passed")
        else:
            print(f"❌ DNN test {i+1}/3 failed")
        
        # Small delay between requests
        time.sleep(1)

def test_gb_manual_entry():
    """Test Gradient Boosting with manual data entry"""
    print_section("GRADIENT BOOSTING (GB) - MANUAL DATA ENTRY TESTS")
    
    # Test 1: Standard manual entry
    print_test("GB with Manual KOI Features (Set 1)")
    request_data = {
        "model": "gb",
        "datasource": "manual",
        "features": SAMPLE_KOI_FEATURES,
        "predict": True
    }
    
    success = make_request(ML_ENDPOINT, request_data, "GB Manual Entry 1")
    if success:
        print("✅ GB Manual test 1 passed")
    else:
        print("❌ GB Manual test 1 failed")
    
    time.sleep(1)
    
    # Test 2: Alternative manual entry
    print_test("GB with Manual KOI Features (Set 2)")
    request_data = {
        "model": "gb",
        "datasource": "manual",
        "features": ALTERNATIVE_KOI_FEATURES,
        "predict": True
    }
    
    success = make_request(ML_ENDPOINT, request_data, "GB Manual Entry 2")
    if success:
        print("✅ GB Manual test 2 passed")
    else:
        print("❌ GB Manual test 2 failed")

def test_svm_manual_entry():
    """Test Support Vector Machine with manual data entry"""
    print_section("SUPPORT VECTOR MACHINE (SVM) - MANUAL DATA ENTRY TESTS")
    
    # Test 1: Standard manual entry
    print_test("SVM with Manual KOI Features (Set 1)")
    request_data = {
        "model": "svm",
        "datasource": "manual",
        "features": SAMPLE_KOI_FEATURES,
        "predict": True
    }
    
    success = make_request(ML_ENDPOINT, request_data, "SVM Manual Entry 1")
    if success:
        print("✅ SVM Manual test 1 passed")
    else:
        print("❌ SVM Manual test 1 failed")
    
    time.sleep(1)
    
    # Test 2: Alternative manual entry
    print_test("SVM with Manual KOI Features (Set 2)")
    request_data = {
        "model": "svm",
        "datasource": "manual",
        "features": ALTERNATIVE_KOI_FEATURES,
        "predict": True
    }
    
    success = make_request(ML_ENDPOINT, request_data, "SVM Manual Entry 2")
    if success:
        print("✅ SVM Manual test 2 passed")
    else:
        print("❌ SVM Manual test 2 failed")

def test_gb_preloaded_data():
    """Test Gradient Boosting with pre-loaded data"""
    print_section("GRADIENT BOOSTING (GB) - PRE-LOADED DATA TESTS")
    
    # Test with Kepler data
    print_test("GB with Pre-loaded Kepler Data")
    request_data = {
        "model": "gb",
        "datasource": "pre-loaded", 
        "data": "kepler",
        "predict": True
    }
    
    success = make_request(ML_ENDPOINT, request_data, "GB Pre-loaded Kepler")
    if success:
        print("✅ GB Pre-loaded Kepler test passed")
    else:
        print("❌ GB Pre-loaded Kepler test failed")
    
    time.sleep(1)
    
    # Test with TESS data
    print_test("GB with Pre-loaded TESS Data")
    request_data = {
        "model": "gb",
        "datasource": "pre-loaded",
        "data": "tess", 
        "predict": True
    }
    
    success = make_request(ML_ENDPOINT, request_data, "GB Pre-loaded TESS")
    if success:
        print("✅ GB Pre-loaded TESS test passed")
    else:
        print("❌ GB Pre-loaded TESS test failed")

def test_svm_preloaded_data():
    """Test Support Vector Machine with pre-loaded data"""
    print_section("SUPPORT VECTOR MACHINE (SVM) - PRE-LOADED DATA TESTS")
    
    # Test with Kepler data
    print_test("SVM with Pre-loaded Kepler Data")
    request_data = {
        "model": "svm",
        "datasource": "pre-loaded",
        "data": "kepler",
        "predict": True
    }
    
    success = make_request(ML_ENDPOINT, request_data, "SVM Pre-loaded Kepler")
    if success:
        print("✅ SVM Pre-loaded Kepler test passed")
    else:
        print("❌ SVM Pre-loaded Kepler test failed")
    
    time.sleep(1)
    
    # Test with TESS data
    print_test("SVM with Pre-loaded TESS Data")
    request_data = {
        "model": "svm",
        "datasource": "pre-loaded",
        "data": "tess",
        "predict": True
    }
    
    success = make_request(ML_ENDPOINT, request_data, "SVM Pre-loaded TESS")
    if success:
        print("✅ SVM Pre-loaded TESS test passed")
    else:
        print("❌ SVM Pre-loaded TESS test failed")

def test_gb_uploaded_data():
    """Test Gradient Boosting with uploaded data format"""
    print_section("GRADIENT BOOSTING (GB) - UPLOADED DATA TESTS")
    
    # Test with multiple uploaded targets
    print_test("GB with Multiple Uploaded Targets")
    request_data = {
        "model": "gb",
        "datasource": "upload",
        "features-target-1": SAMPLE_KOI_FEATURES,
        "features-target-2": ALTERNATIVE_KOI_FEATURES,
        "features-target-3": {
            "koi_period": 15.3741,
            "koi_time0bk": 145.762,
            "koi_impact": 0.089,
            "koi_duration": 2.847,
            "koi_depth": 78.9,
            "koi_incl": 91.23,
            "koi_model_snr": 9.8,
            "koi_count": 1,
            "koi_bin_oedp_sig": 0.234,
            "koi_steff": 5634,
            "koi_slogg": 4.567,
            "koi_srad": 0.789,
            "koi_smass": 0.723,
            "koi_kepmag": 15.123
        },
        "predict": True
    }
    
    success = make_request(ML_ENDPOINT, request_data, "GB Upload Multiple Targets")
    if success:
        print("✅ GB Upload test passed")
    else:
        print("❌ GB Upload test failed")

def test_svm_uploaded_data():
    """Test Support Vector Machine with uploaded data format"""
    print_section("SUPPORT VECTOR MACHINE (SVM) - UPLOADED DATA TESTS")
    
    # Test with multiple uploaded targets
    print_test("SVM with Multiple Uploaded Targets")
    request_data = {
        "model": "svm",
        "datasource": "upload",
        "features-target-1": SAMPLE_KOI_FEATURES,
        "features-target-2": ALTERNATIVE_KOI_FEATURES,
        "features-target-3": {
            "koi_period": 22.8941,
            "koi_time0bk": 158.374,
            "koi_impact": 0.456,
            "koi_duration": 5.123,
            "koi_depth": 412.8,
            "koi_incl": 83.67,
            "koi_model_snr": 23.4,
            "koi_count": 4,
            "koi_bin_oedp_sig": 1.234,
            "koi_steff": 6789,
            "koi_slogg": 4.123,
            "koi_srad": 1.456,
            "koi_smass": 1.567,
            "koi_kepmag": 12.345
        },
        "features-target-4": {
            "koi_period": 7.2156,
            "koi_time0bk": 98.432,
            "koi_impact": 0.678,
            "koi_duration": 1.987,
            "koi_depth": 56.7,
            "koi_incl": 88.91,
            "koi_model_snr": 6.7,
            "koi_count": 2,
            "koi_bin_oedp_sig": 0.345,
            "koi_steff": 4987,
            "koi_slogg": 4.789,
            "koi_srad": 0.612,
            "koi_smass": 0.534,
            "koi_kepmag": 16.789
        },
        "predict": True
    }
    
    success = make_request(ML_ENDPOINT, request_data, "SVM Upload Multiple Targets")
    if success:
        print("✅ SVM Upload test passed")
    else:
        print("❌ SVM Upload test failed")

def test_gb_test_datasource():
    """Test GB with test datasource using Kepler IDs"""
    print_section("GRADIENT BOOSTING (GB) - TEST DATASOURCE")
    
    for i, kepid in enumerate(SAMPLE_KEPLER_IDS[6:8]):  # Test 2 IDs
        print_test(f"GB with Test Datasource - Kepler ID {kepid}")
        request_data = {
            "model": "gb",
            "datasource": "test",
            "kepid": kepid,
            "predict": True
        }
        
        success = make_request(ML_ENDPOINT, request_data, f"GB Test Datasource {i+1}")
        if success:
            print(f"✅ GB Test datasource {i+1} passed")
        else:
            print(f"❌ GB Test datasource {i+1} failed")
        
        time.sleep(1)

def test_svm_test_datasource():
    """Test SVM with test datasource using Kepler IDs"""
    print_section("SUPPORT VECTOR MACHINE (SVM) - TEST DATASOURCE")
    
    for i, kepid in enumerate(SAMPLE_KEPLER_IDS[8:10]):  # Test last 2 IDs
        print_test(f"SVM with Test Datasource - Kepler ID {kepid}")
        request_data = {
            "model": "svm",
            "datasource": "test",
            "kepid": kepid,
            "predict": True
        }
        
        success = make_request(ML_ENDPOINT, request_data, f"SVM Test Datasource {i+1}")
        if success:
            print(f"✅ SVM Test datasource {i+1} passed")
        else:
            print(f"❌ SVM Test datasource {i+1} failed")
        
        time.sleep(1)

def test_error_scenarios():
    """Test various error scenarios"""
    print_section("ERROR SCENARIO TESTS")
    
    # Test invalid model
    print_test("Invalid Model Type")
    request_data = {
        "model": "invalid_model",
        "kepid": "10000490",
        "predict": True
    }
    
    response = requests.post(f"{BASE_URL}{DL_ENDPOINT}", json=request_data)
    if response.status_code != 200:
        print("✅ Invalid model error handled correctly")
    else:
        print("❌ Invalid model should return error")
    
    # Test invalid Kepler ID
    print_test("Invalid Kepler ID")
    request_data = {
        "model": "cnn",
        "kepid": "99999999",
        "predict": True
    }
    
    response = requests.post(f"{BASE_URL}{DL_ENDPOINT}", json=request_data)
    if response.status_code != 200:
        print("✅ Invalid Kepler ID error handled correctly")
    else:
        print("❌ Invalid Kepler ID should return error")
    
    # Test missing required fields
    print_test("Missing Required Fields")
    request_data = {
        "model": "gb",
        "datasource": "manual"
        # Missing features field
    }
    
    response = requests.post(f"{BASE_URL}{ML_ENDPOINT}", json=request_data)
    if response.status_code != 200:
        print("✅ Missing fields error handled correctly")
    else:
        print("❌ Missing fields should return error")

def run_comprehensive_tests():
    """Run all comprehensive tests"""
    print("🚀 Starting Comprehensive API Test Suite")
    print(f"🌐 Base URL: {BASE_URL}")
    print(f"⏰ Test started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    test_functions = [
        test_basic_endpoints,
        test_cnn_with_kepler_ids,
        test_dnn_with_kepler_ids,
        test_gb_manual_entry,
        test_svm_manual_entry,
        test_gb_preloaded_data,
        test_svm_preloaded_data,
        test_gb_uploaded_data,
        test_svm_uploaded_data,
        test_gb_test_datasource,
        test_svm_test_datasource,
        test_error_scenarios
    ]
    
    passed_tests = 0
    total_tests = len(test_functions)
    
    for test_func in test_functions:
        try:
            test_func()
            passed_tests += 1
            print(f"✅ {test_func.__name__} completed")
        except Exception as e:
            print(f"❌ {test_func.__name__} failed with error: {str(e)}")
    
    # Final summary
    print_section("TEST SUMMARY")
    print(f"📊 Tests completed: {passed_tests}/{total_tests}")
    print(f"✅ Success rate: {(passed_tests/total_tests)*100:.1f}%")
    print(f"⏰ Test finished at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    if passed_tests == total_tests:
        print("🎉 All tests completed successfully!")
    else:
        print(f"⚠️  {total_tests - passed_tests} test(s) had issues")

if __name__ == "__main__":
    # Check if server is accessible
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server is accessible")
            run_comprehensive_tests()
        else:
            print(f"❌ Server responded with status {response.status_code}")
            sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to the server. Make sure it's running on localhost:8000")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error checking server: {str(e)}")
        sys.exit(1)