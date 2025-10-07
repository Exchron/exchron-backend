import pandas as pd
import numpy as np
from fastapi import HTTPException
from typing import Dict, Any, Tuple
import os
from scipy import stats
from .feature_normalizer import get_feature_normalizer

# Data paths
DATA_DIR = "data"
LIGHTKURVE_DATA_DIR = os.path.join(DATA_DIR, "lightkurve_data")
TEST_METADATA_PATH = os.path.join(DATA_DIR, "lightkurve_test_metadata.csv")
KOI_TEST_DATA_PATH = "KOI-Playground-Test-Data.csv"

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
        
        # Convert to numpy array
        features_array = np.array(features).reshape(1, -1)
        
        # Apply proper feature normalization using the trained model's statistics
        normalizer = get_feature_normalizer()
        features_normalized = normalizer.normalize(features_array)
        
        return features_normalized
        
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Failed to extract features: {str(e)}")

async def get_feature_data_from_kepid(kepid: str) -> pd.DataFrame:
    """Fetch KOI feature data for a given Kepler ID from test data (for ML models)"""
    try:
        if not os.path.exists(KOI_TEST_DATA_PATH):
            raise FileNotFoundError(f"KOI test data file not found at {KOI_TEST_DATA_PATH}")
        
        # Load KOI test data
        koi_data = pd.read_csv(KOI_TEST_DATA_PATH)
        
        # Find the row for the given kepid
        target_row = koi_data[koi_data['kepid'] == int(kepid)]
        
        if target_row.empty:
            raise ValueError(f"Kepler ID {kepid} not found in KOI test data")
        
        # Extract the KOI features as specified
        features = {
            "koi_period": target_row.iloc[0]['koi_period'],
            "koi_time0bk": target_row.iloc[0]['koi_time0bk'],
            "koi_impact": target_row.iloc[0]['koi_impact'],
            "koi_duration": target_row.iloc[0]['koi_duration'],
            "koi_depth": target_row.iloc[0]['koi_depth'],
            "koi_incl": target_row.iloc[0]['koi_incl'],
            "koi_model_snr": target_row.iloc[0]['koi_model_snr'],
            "koi_count": target_row.iloc[0]['koi_count'],
            "koi_bin_oedp_sig": target_row.iloc[0]['koi_bin_oedp_sig'],
            "koi_steff": target_row.iloc[0]['koi_steff'],
            "koi_slogg": target_row.iloc[0]['koi_slogg'],
            "koi_srad": target_row.iloc[0]['koi_srad'],
            "koi_smass": target_row.iloc[0]['koi_smass'],
            "koi_kepmag": target_row.iloc[0]['koi_kepmag']
        }
        
        # Handle NaN values by filling with 0 (you may want to use different imputation strategy)
        for key, value in features.items():
            if pd.isna(value):
                features[key] = 0.0
        
        return pd.DataFrame([features])
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Failed to fetch KOI feature data: {str(e)}")

async def process_manual_features(features: Dict[str, float]) -> pd.DataFrame:
    """Process manually entered KOI features for ML models"""
    try:
        # Expected KOI feature names
        expected_features = [
            "koi_period", "koi_time0bk", "koi_impact", "koi_duration", "koi_depth",
            "koi_incl", "koi_model_snr", "koi_count", "koi_bin_oedp_sig",
            "koi_steff", "koi_slogg", "koi_srad", "koi_smass", "koi_kepmag"
        ]
        
        # Check if all expected features are present
        missing_features = [f for f in expected_features if f not in features]
        if missing_features:
            raise ValueError(f"Missing required KOI features: {missing_features}")
        
        # Create DataFrame with features in the correct order
        df_features = {feature: features[feature] for feature in expected_features}
        df = pd.DataFrame([df_features])
        return df
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid KOI feature data: {str(e)}")

async def check_kepid_exists(kepid: str) -> bool:
    """Check if a Kepler ID exists in the dataset"""
    file_path = os.path.join(LIGHTKURVE_DATA_DIR, f"kepler_{kepid}_lightkurve.csv")
    return os.path.exists(file_path)

async def check_kepid_exists_in_koi_data(kepid: str) -> bool:
    """Check if a Kepler ID exists in the KOI test data"""
    try:
        if not os.path.exists(KOI_TEST_DATA_PATH):
            return False
        
        koi_data = pd.read_csv(KOI_TEST_DATA_PATH)
        return int(kepid) in koi_data['kepid'].values
    except Exception:
        return False

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

async def get_first_ten_koi_records(data_type: str = "kepler") -> pd.DataFrame:
    """Get the first 10 records from KOI-Playground-Test-Data.csv"""
    try:
        koi_data_path = os.path.join(DATA_DIR, "KOI-Playground-Test-Data.csv")
        
        if not os.path.exists(koi_data_path):
            raise FileNotFoundError(f"KOI data file not found at {koi_data_path}")
        
        # Load KOI data
        koi_data = pd.read_csv(koi_data_path)
        
        # Get first 10 records
        first_ten = koi_data.head(10)
        
        # Extract the KOI features for each record
        feature_columns = [
            "koi_period", "koi_time0bk", "koi_impact", "koi_duration", "koi_depth",
            "koi_incl", "koi_model_snr", "koi_count", "koi_bin_oedp_sig",
            "koi_steff", "koi_slogg", "koi_srad", "koi_smass", "koi_kepmag"
        ]
        
        # Create a list to store processed records
        processed_records = []
        
        for _, row in first_ten.iterrows():
            record = {
                "kepid": str(row['kepid']),
                "features": {}
            }
            
            # Extract features and handle NaN values
            for feature in feature_columns:
                if feature in row and pd.notna(row[feature]):
                    record["features"][feature] = float(row[feature])
                else:
                    record["features"][feature] = 0.0
            
            processed_records.append(record)
        
        return processed_records
        
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Failed to fetch KOI records: {str(e)}")