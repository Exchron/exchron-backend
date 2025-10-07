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

class IndividualPrediction(BaseModel):
    kepid: str = Field(..., description="Kepler ID")
    candidate_probability: float = Field(..., description="Probability of being an exoplanet candidate")
    non_candidate_probability: float = Field(..., description="Probability of not being an exoplanet candidate")

class AveragedMLPredictionResponse(BaseModel):
    candidate_probability: float = Field(..., description="Average probability of being an exoplanet candidate across first 10 predictions")
    non_candidate_probability: float = Field(..., description="Average probability of not being an exoplanet candidate across first 10 predictions")
    first: IndividualPrediction = Field(..., description="First individual prediction")
    second: IndividualPrediction = Field(..., description="Second individual prediction")
    third: IndividualPrediction = Field(..., description="Third individual prediction")
    fourth: IndividualPrediction = Field(..., description="Fourth individual prediction")
    fifth: IndividualPrediction = Field(..., description="Fifth individual prediction")
    sixth: IndividualPrediction = Field(..., description="Sixth individual prediction")
    seventh: IndividualPrediction = Field(..., description="Seventh individual prediction")
    eighth: IndividualPrediction = Field(..., description="Eighth individual prediction")
    ninth: IndividualPrediction = Field(..., description="Ninth individual prediction")
    tenth: IndividualPrediction = Field(..., description="Tenth individual prediction")

class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")
    details: Optional[Any] = Field(None, description="Additional error details")