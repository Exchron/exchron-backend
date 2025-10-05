from pydantic import BaseModel, Field
from typing import Dict, Optional, Any

class DLPredictionResponse(BaseModel):
    candidate_probability: float = Field(..., description="Probability of being an exoplanet candidate")
    non_candidate_probability: float = Field(..., description="Probability of not being an exoplanet candidate")
    lightcurve_link: str = Field(..., description="Link to the NASA archive for lightcurve data")
    dv_report_link: str = Field(..., description="Link to the DV report")
    kepid: str = Field(..., description="Kepler ID used for prediction")
    model_used: str = Field(..., description="Model used for prediction")

class MLPredictionResponse(BaseModel):
    prediction: float = Field(..., description="Prediction result (probability or class)")
    prediction_class: str = Field(..., description="Predicted class (e.g., 'candidate', 'non-candidate')")
    features_used: Dict[str, float] = Field(..., description="Features used for prediction")
    model_used: str = Field(..., description="Model used for prediction")
    kepid: Optional[str] = Field(None, description="Kepler ID if applicable")

class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")
    details: Optional[Any] = Field(None, description="Additional error details")