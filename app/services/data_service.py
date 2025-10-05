import pandas as pd
import numpy as np
from fastapi import HTTPException
from typing import Dict, Any, Tuple
import os
from scipy import stats

# Data paths
DATA_DIR = "data"
LIGHTKURVE_DATA_DIR = os.path.join(DATA_DIR, "lightkurve_data")
TEST_METADATA_PATH = os.path.join(DATA_DIR, "lightkurve_test_metadata.csv")

async def get_time_series_data(kepid: str) -> np.ndarray:
    """Fetch real time series data for a given Kepler ID"""
    try:
        # Construct file path for the lightcurve data
        file_path = os.path.join(LIGHTKURVE_DATA_DIR, f"kepler_{kepid}_lightkurve.csv")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Lightcurve data not found for Kepler ID: {kepid}")
        
        # Read the lightcurve data
        data = pd.read_csv(file_path)
        
        # Extract flux data (prefer pdcsap_flux, fallback to flux)
        if 'pdcsap_flux' in data.columns:
            flux_data = data['pdcsap_flux'].dropna()
        elif 'flux' in data.columns:
            flux_data = data['flux'].dropna()
        else:
            raise ValueError("No flux data found in the lightcurve file")
        
        # Remove outliers (3-sigma clipping)
        mean_flux = flux_data.mean()
        std_flux = flux_data.std()
        outlier_mask = np.abs(flux_data - mean_flux) <= 3 * std_flux
        flux_clean = flux_data[outlier_mask]
        
        # Normalize the flux data (zero mean, unit variance)
        flux_normalized = (flux_clean - flux_clean.mean()) / flux_clean.std()
        
        # Pad or truncate to 3000 points as required by the model
        target_length = 3000
        if len(flux_normalized) >= target_length:
            # Truncate to first 3000 points
            flux_final = flux_normalized.iloc[:target_length].values
        else:
            # Pad with zeros
            flux_final = np.zeros(target_length)
            flux_final[:len(flux_normalized)] = flux_normalized.values
        
        return flux_final.reshape(-1, 1)
        
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Failed to fetch time series data: {str(e)}")

async def get_engineered_features(kepid: str) -> np.ndarray:
    """Extract 12 engineered features from lightcurve data for DNN model"""
    try:
        # Get the raw lightcurve data
        file_path = os.path.join(LIGHTKURVE_DATA_DIR, f"kepler_{kepid}_lightkurve.csv")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Lightcurve data not found for Kepler ID: {kepid}")
        
        data = pd.read_csv(file_path)
        
        # Extract flux data
        if 'pdcsap_flux' in data.columns:
            flux_data = data['pdcsap_flux'].dropna()
        elif 'flux' in data.columns:
            flux_data = data['flux'].dropna()
        else:
            raise ValueError("No flux data found in the lightcurve file")
        
        # Clean outliers
        mean_flux = flux_data.mean()
        std_flux = flux_data.std()
        outlier_mask = np.abs(flux_data - mean_flux) <= 3 * std_flux
        flux_clean = flux_data[outlier_mask]
        
        # Calculate 12 engineered features
        features = []
        
        # 1. Mean
        features.append(flux_clean.mean())
        
        # 2. Standard deviation
        features.append(flux_clean.std())
        
        # 3. Skewness
        features.append(stats.skew(flux_clean))
        
        # 4. Kurtosis
        features.append(stats.kurtosis(flux_clean))
        
        # 5. Minimum value
        features.append(flux_clean.min())
        
        # 6. Maximum value
        features.append(flux_clean.max())
        
        # 7. Range (max - min)
        features.append(flux_clean.max() - flux_clean.min())
        
        # 8. Median
        features.append(flux_clean.median())
        
        # 9. 25th percentile
        features.append(flux_clean.quantile(0.25))
        
        # 10. 75th percentile
        features.append(flux_clean.quantile(0.75))
        
        # 11. Interquartile range
        features.append(flux_clean.quantile(0.75) - flux_clean.quantile(0.25))
        
        # 12. Mean absolute deviation
        features.append(np.mean(np.abs(flux_clean - flux_clean.mean())))
        
        return np.array(features).reshape(1, -1)
        
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Failed to extract features: {str(e)}")

async def get_feature_data_from_kepid(kepid: str) -> pd.DataFrame:
    """Fetch feature data for a given Kepler ID from mock test data (for ML models)"""
    try:
        # This is for the traditional ML models - keeping mock data for now
        # In a real implementation, this would extract features differently
        np.random.seed(int(kepid) % 1000)
        features = {
            "period": np.random.uniform(1, 50),
            "impact": np.random.uniform(0, 1),
            "duration": np.random.uniform(1, 10),
            "depth": np.random.uniform(10, 1000),
            "temp": np.random.uniform(3000, 7000),
            "logg": np.random.uniform(3.5, 5.0),
            "metallicity": np.random.uniform(-0.5, 0.5)
        }
        
        return pd.DataFrame([features])
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Failed to fetch feature data: {str(e)}")

async def process_manual_features(features: Dict[str, float]) -> pd.DataFrame:
    """Process manually entered features for ML models"""
    try:
        # Expected feature names for traditional ML models
        required_features = ["period", "impact", "duration", "depth", "temp", "logg", "metallicity"]
        
        # Check if all required features are present
        missing_features = [f for f in required_features if f not in features]
        if missing_features:
            raise ValueError(f"Missing required features: {missing_features}")
        
        # Create DataFrame with features
        df = pd.DataFrame([features])
        return df
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid feature data: {str(e)}")

async def check_kepid_exists(kepid: str) -> bool:
    """Check if a Kepler ID exists in the dataset"""
    file_path = os.path.join(LIGHTKURVE_DATA_DIR, f"kepler_{kepid}_lightkurve.csv")
    return os.path.exists(file_path)

async def get_ground_truth(kepid: str) -> str:
    """Get ground truth label for a Kepler ID if available"""
    try:
        if os.path.exists(TEST_METADATA_PATH):
            metadata = pd.read_csv(TEST_METADATA_PATH)
            row = metadata[metadata['kepid'] == int(kepid)]
            if not row.empty:
                return row.iloc[0]['koi_disposition']
        return None
    except Exception:
        return None