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
    PRE_LOADED = "pre-loaded"

class DataType(str, Enum):
    KEPLER = "kepler"
    TESS = "tess"

class DLModelRequest(BaseModel):
    model: ModelType = Field(..., description="Deep learning model type (cnn or dnn)")
    kepid: str = Field(..., description="Kepler ID for the target exoplanet")
    predict: bool = Field(True, description="Flag to run prediction")

class MLModelRequest(BaseModel):
    model: ModelType = Field(..., description="ML model type (gb or svm)", examples=["gb", "svm"])
    datasource: DataSource = Field(..., description="Source of input data", examples=["manual", "test", "pre-loaded"])
    data: Optional[DataType] = Field(None, description="Data type for pre-loaded datasource (kepler or tess)", examples=["kepler", "tess"])
    kepid: Optional[str] = Field(None, description="Kepler ID for test data", examples=["123456"])
    features: Optional[Dict[str, float]] = Field(None, description="Features containing KOI parameters: koi_period, koi_time0bk, koi_impact, koi_duration, koi_depth, koi_incl, koi_model_snr, koi_count, koi_bin_oedp_sig, koi_steff, koi_slogg, koi_srad, koi_smass, koi_kepmag")
    predict: bool = Field(True, description="Flag to run prediction")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "model": "gb",
                    "datasource": "pre-loaded",
                    "data": "kepler",
                    "predict": True
                },
                {
                    "model": "gb",
                    "datasource": "manual",
                    "features": {
                        "koi_period": 10.005,
                        "koi_time0bk": 136.830,
                        "koi_impact": 0.148,
                        "koi_duration": 3.481,
                        "koi_depth": 143.3,
                        "koi_incl": 89.61,
                        "koi_model_snr": 11.4,
                        "koi_count": 2,
                        "koi_bin_oedp_sig": 0.461,
                        "koi_steff": 5912,
                        "koi_slogg": 4.453,
                        "koi_srad": 0.924,
                        "koi_smass": 0.884,
                        "koi_kepmag": 14.634
                    },
                    "predict": True
                }
            ]
        }
    }