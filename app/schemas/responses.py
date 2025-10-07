from pydantic import BaseModel, Field
from typing import Dict, Optional, Any

class DLPredictionResponse(BaseModel):
    candidate_probability: float = Field(..., description="Probability of being an exoplanet candidate")
    non_candidate_probability: float = Field(..., description="Probability of not being an exoplanet candidate")
    lightcurve_link: str = Field(..., description="Link to the STScI archive for lightcurve data files")
    target_pixel_file_link: str = Field(..., description="Link to the STScI archive for target pixel files")
    dv_report_link: str = Field(..., description="Link to the NASA Exoplanet Archive DV report")
    kepid: str = Field(..., description="Kepler ID used for prediction")
    model_used: str = Field(..., description="Model used for prediction")

class MLPredictionResponse(BaseModel):
    candidate_probability: float = Field(..., description="Probability of being an exoplanet candidate")
    non_candidate_probability: float = Field(..., description="Probability of not being an exoplanet candidate")

class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")
    details: Optional[Any] = Field(None, description="Additional error details")