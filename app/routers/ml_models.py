from fastapi import APIRouter, HTTPException
from app.schemas.requests import MLModelRequest
from app.schemas.responses import MLPredictionResponse, AveragedMLPredictionResponse, UploadMLPredictionResponse, ErrorResponse
from app.services.prediction_service import get_ml_prediction, get_averaged_ml_prediction, get_upload_ml_prediction
from typing import Union, Dict, Any

router = APIRouter()

@router.post("/predict", response_model=Union[MLPredictionResponse, AveragedMLPredictionResponse, UploadMLPredictionResponse, ErrorResponse])
async def predict_with_ml_model(request: Dict[str, Any]):
    """Make predictions using machine learning models (GB/SVM)"""
    try:
        # Extract basic fields
        model_type = request.get("model")
        datasource = request.get("datasource")
        predict = request.get("predict", True)
        
        if model_type not in ['gb', 'svm']:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid model type: {model_type}. Must be 'gb' or 'svm'"
            )
        
        if not predict:
            return {"message": "Prediction not requested"}
        
        # Handle new pre-loaded datasource format
        if datasource == "pre-loaded":
            data_type = request.get("data")
            if not data_type:
                raise HTTPException(
                    status_code=400,
                    detail="Data type (kepler/tess) required for pre-loaded data source"
                )
            
            # Call the new averaged prediction service
            result = await get_averaged_ml_prediction(
                model_type=model_type,
                data_type=data_type
            )
            return result
        
        # Handle upload datasource
        if datasource == "upload":
            # Extract feature sets dynamically from the request
            upload_features = {}
            for key, value in request.items():
                if key.startswith("features-target-") and isinstance(value, dict):
                    upload_features[key] = value
            
            if not upload_features:
                raise HTTPException(
                    status_code=400,
                    detail="Upload features (features-target-*) required for upload data source"
                )
            
            # Call upload prediction service
            result = await get_upload_ml_prediction(
                model_type=model_type,
                upload_features=upload_features
            )
            return result
        
        # Handle existing datasource formats
        if datasource == "manual":
            features = request.get("features")
            if not features:
                raise HTTPException(
                    status_code=400, 
                    detail="KOI features required for manual data source"
                )
            
            # Call existing prediction service for manual datasource
            result = await get_ml_prediction(
                model_type=model_type,
                datasource=datasource,
                kepid=None,
                features=features
            )
            return result
        
        if datasource == "test":
            kepid = request.get("kepid")
            if not kepid:
                raise HTTPException(
                    status_code=400, 
                    detail="Kepler ID required for test data source"
                )
            
            # Call existing prediction service for test datasource
            result = await get_ml_prediction(
                model_type=model_type,
                datasource=datasource,
                kepid=kepid,
                features=None
            )
            return result
        
        raise HTTPException(
            status_code=400,
            detail=f"Invalid datasource: {datasource}. Must be 'manual', 'test', 'pre-loaded', or 'upload'"
        )
    
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