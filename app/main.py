from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import dl_models, ml_models
import os

app = FastAPI(
    title="Exoplanet Classification API",
    description="API for exoplanet classification using various ML models with real Kepler data",
    version="2.0.0"
)

# Configure CORS to allow requests from your Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "*"],  # Update with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(dl_models.router, prefix="/api/dl", tags=["Deep Learning Models"])
app.include_router(ml_models.router, prefix="/api/ml", tags=["Machine Learning Models"])

@app.get("/", tags=["Root"])
async def read_root():
    return {
        "message": "Welcome to Exoplanet Classification API",
        "version": "2.0.0",
        "description": "Real CNN/DNN models trained on Kepler telescope data",
        "models": {
            "cnn": "Convolutional Neural Network for light curve analysis",
            "dnn": "Dual-input Deep Neural Network (time series + features)",
            "ml_models": "XGBoost, SVM, KNN (mock implementations)"
        },
        "endpoints": {
            "dl_predict": "/api/dl/predict",
            "ml_predict": "/api/ml/predict", 
            "available_ids": "/api/dl/available-ids",
            "docs": "/docs"
        }
    }

@app.get("/health", tags=["Health"])
async def health_check():
    # Check if model files exist
    cnn_exists = os.path.exists("models/exchron-cnn.keras")
    dnn_exists = os.path.exists("models/exchron-dnn.keras")
    data_exists = os.path.exists("data/lightkurve_data")
    
    return {
        "status": "healthy",
        "models": {
            "cnn_loaded": cnn_exists,
            "dnn_loaded": dnn_exists,
            "data_available": data_exists
        }
    }

@app.get("/models", tags=["Models"])
async def list_models():
    return {
        "deep_learning_models": [
            {
                "name": "cnn",
                "type": "Convolutional Neural Network",
                "input": "Time series (3000 points)",
                "file": "exchron-cnn.keras"
            },
            {
                "name": "dnn", 
                "type": "Dual-input Deep Neural Network",
                "input": "Time series + 12 engineered features",
                "file": "exchron-dnn.keras"
            }
        ],
        "machine_learning_models": [
            {
                "name": "xgboost",
                "type": "Gradient Boosting",
                "status": "mock implementation"
            },
            {
                "name": "svm",
                "type": "Support Vector Machine", 
                "status": "mock implementation"
            },
            {
                "name": "knn",
                "type": "K-Nearest Neighbors",
                "status": "mock implementation"
            }
        ]
    }