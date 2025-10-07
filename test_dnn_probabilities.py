#!/usr/bin/env python3
"""
Test script to verify DNN model now outputs probabilities correctly.
This script tests both CNN and DNN models to ensure the updated code handles both outputs properly.
"""

import requests
import json
import sys

def test_model_prediction(model_type, kepid):
    """Test a model prediction and display the results"""
    
    url = "http://localhost:8000/api/dl/predict"
    payload = {
        "model": model_type,
        "kepid": kepid,
        "predict": True
    }
    
    print(f"\n{'='*60}")
    print(f"Testing {model_type.upper()} model with Kepler ID: {kepid}")
    print(f"{'='*60}")
    
    try:
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"✅ Prediction successful!")
            print(f"Model Used: {result.get('model_used', 'Unknown')}")
            print(f"Kepler ID: {result.get('kepid', 'Unknown')}")
            print(f"")
            print(f"📊 PROBABILITY RESULTS:")
            print(f"   Candidate Probability:     {result.get('candidate_probability', 0):.6f}")
            print(f"   Non-candidate Probability: {result.get('non_candidate_probability', 0):.6f}")
            
            # Verify probabilities sum to 1.0
            total_prob = result.get('candidate_probability', 0) + result.get('non_candidate_probability', 0)
            print(f"   Total Probability:         {total_prob:.6f}")
            
            if abs(total_prob - 1.0) < 0.0001:
                print(f"   ✅ Probabilities sum correctly to 1.0")
            else:
                print(f"   ❌ WARNING: Probabilities do not sum to 1.0")
            
            # Determine classification
            candidate_prob = result.get('candidate_probability', 0)
            classification = "CANDIDATE" if candidate_prob >= 0.5 else "NON-CANDIDATE"
            confidence = max(candidate_prob, 1 - candidate_prob)
            
            print(f"")
            print(f"🎯 CLASSIFICATION:")
            print(f"   Predicted Class: {classification}")
            print(f"   Confidence:      {confidence:.1%}")
            
            return True
            
        else:
            print(f"❌ Request failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error making request: {str(e)}")
        return False

def test_model_descriptions():
    """Test the model descriptions endpoint to see updated info"""
    
    print(f"\n{'='*60}")
    print("Testing Model Descriptions Endpoint")
    print(f"{'='*60}")
    
    try:
        response = requests.get("http://localhost:8000/api/dl/models")
        
        if response.status_code == 200:
            result = response.json()
            
            print("Available Models:")
            for model in result.get('models', []):
                print(f"\n🤖 {model['name'].upper()} Model:")
                print(f"   Description: {model['description']}")
                print(f"   Input Shape: {model['input_shape']}")
                print(f"   Input Description: {model['input_description']}")
                
                if 'output_description' in model:
                    print(f"   Output Description: {model['output_description']}")
                if 'architecture' in model:
                    print(f"   Architecture: {model['architecture']}")
            
            return True
        else:
            print(f"❌ Request failed with status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error making request: {str(e)}")
        return False

def main():
    """Main test function"""
    
    print("🧪 Testing Updated DNN Model with Probability Output")
    print("This test verifies that the DNN model now outputs proper probabilities")
    
    # Test model descriptions first
    if not test_model_descriptions():
        print("❌ Failed to get model descriptions. Is the API running?")
        return
    
    # Test sample Kepler IDs with both models
    test_kepler_ids = ["10000490", "10002261", "10004738"]
    
    success_count = 0
    total_tests = 0
    
    for kepid in test_kepler_ids:
        
        # Test DNN model (updated with softmax)
        total_tests += 1
        if test_model_prediction("dnn", kepid):
            success_count += 1
        
        # Test CNN model (still uses sigmoid) for comparison
        total_tests += 1
        if test_model_prediction("cnn", kepid):
            success_count += 1
    
    # Print summary
    print(f"\n{'='*60}")
    print("🏁 TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Tests Passed: {success_count}/{total_tests}")
    print(f"Success Rate: {success_count/total_tests:.1%}")
    
    if success_count == total_tests:
        print("🎉 All tests passed! The DNN model is now outputting probabilities correctly.")
    else:
        print("⚠️  Some tests failed. Check the API server and model files.")

if __name__ == "__main__":
    main()