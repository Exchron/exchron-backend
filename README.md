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
- **Required model files**: `models/cnn/exchron-cnn.keras` and `models/dnn/exchron-dnn.keras`
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

#### Test Machine Learning Model with Pre-loaded Data (NEW FORMAT):
```cmd
curl -X POST "http://localhost:8000/api/ml/predict" ^
     -H "Content-Type: application/json" ^
     -d "{\"model\": \"gb\", \"datasource\": \"pre-loaded\", \"data\": \"kepler\", \"predict\": true}"
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
    "lightcurve_link": "http://archive.stsci.edu/pub/kepler/lightcurves/0001/000123456/",
    "target_pixel_file_link": "http://archive.stsci.edu/pub/kepler/target_pixel_files/0001/000123456/",
    "dv_report_link": "http://exoplanetarchive.ipac.caltech.edu:8000/data/KeplerData/000/000123/000123456/dv/kplr000123456-20160209194854_dvr.pdf",
    "kepid": "123456",
    "model_used": "CNN"
}
```

### Machine Learning Model Response (Pre-loaded Data - NEW):
```json
{
    "candidate_probability": 0.4270,
    "non_candidate_probability": 0.5730,
    "first": {
        "kepid": "7537660",
        "candidate_probability": 0.0357,
        "non_candidate_probability": 0.9643
    },
    "second": {
        "kepid": "3219037",
        "candidate_probability": 0.9254,
        "non_candidate_probability": 0.0746
    },
    "third": {
        "kepid": "9729691",
        "candidate_probability": 0.9695,
        "non_candidate_probability": 0.0305
    },
    ...
    "tenth": {
        "kepid": "6531143",
        "candidate_probability": 0.3172,
        "non_candidate_probability": 0.6828
    }
}
```

### Machine Learning Model Response (Manual/Test Data):
```json
{
    "candidate_probability": 0.8234,
    "non_candidate_probability": 0.1766
}
```

## 🔧 Configuration

### Data Source Options:
- **manual**: User-provided KOI features
- **test**: Predefined test data with specific Kepler IDs
- **pre-loaded**: Uses first 10 records from KOI-Playground-Test-Data.csv (NEW)

### Data Types for Pre-loaded Source:
- **kepler**: Kepler telescope data
- **tess**: TESS telescope data (uses same KOI dataset)

### Required Features for Manual Input:
- **koi_period**: Orbital period in days
- **koi_time0bk**: Transit epoch in Barycentric Kepler Julian Day
- **koi_impact**: Impact parameter (0-1)
- **koi_duration**: Transit duration in hours
- **koi_depth**: Transit depth in ppm
- **koi_incl**: Inclination in degrees
- **koi_model_snr**: Transit signal-to-noise ratio
- **koi_count**: Number of transits observed
- **koi_bin_oedp_sig**: Odd-even depth comparison significance
- **koi_steff**: Stellar effective temperature in K
- **koi_slogg**: Stellar surface gravity (log g)
- **koi_srad**: Stellar radius in solar radii
- **koi_smass**: Stellar mass in solar masses
- **koi_kepmag**: Kepler magnitude

### Available Test Kepler IDs:
- 123456
- 789012
- 345678
- 901234
- 567890

### Pre-loaded Data Features:
When using `datasource: "pre-loaded"`, the API automatically:
1. Loads the first 10 records from `data/KOI-Playground-Test-Data.csv`
2. Makes predictions for each record using the specified model (GB or SVM)
3. Returns averaged probabilities across all 10 predictions
4. Provides individual predictions for each of the 10 records (first, second, ..., tenth)

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

## 🔗 Archive Links

The API provides links to official astronomical data archives:

### DV Report Links
- **Format**: `http://exoplanetarchive.ipac.caltech.edu:8000/data/KeplerData/XXX/XXXXXX/XXXXXXXXX/dv/kplrXXXXXXXXX-TIMESTAMP_dvr.pdf`
- **Source**: NASA Exoplanet Archive
- **Contains**: Data validation reports with detailed analysis results

### STScI Archive Links
The API includes links to the Space Telescope Science Institute (STScI) Kepler data archive:

#### Lightcurve Files
- **Format**: `http://archive.stsci.edu/pub/kepler/lightcurves/XXXX/KKKKKKKKK/`
- **Contains**: Photometric time series data files
- **Example**: `http://archive.stsci.edu/pub/kepler/lightcurves/0014/001429092/`

#### Target Pixel Files
- **Format**: `http://archive.stsci.edu/pub/kepler/target_pixel_files/XXXX/KKKKKKKKK/`
- **Contains**: Pixel-level data for the target star
- **Example**: `http://archive.stsci.edu/pub/kepler/target_pixel_files/0014/001429092/`

**URL Structure Notes:**
- `XXXX`: First 4 digits of the 9-digit zero-padded Kepler ID
- `KKKKKKKKK`: Full 9-digit zero-padded Kepler ID
- All URLs point to directory listings containing the actual data files

## ⚠️ Important Notes

1. **Real Data Integration**: This version uses authentic Kepler telescope data and provides links to official astronomical archives.

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