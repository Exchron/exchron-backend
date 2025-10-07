from enum import Enum
from typing import Optional, Dict
from pydantic import BaseModel, Field

class ModelType(str, Enum):
    CNN = "cnn"
    DNN = "dnn"
    GB = "gb"
    SVM = "svm"

class DataSource(str, Enum):
    MANUAL = "manual"
    TEST = "test"

class DLModelRequest(BaseModel):
    model: ModelType = Field(..., description="Deep learning model type (cnn or dnn)")
    kepid: str = Field(..., description="Kepler ID for the target exoplanet")
    predict: bool = Field(True, description="Flag to run prediction")

class MLModelRequest(BaseModel):
    model: ModelType = Field(..., description="ML model type (gb or svm)")
    datasource: DataSource = Field(..., description="Source of input data")
    kepid: Optional[str] = Field(None, description="Kepler ID for test data")
    features: Optional[Dict[str, float]] = Field(None, description="Features containing KOI parameters: koi_period, koi_time0bk, koi_impact, koi_duration, koi_depth, koi_incl, koi_model_snr, koi_count, koi_bin_oedp_sig, koi_steff, koi_slogg, koi_srad, koi_smass, koi_kepmag")
    predict: bool = Field(True, description="Flag to run prediction")