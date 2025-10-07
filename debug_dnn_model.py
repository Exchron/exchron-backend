#!/usr/bin/env python3
"""
Debug script to investigate DNN model output behavior.
This script loads the model directly and tests predictions to understand why we're getting 0/1 outputs.
"""

import tensorflow as tf
import numpy as np
import pandas as pd
import os
from app.services.data_service import get_time_series_data, get_engineered_features
import asyncio

async def debug_dnn_model():
    """Debug the DNN model to understand its output behavior"""
    
    print("🔍 DNN Model Debug Analysis")
    print("=" * 60)
    
    # Load the DNN model
    try:
        model_path = "models/exchron-dnn.keras"
        print(f"Loading model from: {model_path}")
        model = tf.keras.models.load_model(model_path)
        print("✅ Model loaded successfully")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return
    
    # Print model summary
    print("\n📊 Model Architecture:")
    print("-" * 40)
    model.summary()
    
    # Check the output layer
    output_layer = model.layers[-1]
    print(f"\n🎯 Output Layer Details:")
    print(f"   Layer Name: {output_layer.name}")
    print(f"   Layer Type: {type(output_layer)}")
    print(f"   Output Shape: {output_layer.output.shape}")
    print(f"   Activation: {output_layer.activation.__name__ if hasattr(output_layer.activation, '__name__') else output_layer.activation}")
    print(f"   Units: {output_layer.units}")
    
    # Test with a few Kepler IDs
    test_kepids = ["10000490", "10002261", "10004738"]
    
    for kepid in test_kepids:
        print(f"\n🧪 Testing Kepler ID: {kepid}")
        print("-" * 40)
        
        try:
            # Get input data
            time_series_data = await get_time_series_data(kepid)
            engineered_features = await get_engineered_features(kepid)
            
            # Prepare inputs for DNN model
            time_series_input = time_series_data.flatten().reshape(1, -1)  # Shape: (1, 3000)
            features_input = engineered_features  # Shape: (1, 12)
            
            print(f"   Time Series Input Shape: {time_series_input.shape}")
            print(f"   Features Input Shape: {features_input.shape}")
            print(f"   Time Series Range: [{time_series_input.min():.6f}, {time_series_input.max():.6f}]")
            print(f"   Features Range: [{features_input.min():.6f}, {features_input.max():.6f}]")
            
            # Make prediction
            prediction = model.predict([time_series_input, features_input], verbose=0)
            
            print(f"   Raw Prediction Shape: {prediction.shape}")
            print(f"   Raw Prediction Values: {prediction[0]}")
            print(f"   Class 0 Prob: {prediction[0][0]:.6f}")
            print(f"   Class 1 Prob: {prediction[0][1]:.6f}")
            print(f"   Sum: {prediction[0].sum():.6f}")
            
            # Check if this is actually a softmax output
            if abs(prediction[0].sum() - 1.0) < 0.0001:
                print(f"   ✅ Valid softmax output (sums to 1.0)")
            else:
                print(f"   ❌ Invalid softmax output (doesn't sum to 1.0)")
                
        except Exception as e:
            print(f"   ❌ Error processing {kepid}: {e}")
    
    # Test with random data to see if model always outputs extremes
    print(f"\n🎲 Testing with Random Data:")
    print("-" * 40)
    
    for i in range(3):
        # Generate random inputs matching expected shapes
        random_time_series = np.random.normal(0, 1, (1, 3000))
        random_features = np.random.normal(0, 1, (1, 12))
        
        prediction = model.predict([random_time_series, random_features], verbose=0)
        
        print(f"   Random Test {i+1}:")
        print(f"     Raw Prediction: {prediction[0]}")
        print(f"     Class 0 Prob: {prediction[0][0]:.6f}")
        print(f"     Class 1 Prob: {prediction[0][1]:.6f}")
    
    # Check model compilation details
    print(f"\n⚙️ Model Compilation Details:")
    print("-" * 40)
    print(f"   Loss Function: {model.loss}")
    print(f"   Optimizer: {type(model.optimizer).__name__}")
    print(f"   Metrics: {model.metrics_names}")
    
    # Check if model was trained or if it's in an untrained state
    try:
        weights = model.get_weights()
        print(f"   Total parameters: {sum(w.size for w in weights)}")
        print(f"   Output layer weights shape: {weights[-2].shape}")  # Weight matrix
        print(f"   Output layer bias shape: {weights[-1].shape}")     # Bias vector
        print(f"   Output weights mean: {weights[-2].mean():.6f}")
        print(f"   Output bias values: {weights[-1]}")
    except Exception as e:
        print(f"   Could not access weights: {e}")

if __name__ == "__main__":
    asyncio.run(debug_dnn_model())