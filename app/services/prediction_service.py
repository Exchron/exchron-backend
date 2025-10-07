from app.models.model_loader import get_model
from app.services.data_service import (
    get_time_series_data,
    get_engineered_features,
    get_feature_data_from_kepid,
    process_manual_features,
    check_kepid_exists,
    get_ground_truth
)
from app.services.url_service import get_archive_links
from app.schemas.responses import DLPredictionResponse, MLPredictionResponse
import numpy as np
import pandas as pd
from typing import Dict, Optional

# Model Output Specifications:
# - CNN: Uses sigmoid activation, outputs single probability for candidate class
# - DNN: Uses softmax activation, outputs probability distribution [non_candidate_prob, candidate_prob]

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
    
    # Process prediction results based on model type
    if model_type.lower() == "cnn":
        # CNN still uses sigmoid output - single probability for positive class
        candidate_prob = float(prediction[0][0])
        non_candidate_prob = 1.0 - candidate_prob
    elif model_type.lower() == "dnn":
        # DNN now uses softmax output - probability distribution over two classes
        # prediction shape: (1, 2) where [0] = non-candidate prob, [1] = candidate prob
        non_candidate_prob = float(prediction[0][0])  # Class 0: Non-candidate probability
        candidate_prob = float(prediction[0][1])      # Class 1: Candidate probability
    
    # Get ground truth if available
    ground_truth = await get_ground_truth(kepid)
    
    # Generate NASA archive links using the new URL service
    archive_links = get_archive_links(kepid)
    
    return DLPredictionResponse(
        candidate_probability=candidate_prob,
        non_candidate_probability=non_candidate_prob,
        lightcurve_link=archive_links["lightcurve_link"],
        target_pixel_file_link=archive_links["target_pixel_file_link"],
        dv_report_link=archive_links["dv_report_link"],
        kepid=kepid,
        model_used=model_type.upper()
    )

async def get_ml_prediction(
    model_type: str, 
    datasource: str, 
    kepid: Optional[str] = None,
    features: Optional[Dict[str, float]] = None
) -> MLPredictionResponse:
    """Get prediction using machine learning models (GB/SVM)"""
    from app.services.data_service import check_kepid_exists_in_koi_data
    
    # Validate model type
    if model_type not in ['gb', 'svm']:
        raise ValueError(f"Invalid model type: {model_type}. Must be 'gb' or 'svm'")
    
    # Load model
    model = get_model(model_type)
    
    # Prepare input features based on data source
    if datasource == "test":
        if not kepid:
            raise ValueError("Kepler ID required for test data source")
        if not await check_kepid_exists_in_koi_data(kepid):
            raise ValueError(f"Kepler ID {kepid} not found in KOI test data")
        input_features = await get_feature_data_from_kepid(kepid)
    elif datasource == "manual":
        if not features:
            raise ValueError("Features required for manual data source")
        input_features = await process_manual_features(features)
    else:
        raise ValueError(f"Invalid data source: {datasource}")
    
    # Convert to numpy array for prediction
    feature_array = input_features.values
    
    # Make prediction with probability
    if hasattr(model, 'predict_proba'):
        prediction_proba = model.predict_proba(feature_array)[0]
        candidate_prob = float(prediction_proba[1])  # Probability of candidate class
        non_candidate_prob = float(prediction_proba[0])  # Probability of non-candidate class
    else:
        # Fallback for models without predict_proba
        prediction = model.predict(feature_array)[0]
        candidate_prob = float(prediction) if prediction > 0.5 else 0.0
        non_candidate_prob = 1.0 - candidate_prob
    
    return MLPredictionResponse(
        candidate_probability=candidate_prob,
        non_candidate_probability=non_candidate_prob
    )