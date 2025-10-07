# Exoplanet Classification API - Request Examples

This document provides example API requests for all supported endpoints in the Exoplanet Classification API. Use these examples as templates for your own API calls.

## Table of Contents
- [Deep Learning Models](#deep-learning-models)
  - [CNN Model Prediction](#cnn-model-prediction)
  - [DNN Model Prediction](#dnn-model-prediction)
- [Machine Learning Models](#machine-learning-models)
  - [Manual Feature Entry](#manual-feature-entry)
  - [Pre-loaded Data](#pre-loaded-data)
  - [Upload Multiple Targets](#upload-multiple-targets)
  - [Test Data Source](#test-data-source)
- [Informational Endpoints](#informational-endpoints)

## Deep Learning Models

### CNN Model Prediction

The CNN model analyzes time series light curve data from a specified Kepler ID.

**Endpoint**: `POST /api/dl/predict`

```json
{
  "model": "cnn",
  "kepid": "10000490",
  "predict": true
}
```

**Response**:

```json
{
  "candidate_probability": 0.8764,
  "non_candidate_probability": 0.1236,
  "lightcurve_link": "https://archive.stsci.edu/missions/kepler/lightcurves/0100/010004908/kplr010004908-2009166043257_llc.fits",
  "target_pixel_file_link": "https://archive.stsci.edu/missions/kepler/target_pixel_files/0100/010004908/kplr010004908-2009166043257_lpd-targ.fits",
  "dv_report_link": "https://exoplanetarchive.ipac.caltech.edu/data/KeplerData/008/008358/008358421/dv/kplr008358421_20121029225749_dvr.pdf",
  "kepid": "10000490",
  "model_used": "CNN"
}
```

### DNN Model Prediction

The DNN model uses both time series data and engineered features for a dual-input prediction.

**Endpoint**: `POST /api/dl/predict`

```json
{
  "model": "dnn",
  "kepid": "10002261",
  "predict": true
}
```

**Response**:

```json
{
  "candidate_probability": 0.9135,
  "non_candidate_probability": 0.0865,
  "lightcurve_link": "https://archive.stsci.edu/missions/kepler/lightcurves/0100/010002261/kplr010002261-2009166043257_llc.fits",
  "target_pixel_file_link": "https://archive.stsci.edu/missions/kepler/target_pixel_files/0100/010002261/kplr010002261-2009166043257_lpd-targ.fits",
  "dv_report_link": "https://exoplanetarchive.ipac.caltech.edu/data/KeplerData/008/008358/008358421/dv/kplr008358421_20121029225749_dvr.pdf",
  "kepid": "10002261",
  "model_used": "DNN"
}
```

## Machine Learning Models

### Manual Feature Entry

Provide specific KOI features for a manual prediction with a choice of models.

#### Gradient Boosting (GB) Model

**Endpoint**: `POST /api/ml/predict`

```json
{
  "model": "gb",
  "datasource": "manual",
  "features": {
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
  },
  "predict": true
}
```

**Response**:

```json
{
  "candidate_probability": 0.9254,
  "non_candidate_probability": 0.0746
}
```

#### Support Vector Machine (SVM) Model

**Endpoint**: `POST /api/ml/predict`

```json
{
  "model": "svm",
  "datasource": "manual",
  "features": {
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
  },
  "predict": true
}
```

**Response**:

```json
{
  "candidate_probability": 0.8792,
  "non_candidate_probability": 0.1208
}
```

### Pre-loaded Data

Use pre-loaded datasets for batch predictions.

#### Kepler Data - Gradient Boosting (GB)

**Endpoint**: `POST /api/ml/predict`

```json
{
  "model": "gb",
  "datasource": "pre-loaded",
  "data": "kepler",
  "predict": true
}
```

**Response**:

```json
{
  "candidate_probability": 0.6128,
  "non_candidate_probability": 0.3872,
  "first": {
    "kepid": "10000001",
    "candidate_probability": 0.8765,
    "non_candidate_probability": 0.1235
  },
  "second": {
    "kepid": "10000018",
    "candidate_probability": 0.2341,
    "non_candidate_probability": 0.7659
  },
  "third": {
    "kepid": "10000056",
    "candidate_probability": 0.9876,
    "non_candidate_probability": 0.0124
  },
  "fourth": {
    "kepid": "10000106",
    "candidate_probability": 0.3452,
    "non_candidate_probability": 0.6548
  },
  "fifth": {
    "kepid": "10000109",
    "candidate_probability": 0.7845,
    "non_candidate_probability": 0.2155
  },
  "sixth": {
    "kepid": "10000214",
    "candidate_probability": 0.4567,
    "non_candidate_probability": 0.5433
  },
  "seventh": {
    "kepid": "10000349",
    "candidate_probability": 0.8975,
    "non_candidate_probability": 0.1025
  },
  "eighth": {
    "kepid": "10000423",
    "candidate_probability": 0.1234,
    "non_candidate_probability": 0.8766
  },
  "ninth": {
    "kepid": "10000502",
    "candidate_probability": 0.6789,
    "non_candidate_probability": 0.3211
  },
  "tenth": {
    "kepid": "10000571",
    "candidate_probability": 0.5432,
    "non_candidate_probability": 0.4568
  }
}
```

#### TESS Data - Support Vector Machine (SVM)

**Endpoint**: `POST /api/ml/predict`

```json
{
  "model": "svm",
  "datasource": "pre-loaded",
  "data": "tess",
  "predict": true
}
```

**Response**:

```json
{
  "candidate_probability": 0.5128,
  "non_candidate_probability": 0.4872,
  "first": {
    "kepid": "TIC 2021993",
    "candidate_probability": 0.7652,
    "non_candidate_probability": 0.2348
  },
  "second": {
    "kepid": "TIC 2066322",
    "candidate_probability": 0.4321,
    "non_candidate_probability": 0.5679
  },
  "third": {
    "kepid": "TIC 2159205",
    "candidate_probability": 0.8976,
    "non_candidate_probability": 0.1024
  },
  "fourth": {
    "kepid": "TIC 2192012",
    "candidate_probability": 0.2345,
    "non_candidate_probability": 0.7655
  },
  "fifth": {
    "kepid": "TIC 2234054",
    "candidate_probability": 0.6789,
    "non_candidate_probability": 0.3211
  },
  "sixth": {
    "kepid": "TIC 2275265",
    "candidate_probability": 0.3456,
    "non_candidate_probability": 0.6544
  },
  "seventh": {
    "kepid": "TIC 2319444",
    "candidate_probability": 0.7890,
    "non_candidate_probability": 0.2110
  },
  "eighth": {
    "kepid": "TIC 2337343",
    "candidate_probability": 0.2109,
    "non_candidate_probability": 0.7891
  },
  "ninth": {
    "kepid": "TIC 2409807",
    "candidate_probability": 0.5678,
    "non_candidate_probability": 0.4322
  },
  "tenth": {
    "kepid": "TIC 2448650",
    "candidate_probability": 0.4567,
    "non_candidate_probability": 0.5433
  }
}
```

### Upload Multiple Targets

Submit multiple feature sets for batch processing.

#### Gradient Boosting (GB) with Multiple Targets

**Endpoint**: `POST /api/ml/predict`

```json
{
  "model": "gb",
  "datasource": "upload",
  "features-target-1": {
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
  },
  "features-target-2": {
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
  },
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
  "predict": true
}
```

**Response**:

```json
{
  "candidate_probability": 0.8234,
  "non_candidate_probability": 0.1766,
  "predictions": {
    "features-target-1": {
      "target_name": "features-target-1",
      "candidate_probability": 0.9254,
      "non_candidate_probability": 0.0746
    },
    "features-target-2": {
      "target_name": "features-target-2",
      "candidate_probability": 0.8792,
      "non_candidate_probability": 0.1208
    },
    "features-target-3": {
      "target_name": "features-target-3",
      "candidate_probability": 0.6657,
      "non_candidate_probability": 0.3343
    }
  }
}
```

#### Support Vector Machine (SVM) with Multiple Targets

**Endpoint**: `POST /api/ml/predict`

```json
{
  "model": "svm",
  "datasource": "upload",
  "features-target-1": {
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
  },
  "features-target-2": {
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
  },
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
  "predict": true
}
```

**Response**:

```json
{
  "candidate_probability": 0.7128,
  "non_candidate_probability": 0.2872,
  "predictions": {
    "features-target-1": {
      "target_name": "features-target-1",
      "candidate_probability": 0.9128,
      "non_candidate_probability": 0.0872
    },
    "features-target-2": {
      "target_name": "features-target-2",
      "candidate_probability": 0.8654,
      "non_candidate_probability": 0.1346
    },
    "features-target-3": {
      "target_name": "features-target-3",
      "candidate_probability": 0.7123,
      "non_candidate_probability": 0.2877
    },
    "features-target-4": {
      "target_name": "features-target-4",
      "candidate_probability": 0.3606,
      "non_candidate_probability": 0.6394
    }
  }
}
```

### Test Data Source

Use specific Kepler IDs from the test dataset for prediction.

#### Gradient Boosting (GB) with Test Data

**Endpoint**: `POST /api/ml/predict`

```json
{
  "model": "gb",
  "datasource": "test",
  "kepid": "10016874",
  "predict": true
}
```

**Response**:

```json
{
  "candidate_probability": 0.8921,
  "non_candidate_probability": 0.1079
}
```

#### Support Vector Machine (SVM) with Test Data

**Endpoint**: `POST /api/ml/predict`

```json
{
  "model": "svm",
  "datasource": "test",
  "kepid": "10024051",
  "predict": true
}
```

**Response**:

```json
{
  "candidate_probability": 0.7634,
  "non_candidate_probability": 0.2366
}
```

## Informational Endpoints

### Root Endpoint

Provides general API information.

**Endpoint**: `GET /`

**Response**:

```json
{
  "message": "Welcome to Exoplanet Classification API",
  "version": "2.0.0",
  "description": "Real CNN/DNN models trained on Kepler telescope data",
  "models": {
    "cnn": "Convolutional Neural Network for light curve analysis",
    "dnn": "Dual-input Deep Neural Network (time series + features)",
    "gb": "Gradient Boosting for KOI feature classification",
    "svm": "Support Vector Machine for KOI feature classification"
  },
  "endpoints": {
    "dl_predict": "/api/dl/predict",
    "ml_predict": "/api/ml/predict",
    "available_ids": "/api/dl/available-ids",
    "docs": "/docs"
  }
}
```

### Health Check

Check API and model health status.

**Endpoint**: `GET /health`

**Response**:

```json
{
  "status": "healthy",
  "models": {
    "cnn_loaded": true,
    "dnn_loaded": true,
    "data_available": true
  }
}
```

### Models Listing

List all available models.

**Endpoint**: `GET /models`

**Response**:

```json
{
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
      "name": "gb",
      "type": "Gradient Boosting",
      "input": "14 KOI features",
      "file": "exchron-gb.joblib"
    },
    {
      "name": "svm",
      "type": "Support Vector Machine", 
      "input": "14 KOI features",
      "file": "exchron-svm.joblib"
    }
  ]
}
```

### Available Kepler IDs

Get list of available Kepler IDs in the dataset.

**Endpoint**: `GET /api/dl/available-ids`

**Response**:

```json
{
  "total_available": 40,
  "sample_ids": [
    {"kepid": "10000490", "ground_truth": "CANDIDATE"},
    {"kepid": "10002261", "ground_truth": "FALSE POSITIVE"},
    {"kepid": "10002866", "ground_truth": "CANDIDATE"},
    {"kepid": "10004738", "ground_truth": "FALSE POSITIVE"},
    {"kepid": "10006096", "ground_truth": "CONFIRMED"},
    {"kepid": "10015516", "ground_truth": "FALSE POSITIVE"},
    {"kepid": "10016874", "ground_truth": "CANDIDATE"},
    {"kepid": "10020423", "ground_truth": "FALSE POSITIVE"},
    {"kepid": "10024051", "ground_truth": "CANDIDATE"},
    {"kepid": "10026457", "ground_truth": "FALSE POSITIVE"},
    {"kepid": "10028792", "ground_truth": "CONFIRMED"},
    {"kepid": "10031409", "ground_truth": "FALSE POSITIVE"},
    {"kepid": "10031808", "ground_truth": null},
    {"kepid": "10063802", "ground_truth": null},
    {"kepid": "10091110", "ground_truth": null},
    {"kepid": "10095512", "ground_truth": null},
    {"kepid": "10123064", "ground_truth": null},
    {"kepid": "10129482", "ground_truth": null},
    {"kepid": "10136549", "ground_truth": null},
    {"kepid": "10153011", "ground_truth": null}
  ],
  "note": "Use any of these Kepler IDs for predictions"
}
```

### Deep Learning Models List

Get information about available deep learning models.

**Endpoint**: `GET /api/dl/models`

**Response**:

```json
{
  "models": [
    {
      "name": "cnn",
      "description": "Convolutional Neural Network for time series analysis",
      "input_shape": "(3000, 1)",
      "input_description": "Normalized light curve flux data"
    },
    {
      "name": "dnn", 
      "description": "Dual-input Deep Neural Network with softmax output for probability classification",
      "input_shape": "[(3000,), (12,)]",
      "input_description": "Time series data + 12 engineered features",
      "output_description": "Probability distribution over candidate/non-candidate classes",
      "architecture": "Updated with softmax activation for explicit probabilities"
    }
  ]
}
```

### Machine Learning Models List

Get information about available machine learning models.

**Endpoint**: `GET /api/ml/models`

**Response**:

```json
{
  "models": ["gb", "svm"],
  "description": "Gradient Boosting and Support Vector Machine for KOI feature-based classification"
}
```

### Required Features List

Get information about required features for machine learning models.

**Endpoint**: `GET /api/ml/features`

**Response**:

```json
{
  "required_features": [
    "koi_period",
    "koi_time0bk",
    "koi_impact", 
    "koi_duration",
    "koi_depth",
    "koi_incl",
    "koi_model_snr",
    "koi_count",
    "koi_bin_oedp_sig",
    "koi_steff",
    "koi_slogg",
    "koi_srad",
    "koi_smass",
    "koi_kepmag"
  ],
  "descriptions": {
    "koi_period": "Orbital period in days",
    "koi_time0bk": "Transit epoch in Barycentric Kepler Julian Day (BKJD)",
    "koi_impact": "Impact parameter",
    "koi_duration": "Transit duration in hours",
    "koi_depth": "Transit depth in parts per million (ppm)",
    "koi_incl": "Inclination in degrees",
    "koi_model_snr": "Transit signal-to-noise ratio",
    "koi_count": "Number of transits observed",
    "koi_bin_oedp_sig": "Odd-even depth comparison significance",
    "koi_steff": "Stellar effective temperature in Kelvin",
    "koi_slogg": "Stellar surface gravity (log g)",
    "koi_srad": "Stellar radius in solar radii",
    "koi_smass": "Stellar mass in solar masses",
    "koi_kepmag": "Kepler magnitude"
  }
}
```

### Debug Features

Get detailed feature information for a specific Kepler ID.

**Endpoint**: `GET /api/dl/debug-features/{kepid}`

Example: `GET /api/dl/debug-features/10000490`

**Response**:

```json
{
  "kepid": "10000490",
  "features": [
    {
      "feature": "period",
      "description": "Orbital period (days)",
      "raw_value": 10.00506974,
      "normalized_value": 0.2347,
      "training_mean": 8.25,
      "training_std": 7.44
    },
    {
      "feature": "impact",
      "description": "Impact parameter",
      "raw_value": 0.148,
      "normalized_value": -0.6789,
      "training_mean": 0.54,
      "training_std": 0.58
    },
    {
      "feature": "duration",
      "description": "Transit duration (hours)",
      "raw_value": 3.481,
      "normalized_value": 0.1432,
      "training_mean": 3.12,
      "training_std": 2.53
    },
    {
      "feature": "depth",
      "description": "Transit depth (ppm)",
      "raw_value": 143.3,
      "normalized_value": -0.7812,
      "training_mean": 584.53,
      "training_std": 565.23
    },
    {
      "feature": "stellar_temp",
      "description": "Stellar temperature (K)",
      "raw_value": 5912.0,
      "normalized_value": 0.2341,
      "training_mean": 5625.35,
      "training_std": 1225.76
    },
    {
      "feature": "stellar_radius",
      "description": "Stellar radius (solar radii)",
      "raw_value": 0.924,
      "normalized_value": -0.3476,
      "training_mean": 1.15,
      "training_std": 0.65
    },
    {
      "feature": "stellar_mass",
      "description": "Stellar mass (solar masses)",
      "raw_value": 0.884,
      "normalized_value": -0.5342,
      "training_mean": 1.06,
      "training_std": 0.33
    },
    {
      "feature": "inclination",
      "description": "Orbital inclination (degrees)",
      "raw_value": 89.61,
      "normalized_value": 0.7432,
      "training_mean": 87.32,
      "training_std": 3.08
    },
    {
      "feature": "snr",
      "description": "Transit signal-to-noise ratio",
      "raw_value": 11.4,
      "normalized_value": -0.3267,
      "training_mean": 19.87,
      "training_std": 25.89
    },
    {
      "feature": "transit_count",
      "description": "Number of observed transits",
      "raw_value": 2.0,
      "normalized_value": -1.1342,
      "training_mean": 6.45,
      "training_std": 3.92
    },
    {
      "feature": "epoch",
      "description": "Transit epoch (BKJD)",
      "raw_value": 136.83029,
      "normalized_value": -0.0432,
      "training_mean": 142.32,
      "training_std": 126.98
    },
    {
      "feature": "odd_even_sig",
      "description": "Odd-even depth significance",
      "raw_value": 0.4606,
      "normalized_value": -0.2341,
      "training_mean": 0.65,
      "training_std": 0.81
    }
  ],
  "summary": {
    "raw_range": [0.148, 5912.0],
    "normalized_range": [-1.1342, 0.7432],
    "normalization_applied": true
  }
}
```

## Error Examples

### Invalid Model Type

**Request**:

```json
{
  "model": "invalid_model",
  "kepid": "10000490",
  "predict": true
}
```

**Response** (Status Code: 400):

```json
{
  "detail": "Invalid model type: invalid_model. Must be 'cnn' or 'dnn'"
}
```

### Invalid Kepler ID

**Request**:

```json
{
  "model": "cnn",
  "kepid": "99999999",
  "predict": true
}
```

**Response** (Status Code: 404):

```json
{
  "detail": "Kepler ID 99999999 not found in dataset. Use /api/dl/available-ids to see valid IDs."
}
```

### Missing Required Fields

**Request**:

```json
{
  "model": "gb",
  "datasource": "manual"
}
```

**Response** (Status Code: 400):

```json
{
  "detail": "KOI features required for manual data source"
}
```

### Invalid Data Source

**Request**:

```json
{
  "model": "svm",
  "datasource": "invalid_source",
  "predict": true
}
```

**Response** (Status Code: 400):

```json
{
  "detail": "Invalid datasource: invalid_source. Must be 'manual', 'test', 'pre-loaded', or 'upload'"
}
```