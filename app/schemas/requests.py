from enum import Enum
from typing import Optional, Dict
from pydantic import BaseModel, Field

class ModelType(str, Enum):
    CNN = "cnn"
    DNN = "dnn"
    XGBOOST = "xgboost"
    SVM = "svm"
    KNN = "knn"

class DataSource(str, Enum):
    MANUAL = "manual"
    TEST = "test"

class DLModelRequest(BaseModel):
    model: ModelType = Field(..., description="Deep learning model type (cnn or dnn)")
    kepid: str = Field(..., description="Kepler ID for the target exoplanet")
    predict: bool = Field(True, description="Flag to run prediction")

class MLModelRequest(BaseModel):
    model: ModelType = Field(..., description="ML model type (xgboost, svm, or knn)")
    datasource: DataSource = Field(..., description="Source of input data")
    kepid: Optional[str] = Field(None, description="Kepler ID for test data")
    features: Optional[Dict[str, float]] = Field(None, description="Features for manual input")
    predict: bool = Field(True, description="Flag to run prediction")