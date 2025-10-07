from fastapi import APIRouter, HTTPException
from app.schemas.requests import DLModelRequest
from app.schemas.responses import DLPredictionResponse, ErrorResponse
from app.services.prediction_service import get_dl_prediction
from app.services.data_service import check_kepid_exists, get_ground_truth
from typing import Union
import os
import pandas as pd

router = APIRouter()

@router.post("/predict", response_model=Union[DLPredictionResponse, ErrorResponse])
async def predict_with_dl_model(request: DLModelRequest):
    """Make predictions using deep learning models (CNN/DNN)"""
    try:
        if request.model not in ['cnn', 'dnn']:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid model type: {request.model}. Must be 'cnn' or 'dnn'"
            )
        
        if not request.predict:
            return {"message": "Prediction not requested"}
        
        # Validate that kepid exists
        if not await check_kepid_exists(request.kepid):
            raise HTTPException(
                status_code=404,
                detail=f"Kepler ID {request.kepid} not found in dataset. Use /api/dl/available-ids to see valid IDs."
            )
        
        # Call prediction service
        result = await get_dl_prediction(request.model, request.kepid)
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        return ErrorResponse(error=str(e))

@router.get("/models")
async def list_dl_models():
    """List available deep learning models"""
    return {
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

@router.get("/available-ids")
async def get_available_kepler_ids():
    """Get list of available Kepler IDs in the dataset"""
    try:
        data_dir = "data/lightkurve_data"
        if not os.path.exists(data_dir):
            return {"error": "Data directory not found"}
        
        # Get all kepler files
        files = [f for f in os.listdir(data_dir) if f.startswith("kepler_") and f.endswith(".csv")]
        
        # Extract kepler IDs
        kepler_ids = []
        for file in files:
            try:
                # Extract ID from filename like "kepler_10904857_lightkurve.csv"
                kepid = file.replace("kepler_", "").replace("_lightkurve.csv", "")
                kepler_ids.append(kepid)
            except:
                continue
        
        # Sort numerically
        kepler_ids.sort(key=lambda x: int(x))
        
        # Get ground truth labels if available
        labeled_ids = []
        try:
            metadata_path = "data/lightkurve_test_metadata.csv"
            if os.path.exists(metadata_path):
                metadata = pd.read_csv(metadata_path)
                for kepid in kepler_ids[:20]:  # Show first 20 with labels
                    label = None
                    row = metadata[metadata['kepid'] == int(kepid)]
                    if not row.empty:
                        label = row.iloc[0]['koi_disposition']
                    labeled_ids.append({"kepid": kepid, "ground_truth": label})
        except:
            labeled_ids = [{"kepid": kepid, "ground_truth": None} for kepid in kepler_ids[:20]]
        
        return {
            "total_available": len(kepler_ids),
            "sample_ids": labeled_ids,
            "note": "Use any of these Kepler IDs for predictions"
        }
    
    except Exception as e:
        return {"error": f"Failed to retrieve available IDs: {str(e)}"}

@router.get("/debug-features/{kepid}")
async def debug_features(kepid: str):
    """Debug endpoint to inspect feature extraction and normalization"""
    try:
        from app.services.data_service import get_engineered_features
        from app.services.feature_normalizer import get_feature_normalizer
        
        # Get raw and normalized features
        normalized_features = await get_engineered_features(kepid)
        
        # Get normalizer info
        normalizer = get_feature_normalizer()
        feature_info = normalizer.get_feature_info()
        
        # Calculate raw features for comparison
        import numpy as np
        raw_features = (normalized_features * np.array([info['std'] for info in feature_info]).reshape(1, -1) + 
                       np.array([info['mean'] for info in feature_info]).reshape(1, -1))
        
        # Format response
        features_comparison = []
        for i, info in enumerate(feature_info):
            features_comparison.append({
                "feature": info['name'],
                "description": info['description'],
                "raw_value": float(raw_features[0][i]),
                "normalized_value": float(normalized_features[0][i]),
                "training_mean": info['mean'],
                "training_std": info['std']
            })
        
        return {
            "kepid": kepid,
            "features": features_comparison,
            "summary": {
                "raw_range": [float(raw_features.min()), float(raw_features.max())],
                "normalized_range": [float(normalized_features.min()), float(normalized_features.max())],
                "normalization_applied": True
            }
        }
    
    except Exception as e:
        return {"error": f"Failed to debug features for {kepid}: {str(e)}"}