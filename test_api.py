"""
Test script for Exoplanet Classification API (v2.0 - Real Models)
Run this script after starting the API server to test all endpoints with real Kepler data
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

# Real Kepler IDs from the test metadata
TEST_KEPLER_IDS = [
    "10904857",  # CANDIDATE
    "9652632",   # FALSE POSITIVE  
    "6781535",   # FALSE POSITIVE
    "6362874",   # CANDIDATE
    "6266741",   # CANDIDATE
]

def test_endpoint(method, endpoint, data=None, description=""):
    """Test an API endpoint and print results"""
    print(f"\n{'='*50}")
    print(f"Testing: {description}")
    print(f"Endpoint: {method} {endpoint}")
    
    try:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{endpoint}")
        elif method == "POST":
            response = requests.post(f"{BASE_URL}{endpoint}", json=data)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("Response:")
            if isinstance(result, dict) and len(str(result)) > 1000:
                # Truncate long responses
                print(json.dumps({k: v for k, v in list(result.items())[:5]}, indent=2))
                print("... (truncated)")
            else:
                print(json.dumps(result, indent=2))
        else:
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API. Make sure the server is running!")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def main():
    print("🚀 Exoplanet Classification API Test Suite v2.0")
    print("Testing with REAL CNN/DNN models and Kepler telescope data")
    print("Make sure the API server is running on http://localhost:8000")
    print("Start server with: uvicorn app.main:app --reload")
    
    # Wait for user confirmation
    input("\nPress Enter to start testing...")
    
    # Test basic endpoints
    test_endpoint("GET", "/", description="Root endpoint (API info)")
    test_endpoint("GET", "/health", description="Health check (model status)")
    test_endpoint("GET", "/models", description="List all models")
    
    # Test deep learning endpoints
    test_endpoint("GET", "/api/dl/models", description="List DL models with details")
    test_endpoint("GET", "/api/dl/available-ids", description="Get available Kepler IDs")
    
    # Test CNN predictions with real Kepler IDs
    print(f"\n{'='*60}")
    print("TESTING CNN MODEL WITH REAL KEPLER DATA")
    print(f"{'='*60}")
    
    for kepid in TEST_KEPLER_IDS[:3]:  # Test first 3 IDs
        test_endpoint("POST", "/api/dl/predict", 
                     data={
                         "model": "cnn",
                         "kepid": kepid,
                         "predict": True
                     },
                     description=f"CNN prediction for Kepler ID {kepid}")
    
    # Test DNN predictions
    print(f"\n{'='*60}")
    print("TESTING DUAL-INPUT DNN MODEL")
    print(f"{'='*60}")
    
    for kepid in TEST_KEPLER_IDS[:2]:  # Test first 2 IDs
        test_endpoint("POST", "/api/dl/predict", 
                     data={
                         "model": "dnn",
                         "kepid": kepid,
                         "predict": True
                     },
                     description=f"DNN prediction for Kepler ID {kepid}")
    
    # Test machine learning endpoints (still using mock data)
    print(f"\n{'='*60}")
    print("TESTING TRADITIONAL ML MODELS (Mock Data)")
    print(f"{'='*60}")
    
    test_endpoint("GET", "/api/ml/models", description="List ML models")
    test_endpoint("GET", "/api/ml/features", description="Get required features")
    
    test_endpoint("POST", "/api/ml/predict", 
                 data={
                     "model": "xgboost",
                     "datasource": "test",
                     "kepid": "123456",
                     "predict": True
                 },
                 description="XGBoost with mock test data")
    
    test_endpoint("POST", "/api/ml/predict", 
                 data={
                     "model": "svm",
                     "datasource": "manual",
                     "features": {
                         "period": 3.5,
                         "impact": 0.15,
                         "duration": 3.0,
                         "depth": 100.0,
                         "temp": 5500.0,
                         "logg": 4.5,
                         "metallicity": 0.0
                     },
                     "predict": True
                 },
                 description="SVM with manual features")
    
    # Test error cases
    print(f"\n{'='*60}")
    print("TESTING ERROR HANDLING")
    print(f"{'='*60}")
    
    test_endpoint("POST", "/api/dl/predict", 
                 data={
                     "model": "cnn",
                     "kepid": "999999999",  # Non-existent ID
                     "predict": True
                 },
                 description="CNN with invalid Kepler ID (should fail)")
    
    test_endpoint("POST", "/api/dl/predict", 
                 data={
                     "model": "invalid_model",
                     "kepid": TEST_KEPLER_IDS[0],
                     "predict": True
                 },
                 description="Invalid DL model (should fail)")
    
    print(f"\n{'='*60}")
    print("✅ Test suite completed!")
    print("")
    print("📊 Summary:")
    print("- CNN: Uses real Keras model for time series classification")
    print("- DNN: Uses real dual-input Keras model (time series + features)")
    print("- ML Models: Mock implementations (XGBoost/SVM/KNN)")
    print("- Real Kepler telescope lightcurve data from NASA archive")
    print("")
    print("🔗 Key endpoints:")
    print("- GET  /api/dl/available-ids  - List valid Kepler IDs")
    print("- POST /api/dl/predict        - CNN/DNN predictions")
    print("- POST /api/ml/predict        - Traditional ML predictions")
    print("- GET  /docs                  - Interactive API documentation")

def test_specific_kepid():
    """Test a specific Kepler ID with both models"""
    kepid = "10904857"  # Known candidate
    print(f"\n🔍 Detailed test for Kepler ID {kepid}")
    print("="*50)
    
    # Test CNN
    print("\n📡 CNN Analysis:")
    test_endpoint("POST", "/api/dl/predict", 
                 data={"model": "cnn", "kepid": kepid, "predict": True},
                 description="CNN time series analysis")
    
    # Test DNN
    print("\n🧠 DNN Analysis:")
    test_endpoint("POST", "/api/dl/predict", 
                 data={"model": "dnn", "kepid": kepid, "predict": True},
                 description="DNN dual-input analysis")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--kepid":
        test_specific_kepid()
    else:
        main()