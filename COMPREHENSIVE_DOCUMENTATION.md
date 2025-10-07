# Comprehensive Documentation - Exoplanet Classification API

*This document combines all technical documentation, implementation summaries, and usage guides for the Exoplanet Classification API system.*

---

## Table of Contents

1. [System Overview](#system-overview)
2. [API Quick Reference](#api-quick-reference)
3. [Implementation History](#implementation-history)
4. [Model Architecture](#model-architecture)
5. [API Usage Examples](#api-usage-examples)
6. [Troubleshooting Guide](#troubleshooting-guide)
7. [Technical Specifications](#technical-specifications)

---

## System Overview

### Current Status: ✅ Production Ready with Real Models (v2.0.0)

The Exoplanet Classification API is a comprehensive machine learning system that provides:

- **Real CNN Model**: Keras model (`exchron-cnn.keras`) for time series analysis
- **Real DNN Model**: Dual-input Keras model (`exchron-dnn.keras`) with 97.25% accuracy
- **Traditional ML Models**: Gradient Boosting (GB) and Support Vector Machine (SVM)
- **Real Data**: Authentic Kepler Space Telescope lightcurve data (873+ objects)
- **Multiple Data Sources**: Pre-loaded datasets, manual feature input, and file uploads
- **Archive Integration**: Direct links to NASA and STScI data archives

---

## API Quick Reference

### 🎯 Key Endpoints

#### Get Available Data
```bash
GET /api/dl/available-ids  # List all valid Kepler IDs
```

#### Deep Learning Predictions
```bash
POST /api/dl/predict
{
  "model": "cnn" | "dnn",
  "kepid": "10904857",  # Use real Kepler ID
  "predict": true
}
```

#### Machine Learning Predictions
```bash
POST /api/ml/predict
{
  "model": "gb" | "svm",
  "datasource": "pre-loaded" | "manual" | "upload",
  "data": "kepler" | "tess",  # for pre-loaded only
  "predict": true
}
```

### 📊 Sample Valid Kepler IDs

#### Known Candidates
- `10904857` - High confidence candidate
- `6362874` - Validated candidate  
- `6266741` - Strong candidate signal

#### Known False Positives
- `9652632` - Stellar variability
- `6781535` - Binary eclipse
- `3233043` - Instrumental artifact

---

## Implementation History

### ✅ Archive URL Implementation

Successfully implemented comprehensive archive URL generation:

#### DV Report URLs (NASA Exoplanet Archive)
- **Format**: `http://exoplanetarchive.ipac.caltech.edu:8000/data/KeplerData/XXX/XXXXXX/XXXXXXXXX/dv/kplrXXXXXXXXX-TIMESTAMP_dvr.pdf`
- **Source**: CSV data file with exact paths and timestamps
- **Example**: `http://exoplanetarchive.ipac.caltech.edu:8000/data/KeplerData/003/003247/003247268/dv/kplr003247268-20160209194854_dvr.pdf`

#### STScI Archive URLs
- **Lightcurve**: `http://archive.stsci.edu/pub/kepler/lightcurves/XXXX/KKKKKKKKK/`
- **Target Pixel**: `http://archive.stsci.edu/pub/kepler/target_pixel_files/XXXX/KKKKKKKKK/`
- **Structure**: First 4 digits / Full 9-digit zero-padded ID

### ✅ Pre-loaded Data Format Implementation

Successfully implemented new API format accepting:

```json
{
  "model": "gb" | "svm",
  "datasource": "pre-loaded",
  "data": "kepler" | "tess", 
  "predict": true
}
```

**Response Format**: Returns averaged predictions across first 10 records with individual breakdowns:

```json
{
  "candidate_probability": 0.4270,
  "non_candidate_probability": 0.5730,
  "first": {
    "kepid": "7537660",
    "candidate_probability": 0.0357,
    "non_candidate_probability": 0.9643
  },
  // ... continues through "tenth"
}
```

### ✅ DNN Model Softmax Update

**Key Changes Made:**
- **Output Layer**: Changed from `Dense(1, sigmoid)` to `Dense(2, softmax)`
- **Loss Function**: Updated from `binary_crossentropy` to `sparse_categorical_crossentropy`
- **Performance**: Improved accuracy from 96.15% to 97.25%

**Technical Implementation:**
```python
# Model-specific handling for different output formats
if model_type.lower() == "cnn":
    # CNN uses sigmoid output - single probability for positive class
    candidate_prob = float(prediction[0][0])
    non_candidate_prob = 1.0 - candidate_prob
elif model_type.lower() == "dnn":
    # DNN uses softmax output - probability distribution over two classes
    non_candidate_prob = float(prediction[0][0])  # Class 0: Non-candidate
    candidate_prob = float(prediction[0][1])      # Class 1: Candidate
```

---

## Model Architecture

### DNN Model (Dual-Input Deep Neural Network)

#### Overview
- **Model Type**: Dual-Input DNN with Softmax Output
- **Architecture**: Combined CNN and Dense layers for time series and tabular data
- **Total Parameters**: 3,151,938
- **Final Test Accuracy**: 0.9725
- **AUC Score**: 0.9965

#### Input Specifications

##### 1. Time Series Input (Light Curves)
- **Shape**: `(3000, 1)`
- **Description**: Normalized light curve data representing flux measurements
- **Preprocessing**: Sequence padding/truncation, normalization, missing value handling

##### 2. Stellar and Planetary Features Input
- **Shape**: `(12,)`
- **Features**: 12 KOI parameters including:
  - `koi_period`: Orbital period (days)
  - `koi_duration`: Transit duration (hours)
  - `koi_depth`: Transit depth (ppm)
  - `koi_model_snr`: Signal-to-noise ratio
  - `koi_impact`: Impact parameter
  - `koi_steff`: Stellar effective temperature (K)
  - `koi_slogg`: Stellar surface gravity (log g)
  - `koi_srad`: Stellar radius (solar radii)
  - `koi_smass`: Stellar mass (solar masses)
  - `koi_kepmag`: Kepler magnitude

#### Network Architecture Details

**Key Layers:**
- **Conv1D Layers**: Multiple 1D convolution layers with ReLU activation
- **BatchNormalization**: Stabilizes training across layers
- **MaxPooling1D**: Reduces dimensionality while preserving important features
- **Dropout**: Regularization to prevent overfitting (rates: 0.25-0.5)
- **Dense Layers**: Fully connected layers for feature processing
- **Concatenate**: Combines time series and tabular features
- **Output Layer**: Dense(2, softmax) for binary classification probabilities

**Training Configuration:**
- **Batch Size**: 32
- **Learning Rate**: 0.001
- **Optimizer**: Adam
- **Loss Function**: sparse_categorical_crossentropy
- **Early Stopping**: patience=15, monitor='val_loss'

### CNN Model Architecture

#### Input Specifications
- **Shape**: `(3000, 1)`
- **Data Type**: `float32`
- **Processing Pipeline**:
  1. Load CSV file
  2. Extract flux column (`pdcsap_flux` or `flux`)
  3. Remove NaN values and outliers (3-sigma clipping)
  4. Normalize (zero mean, unit variance)
  5. Pad or truncate to 3000 points
  6. Reshape to `(1, 3000, 1)` for prediction

#### Required Data Formats

**Lightkurve CSV Files:**
- **Location**: `lightkurve_data/kepler_{kepler_id}_lightkurve.csv`
- **Primary Column**: `pdcsap_flux` or `flux`
- **Additional Columns**: `flux_err`, `quality`, `timecorr`, etc.

**Example CSV Structure:**
```csv
flux,flux_err,quality,pdcsap_flux,pdcsap_flux_err,kepler_id
425586.3,96.70743,0,425586.3,96.70743,10000490
...
```

---

## API Usage Examples

### Working JSON Examples for Swagger UI

#### Manual Features Request
```json
{
  "model": "gb",
  "datasource": "manual",
  "features": {
    "koi_period": 10.005,
    "koi_time0bk": 136.83,
    "koi_impact": 0.148,
    "koi_duration": 3.481,
    "koi_depth": 143.3,
    "koi_incl": 89.61,
    "koi_model_snr": 11.4,
    "koi_count": 2,
    "koi_bin_oedp_sig": 0.461,
    "koi_steff": 5912.0,
    "koi_slogg": 4.453,
    "koi_srad": 0.924,
    "koi_smass": 0.884,
    "koi_kepmag": 14.634
  },
  "predict": true
}
```

#### Pre-loaded Format
```json
{
  "model": "gb",
  "datasource": "pre-loaded",
  "data": "kepler",
  "predict": true
}
```

#### Deep Learning Prediction
```json
{
  "model": "cnn",
  "kepid": "10904857",
  "predict": true
}
```

### CURL Command Examples

#### Test GB Model with Pre-loaded Data
```bash
curl -X POST "http://localhost:8000/api/ml/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "model": "gb",
       "datasource": "pre-loaded",
       "data": "kepler",
       "predict": true
     }'
```

#### Test CNN Model
```bash
curl -X POST "http://localhost:8000/api/dl/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "model": "cnn",
       "kepid": "10904857",
       "predict": true
     }'
```

#### Windows PowerShell Example
```powershell
$body = @{
    model = "gb"
    datasource = "pre-loaded" 
    data = "kepler"
    predict = $true
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/ml/predict" -Method POST -Body $body -ContentType "application/json"
```

### Expected Response Formats

#### ML Model Response (Pre-loaded)
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
  // ... continues through "tenth"
}
```

#### DL Model Response (with Archive Links)
```json
{
  "candidate_probability": 0.7234,
  "non_candidate_probability": 0.2766,
  "lightcurve_link": "http://archive.stsci.edu/pub/kepler/lightcurves/0032/003247268/",
  "target_pixel_file_link": "http://archive.stsci.edu/pub/kepler/target_pixel_files/0032/003247268/",
  "dv_report_link": "http://exoplanetarchive.ipac.caltech.edu:8000/data/KeplerData/003/003247/003247268/dv/kplr003247268-20160209194854_dvr.pdf",
  "kepid": "3247268",
  "model_used": "CNN"
}
```

---

## Troubleshooting Guide

### 🔧 Swagger UI Issues

#### ✅ **Common Problems and Solutions**

**Problem**: 422 "JSON decode error" in Swagger UI

**Solutions:**

1. **Boolean Values**
   - ❌ Wrong: `"predict": True` (Python format)
   - ✅ Correct: `"predict": true` (JSON format)

2. **Number Precision**
   - ❌ Problematic: Very long decimal numbers
   - ✅ Better: Round to reasonable precision

3. **Trailing Commas**
   - ❌ Wrong: `"predict": true,}` (trailing comma)
   - ✅ Correct: `"predict": true}` (no trailing comma)

4. **Copy-Paste Issues**
   - Make sure to copy entire JSON blocks
   - Check for hidden characters
   - Try typing manually if copy-paste fails

#### Testing Steps
1. Go to `http://localhost:8000/docs`
2. Find `POST /api/ml/predict` or `POST /api/dl/predict` endpoint
3. Click "Try it out" button
4. Clear existing JSON in request body
5. Copy-paste exact examples from above
6. Click "Execute"
7. Expect 200 response with prediction results

### Alternative Testing Methods

If Swagger UI doesn't work:

1. **Use curl commands** (see examples above)
2. **Use Python test scripts**: `test_comprehensive.py`
3. **Check server logs** for error messages
4. **Refresh Swagger UI** page (Ctrl+F5)

---

## Technical Specifications

### 🔧 File Structure

#### Modified Files
1. `app/schemas/requests.py` - API request schemas
2. `app/schemas/responses.py` - API response schemas
3. `app/services/data_service.py` - Data loading and processing
4. `app/services/prediction_service.py` - Core prediction logic
5. `app/services/url_service.py` - Archive URL generation
6. `app/routers/ml_models.py` - ML model endpoints
7. `app/routers/dl_models.py` - Deep learning model endpoints
8. `app/main.py` - Main application setup

#### Model Files
- `models/cnn/exchron-cnn.keras` - Real CNN model
- `models/dnn/exchron-dnn.keras` - Real DNN model
- `models/gb/` - Gradient Boosting model files
- `models/svm/` - Support Vector Machine model files

#### Data Files
- `data/lightkurve_data/` - Kepler lightcurve CSV files (873+ objects)
- `data/lightkurve_test_metadata.csv` - Ground truth labels
- `data/KOI-Playground-Test-Data.csv` - KOI feature dataset
- `data/slected-2000-dnn-cnn.csv` - DV report paths and metadata

### 🛡️ Validation & Error Handling

#### Input Validation
- ✅ Model type validation (gb/svm for ML, cnn/dnn for DL)
- ✅ Kepler ID existence validation
- ✅ Required field validation for each datasource
- ✅ Proper error messages for missing fields
- ✅ Graceful handling of NaN values in data

#### Response Validation
- ✅ Probabilities always sum to 1.0
- ✅ Consistent response formats across models
- ✅ Archive URLs properly formatted
- ✅ Individual prediction breakdowns for pre-loaded format

### 📈 Performance Metrics

#### DNN Model Performance
- **Accuracy**: 97.25%
- **Precision**: 96.43%
- **Recall**: 97.59%
- **AUC Score**: 99.65%
- **Processing Time**: <2 seconds per prediction

#### CNN Model Performance
- **Dataset Size**: 873+ Kepler lightcurves
- **Time Series Length**: 3000 points (fixed)
- **Processing Time**: <2 seconds per prediction
- **Memory Usage**: ~12KB per input

#### System Performance
- **API Response Time**: <3 seconds typical
- **Concurrent Requests**: Supported via FastAPI
- **Memory Footprint**: ~200MB total (models loaded)
- **Storage Requirements**: ~50MB for models, variable for data

### 🔄 Backward Compatibility

The API maintains full backward compatibility:
- ✅ Existing `manual` datasource still works
- ✅ Existing `test` datasource still works
- ✅ All existing API endpoints remain functional
- ✅ Response formats for old requests unchanged
- ✅ Original model behaviors preserved

---

## Quick Testing Commands

### Start the API
```bash
uvicorn app.main:app --reload
```

### Test Different Models
```bash
# Test CNN
python test_comprehensive.py

# Test DNN  
python test_ml_models.py

# Test Pre-loaded format
python test_different_features.py

# Test complete functionality
python test_full.py
```

### Access Documentation
- **Interactive API Docs**: `http://localhost:8000/docs`
- **Alternative Docs**: `http://localhost:8000/redoc`
- **Available IDs**: `http://localhost:8000/api/dl/available-ids`

---

## System Status Summary

### ✅ **Fully Implemented Features**

1. **Real Model Integration**
   - CNN model for time series analysis
   - DNN model with dual inputs and 97.25% accuracy
   - Traditional ML models (GB, SVM)

2. **Data Integration**
   - 873+ authentic Kepler lightcurves
   - Automated feature extraction
   - Ground truth validation data

3. **API Functionality**
   - Multiple datasource options
   - Pre-loaded data with averaged predictions
   - Manual feature input
   - File upload capabilities

4. **Archive Integration**
   - NASA Exoplanet Archive DV report links
   - STScI lightcurve data links
   - STScI target pixel file links

5. **Enhanced Documentation**
   - Comprehensive API documentation
   - Working examples for all endpoints
   - Troubleshooting guides
   - Model architecture specifications

**Status**: ✅ **Production Ready**  
**Version**: 2.0.0  
**Last Updated**: October 7, 2025

---

*This comprehensive documentation provides all necessary information for using, maintaining, and extending the Exoplanet Classification API system.*