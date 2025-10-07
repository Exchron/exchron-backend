import os
import numpy as np
import tensorflow as tf
import joblib
from fastapi import HTTPException
from typing import Any

# Paths to model files (updated for new subdirectory structure)
MODEL_DIR = "models"
CNN_MODEL_PATH = os.path.join(MODEL_DIR, "cnn", "exchron-cnn.keras")
DNN_MODEL_PATH = os.path.join(MODEL_DIR, "dnn", "exchron-dnn.keras")
GB_MODEL_PATH = os.path.join(MODEL_DIR, "gb", "exchron-gb.joblib")
SVM_MODEL_PATH = os.path.join(MODEL_DIR, "svm", "exchron-svm.joblib")

# Cache for loaded models to avoid reloading
_model_cache = {}

def get_model(model_type: str) -> Any:
    """Load and cache ML models (CNN/DNN/GB/SVM)"""
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
        elif model_type == "gb":
            if not os.path.exists(GB_MODEL_PATH):
                raise FileNotFoundError(f"GB model file not found at {GB_MODEL_PATH}")
            model = joblib.load(GB_MODEL_PATH)
        elif model_type == "svm":
            if not os.path.exists(SVM_MODEL_PATH):
                raise FileNotFoundError(f"SVM model file not found at {SVM_MODEL_PATH}")
            model = joblib.load(SVM_MODEL_PATH)
        else:
            raise ValueError(f"Unknown model type: {model_type}. Supported models: cnn, dnn, gb, svm")
        
        # Cache the model
        _model_cache[model_type] = model
        return model
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load model {model_type}: {str(e)}")