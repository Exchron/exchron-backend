from fastapi import APIRouter, HTTPException
from app.schemas.requests import MLModelRequest
from app.schemas.responses import MLPredictionResponse, ErrorResponse
from app.services.prediction_service import get_ml_prediction
from typing import Union

router = APIRouter()

@router.post("/predict", response_model=Union[MLPredictionResponse, ErrorResponse])
async def predict_with_ml_model(request: MLModelRequest):
    """Make predictions using machine learning models (XGBoost/SVM/KNN)"""
    try:
        if request.model not in ['xgboost', 'svm', 'knn']:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid model type: {request.model}. Must be 'xgboost', 'svm', or 'knn'"
            )
        
        if not request.predict:
            return {"message": "Prediction not requested"}
        
        if request.datasource == "manual" and not request.features:
            raise HTTPException(
                status_code=400, 
                detail="Features required for manual data source"
            )
        
        if request.datasource == "test" and not request.kepid:
            raise HTTPException(
                status_code=400, 
                detail="Kepler ID required for test data source"
            )
        
        # Call prediction service
        result = await get_ml_prediction(
            model_type=request.model,
            datasource=request.datasource,
            kepid=request.kepid,
            features=request.features
        )
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        return ErrorResponse(error=str(e))

@router.get("/models")
async def list_ml_models():
    """List available machine learning models"""
    return {
        "models": ["xgboost", "svm", "knn"],
        "description": "XGBoost, Support Vector Machine, and K-Nearest Neighbors for feature-based classification"
    }

@router.get("/features")
async def get_required_features():
    """Get the list of required features for manual input"""
    return {
        "required_features": [
            "period",
            "impact", 
            "duration",
            "depth",
            "temp",
            "logg",
            "metallicity"
        ],
        "descriptions": {
            "period": "Orbital period in days",
            "impact": "Impact parameter",
            "duration": "Transit duration in hours",
            "depth": "Transit depth in ppm",
            "temp": "Stellar effective temperature in K",
            "logg": "Stellar surface gravity",
            "metallicity": "Stellar metallicity [Fe/H]"
        }
    }