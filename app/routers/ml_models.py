from fastapi import APIRouter, HTTPException
from app.schemas.requests import MLModelRequest
from app.schemas.responses import MLPredictionResponse, AveragedMLPredictionResponse, ErrorResponse
from app.services.prediction_service import get_ml_prediction, get_averaged_ml_prediction
from typing import Union

router = APIRouter()

@router.post("/predict", response_model=Union[MLPredictionResponse, AveragedMLPredictionResponse, ErrorResponse])
async def predict_with_ml_model(request: MLModelRequest):
    """Make predictions using machine learning models (GB/SVM)"""
    try:
        if request.model not in ['gb', 'svm']:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid model type: {request.model}. Must be 'gb' or 'svm'"
            )
        
        if not request.predict:
            return {"message": "Prediction not requested"}
        
        # Handle new pre-loaded datasource format
        if request.datasource == "pre-loaded":
            if not request.data:
                raise HTTPException(
                    status_code=400,
                    detail="Data type (kepler/tess) required for pre-loaded data source"
                )
            
            # Call the new averaged prediction service
            result = await get_averaged_ml_prediction(
                model_type=request.model,
                data_type=request.data
            )
            return result
        
        # Handle existing datasource formats
        if request.datasource == "manual" and not request.features:
            raise HTTPException(
                status_code=400, 
                detail="KOI features required for manual data source"
            )
        
        if request.datasource == "test" and not request.kepid:
            raise HTTPException(
                status_code=400, 
                detail="Kepler ID required for test data source"
            )
        
        # Call existing prediction service for manual/test datasources
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
        "models": ["gb", "svm"],
        "description": "Gradient Boosting and Support Vector Machine for KOI feature-based classification"
    }

@router.get("/features")
async def get_required_features():
    """Get the list of required KOI features for manual input"""
    return {
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