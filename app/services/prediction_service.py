from app.models.model_loader import get_model
from app.services.data_service import (
    get_time_series_data,
    get_engineered_features,
    get_feature_data_from_kepid,
    process_manual_features,
    check_kepid_exists,
    get_ground_truth
)
from app.schemas.responses import DLPredictionResponse, MLPredictionResponse
import numpy as np
import pandas as pd
from typing import Dict, Optional

async def get_dl_prediction(model_type: str, kepid: str) -> DLPredictionResponse:
    """Get prediction using deep learning models (CNN/DNN)"""
    # Check if kepid exists in dataset
    if not await check_kepid_exists(kepid):
        raise ValueError(f"Kepler ID {kepid} not found in dataset")
    
    # Load model
    model = get_model(model_type)
    
    # Prepare inputs based on model type
    if model_type.lower() == "cnn":
        # CNN expects only time series data: shape (1, 3000, 1)
        time_series_data = await get_time_series_data(kepid)
        preprocessed_data = time_series_data.reshape(1, 3000, 1)
        
        # Make prediction
        prediction = model.predict(preprocessed_data)
        
    elif model_type.lower() == "dnn":
        # DNN expects both time series and engineered features
        time_series_data = await get_time_series_data(kepid)
        engineered_features = await get_engineered_features(kepid)
        
        # Prepare inputs for dual-input DNN model
        time_series_input = time_series_data.flatten().reshape(1, -1)  # Shape: (1, 3000)
        features_input = engineered_features  # Shape: (1, 12)
        
        # Make prediction with both inputs
        prediction = model.predict([time_series_input, features_input])
    else:
        raise ValueError(f"Invalid deep learning model type: {model_type}")
    
    # Process prediction results
    # The models output sigmoid probability for the positive class (CANDIDATE)
    candidate_prob = float(prediction[0][0])
    non_candidate_prob = 1.0 - candidate_prob
    
    # Get ground truth if available
    ground_truth = await get_ground_truth(kepid)
    
    # Generate NASA archive links
    lightcurve_link = f"https://exoplanetarchive.ipac.caltech.edu/cgi-bin/keplerLightCurveViewer/nph-keplerLCViewer?kepid={kepid}"
    dv_report_link = f"https://exoplanetarchive.ipac.caltech.edu/data/KeplerData/dv_reports/kepler{kepid}/kplr{kepid}-dv_report.pdf"
    
    return DLPredictionResponse(
        candidate_probability=candidate_prob,
        non_candidate_probability=non_candidate_prob,
        lightcurve_link=lightcurve_link,
        dv_report_link=dv_report_link,
        kepid=kepid,
        model_used=model_type.upper()
    )

async def get_ml_prediction(
    model_type: str, 
    datasource: str, 
    kepid: Optional[str] = None,
    features: Optional[Dict[str, float]] = None
) -> MLPredictionResponse:
    """Get prediction using machine learning models (XGBoost/SVM/KNN)"""
    # Load model
    model = get_model(model_type)
    
    # Prepare input features based on data source
    if datasource == "test":
        if not kepid:
            raise ValueError("Kepler ID required for test data source")
        input_features = await get_feature_data_from_kepid(kepid)
        features_used = input_features.iloc[0].to_dict()
    elif datasource == "manual":
        if not features:
            raise ValueError("Features required for manual data source")
        input_features = await process_manual_features(features)
        features_used = features
    else:
        raise ValueError(f"Invalid data source: {datasource}")
    
    # Convert to numpy array for prediction
    feature_array = input_features.values
    
    # Make prediction
    if hasattr(model, 'predict_proba'):
        prediction_proba = model.predict_proba(feature_array)[0]
        prediction_value = float(prediction_proba[1])  # Probability of positive class
    else:
        prediction_value = float(model.predict(feature_array)[0])
    
    # Determine prediction class
    prediction_class = "candidate" if prediction_value >= 0.5 else "non-candidate"
    
    return MLPredictionResponse(
        prediction=prediction_value,
        prediction_class=prediction_class,
        features_used=features_used,
        model_used=model_type.upper(),
        kepid=kepid if datasource == "test" else None
    )