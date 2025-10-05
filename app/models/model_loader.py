import os
import numpy as np
import tensorflow as tf
from fastapi import HTTPException
from typing import Any

# Paths to model files (adjusted for the actual file structure)
MODEL_DIR = "models"
CNN_MODEL_PATH = os.path.join(MODEL_DIR, "exchron-cnn.keras")
DNN_MODEL_PATH = os.path.join(MODEL_DIR, "exchron-dnn.keras")

# Mock ML model implementations for XGBoost/SVM/KNN (these would be replaced with real models)
class MockMLModel:
    def __init__(self, model_type: str):
        self.model_type = model_type
    
    def predict_proba(self, data: np.ndarray) -> np.ndarray:
        # Mock prediction - returns random probabilities for binary classification
        np.random.seed(42)
        prob_positive = np.random.random()
        return np.array([[1 - prob_positive, prob_positive]])
    
    def predict(self, data: np.ndarray) -> np.ndarray:
        proba = self.predict_proba(data)
        return np.array([1 if proba[0][1] > 0.5 else 0])

# Cache for loaded models to avoid reloading
_model_cache = {}

def get_model(model_type: str) -> Any:
    """Load and cache ML models (real CNN/DNN, mock for others)"""
    model_type = model_type.lower()
    
    # Return cached model if available
    if model_type in _model_cache:
        return _model_cache[model_type]
    
    try:
        if model_type == "cnn":
            if not os.path.exists(CNN_MODEL_PATH):
                raise FileNotFoundError(f"CNN model file not found at {CNN_MODEL_PATH}")
            model = tf.keras.models.load_model(CNN_MODEL_PATH)
        elif model_type == "dnn":
            if not os.path.exists(DNN_MODEL_PATH):
                raise FileNotFoundError(f"DNN model file not found at {DNN_MODEL_PATH}")
            model = tf.keras.models.load_model(DNN_MODEL_PATH)
        elif model_type in ["xgboost", "svm", "knn"]:
            # These remain as mock implementations for now
            model = MockMLModel(model_type)
        else:
            raise ValueError(f"Unknown model type: {model_type}")
        
        # Cache the model
        _model_cache[model_type] = model
        return model
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load model {model_type}: {str(e)}")