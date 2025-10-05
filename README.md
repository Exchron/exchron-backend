# Exoplanet Classification API v2.0

A sophisticated FastAPI backend for exoplanet classification using **real trained models** on **authentic Kepler Space Telescope data**:

## 🎯 **Models Overview**

### **Deep Learning Models (REAL)**
- **CNN**: Convolutional Neural Network trained on light curve time series
  - Input: 3000-point normalized flux data
  - Architecture: Conv1D layers for temporal pattern detection
  - File: `exchron-cnn.keras`
  
- **DNN**: Dual-input Deep Neural Network combining time series + engineered features
  - Input: Time series (3000 points) + 12 statistical features
  - Architecture: CNN branch + Dense branch with fusion layers
  - File: `exchron-dnn.keras`
  - Test Accuracy: 95.6%, AUC: 99.59%

### **Traditional ML Models (Mock)**
- **XGBoost**: Gradient boosting (mock implementation)
- **SVM**: Support Vector Machine (mock implementation) 
- **KNN**: K-Nearest Neighbors (mock implementation)

## 🚀 Quick Start Guide

### Prerequisites

- Python 3.9 or higher
- pip package manager
- **Required model files**: `models/exchron-cnn.keras` and `models/exchron-dnn.keras`
- **Required data**: `data/lightkurve_data/` directory with Kepler lightcurve CSV files

### Installation

1. **Navigate to the project directory:**
   ```cmd
   cd C:\Users\navid\Desktop\Figma\exchron-backend
   ```

2. **Create a virtual environment (recommended):**
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```

4. **Verify model files exist:**
   ```cmd
   dir models\*.keras
   dir data\lightkurve_data\*.csv
   ```

5. **Start the API server:**
   ```cmd
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Access the API:**
   - API Documentation: http://localhost:8000/docs
   - API Status: http://localhost:8000/health
   - Available Kepler IDs: http://localhost:8000/api/dl/available-ids

## 📚 API Documentation

### Available Endpoints

#### Root Endpoints
- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /models` - List all available models

#### Deep Learning Models
- `POST /api/dl/predict` - Make predictions using CNN/DNN models
- `GET /api/dl/models` - List available DL models

#### Machine Learning Models
- `POST /api/ml/predict` - Make predictions using XGBoost/SVM/KNN models
- `GET /api/ml/models` - List available ML models
- `GET /api/ml/features` - Get required features for manual input

## 🧪 Testing the API

### 1. Using the Interactive Documentation

Visit http://localhost:8000/docs and use the interactive Swagger UI to test endpoints.

### 2. Using curl commands

#### Test Deep Learning Model (CNN):
```cmd
curl -X POST "http://localhost:8000/api/dl/predict" ^
     -H "Content-Type: application/json" ^
     -d "{\"model\": \"cnn\", \"kepid\": \"123456\", \"predict\": true}"
```

#### Test Machine Learning Model with Test Data:
```cmd
curl -X POST "http://localhost:8000/api/ml/predict" ^
     -H "Content-Type: application/json" ^
     -d "{\"model\": \"xgboost\", \"datasource\": \"test\", \"kepid\": \"123456\", \"predict\": true}"
```

#### Test Machine Learning Model with Manual Features:
```cmd
curl -X POST "http://localhost:8000/api/ml/predict" ^
     -H "Content-Type: application/json" ^
     -d "{\"model\": \"svm\", \"datasource\": \"manual\", \"features\": {\"period\": 3.5, \"impact\": 0.15, \"duration\": 3.0, \"depth\": 100.0, \"temp\": 5500.0, \"logg\": 4.5, \"metallicity\": 0.0}, \"predict\": true}"
```

### 3. Using Python requests

```python
import requests
import json

# Test DL model
dl_response = requests.post(
    "http://localhost:8000/api/dl/predict",
    json={
        "model": "dnn",
        "kepid": "789012",
        "predict": True
    }
)
print("DL Prediction:", dl_response.json())

# Test ML model with test data
ml_response = requests.post(
    "http://localhost:8000/api/ml/predict",
    json={
        "model": "knn",
        "datasource": "test",
        "kepid": "123456",
        "predict": True
    }
)
print("ML Prediction:", ml_response.json())

# Test ML model with manual features
manual_response = requests.post(
    "http://localhost:8000/api/ml/predict",
    json={
        "model": "xgboost",
        "datasource": "manual",
        "features": {
            "period": 5.2,
            "impact": 0.3,
            "duration": 4.1,
            "depth": 150.0,
            "temp": 5200.0,
            "logg": 4.2,
            "metallicity": 0.1
        },
        "predict": True
    }
)
print("Manual Prediction:", manual_response.json())
```

## 📊 Sample Responses

### Deep Learning Model Response:
```json
{
    "candidate_probability": 0.7234,
    "non_candidate_probability": 0.2766,
    "lightcurve_link": "https://exoplanetarchive.ipac.caltech.edu/cgi-bin/keplerLightCurveViewer/nph-keplerLCViewer?kepid=123456",
    "dv_report_link": "https://exoplanetarchive.ipac.caltech.edu/data/KeplerData/dv_reports/kepler123456/kplr123456-dv_report.pdf",
    "kepid": "123456",
    "model_used": "CNN"
}
```

### Machine Learning Model Response:
```json
{
    "prediction": 0.8234,
    "prediction_class": "candidate",
    "features_used": {
        "period": 3.525,
        "impact": 0.146,
        "duration": 2.957,
        "depth": 103.4,
        "temp": 5455.0,
        "logg": 4.467,
        "metallicity": 0.04
    },
    "model_used": "XGBOOST",
    "kepid": "123456"
}
```

## 🔧 Configuration

### Required Features for Manual Input:
- **period**: Orbital period in days
- **impact**: Impact parameter (0-1)
- **duration**: Transit duration in hours
- **depth**: Transit depth in ppm
- **temp**: Stellar effective temperature in K
- **logg**: Stellar surface gravity
- **metallicity**: Stellar metallicity [Fe/H]

### Available Test Kepler IDs:
- 123456
- 789012
- 345678
- 901234
- 567890

## 🐳 Docker Deployment

1. **Build the Docker image:**
   ```cmd
   docker build -t exoplanet-api .
   ```

2. **Run the container:**
   ```cmd
   docker run -p 8000:8000 exoplanet-api
   ```

## 🧠 Model Information

### Deep Learning Models (CNN/DNN)
- **Input**: Time series data (light curves)
- **Output**: Binary classification probability (candidate/non-candidate)
- **Use case**: Analyzing temporal patterns in stellar brightness data

### Traditional ML Models (XGBoost/SVM/KNN)
- **Input**: Extracted features from transit data
- **Output**: Binary classification probability
- **Use case**: Feature-based classification using stellar and planetary parameters

## ⚠️ Important Notes

1. **Mock Implementation**: This is a simplified version using mock models for demonstration. In production, you would replace the mock models with actual trained models.

2. **Data Sources**: 
   - `test`: Uses predefined test data with known Kepler IDs
   - `manual`: Accepts user-provided feature values

3. **CORS**: The API is configured to allow requests from `http://localhost:3000` for frontend integration.

4. **Error Handling**: The API includes comprehensive error handling and validation.

## 🛠️ Development

### Project Structure:
```
exoplanet-classification-api/
├── app/
│   ├── main.py              # FastAPI application
│   ├── models/
│   │   └── model_loader.py  # Model loading utilities
│   ├── routers/
│   │   ├── dl_models.py     # Deep learning endpoints
│   │   └── ml_models.py     # ML endpoints
│   ├── schemas/
│   │   ├── requests.py      # Request models
│   │   └── responses.py     # Response models
│   └── services/
│       ├── data_service.py      # Data handling
│       └── prediction_service.py # Prediction logic
├── data/
│   └── test_data.csv        # Sample test data
├── requirements.txt         # Dependencies
└── Dockerfile              # Container configuration
```

### Adding Real Models:

To replace mock models with real ones:

1. Place your model files in the `models/` directory
2. Update `model_loader.py` to load actual models
3. Adjust preprocessing in `prediction_service.py`
4. Update feature requirements in `data_service.py`

## 📝 License

This project is for educational and demonstration purposes.