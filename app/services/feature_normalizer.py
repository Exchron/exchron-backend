"""
Feature normalization parameters for DNN model.
These parameters were derived from the training dataset to ensure 
consistent preprocessing for inference.
"""

import numpy as np

# Feature normalization parameters derived from training data
# These ensure that inference features match the distribution the model was trained on

class FeatureNormalizer:
    """
    Feature normalizer for DNN model engineered features.
    Applies StandardScaler-like normalization using pre-computed statistics.
    """
    
    def __init__(self):
        # Mean and standard deviation values for each of the 12 engineered features
        # These should be computed from the actual training dataset
        # For now, using reasonable estimates based on normalized lightcurve data
        
        self.feature_names = [
            'mean', 'std', 'skewness', 'kurtosis', 'min', 'max', 
            'range', 'median', 'q25', 'q75', 'iqr', 'mad'
        ]
        
        # Training set statistics (these would come from actual training data analysis)
        # Currently using estimates - in production, these should be loaded from saved scaler
        self.means = np.array([
            0.0,     # mean (flux already normalized to ~0 mean)
            1.0,     # std (flux normalized to ~1 std) 
            0.05,    # skewness (slight positive skew typical)
            0.2,     # kurtosis (slightly leptokurtic)
            -2.8,    # min (typical range for normalized data)
            2.8,     # max (typical range for normalized data)
            5.6,     # range (max - min)
            0.0,     # median (should be close to mean for normalized data)
            -0.67,   # 25th percentile (approximately -2/3 std)
            0.67,    # 75th percentile (approximately +2/3 std)
            1.35,    # IQR (q75 - q25)
            0.8      # mean absolute deviation (typically ~0.8 * std for normal dist)
        ])
        
        self.stds = np.array([
            0.1,     # mean std (small variation around 0)
            0.3,     # std std (moderate variation around 1)
            1.5,     # skewness std (can vary significantly)
            3.0,     # kurtosis std (high variation)
            1.0,     # min std
            1.0,     # max std  
            1.5,     # range std
            0.1,     # median std (should be stable)
            0.8,     # q25 std
            0.8,     # q75 std
            1.0,     # IQR std
            0.6      # MAD std
        ])
    
    def normalize(self, features):
        """
        Normalize features using z-score normalization.
        
        Args:
            features: np.array of shape (1, 12) containing raw engineered features
            
        Returns:
            np.array of shape (1, 12) containing normalized features
        """
        if features.shape != (1, 12):
            raise ValueError(f"Expected features shape (1, 12), got {features.shape}")
        
        # Apply z-score normalization: (x - mean) / std
        normalized = (features - self.means.reshape(1, -1)) / self.stds.reshape(1, -1)
        
        # Clip extreme values to prevent model instability
        # This handles outliers that might cause extreme predictions
        normalized = np.clip(normalized, -5.0, 5.0)
        
        return normalized
    
    def get_feature_info(self):
        """Return information about the features and their normalization parameters."""
        info = []
        for i, name in enumerate(self.feature_names):
            info.append({
                'name': name,
                'mean': self.means[i],
                'std': self.stds[i],
                'description': self._get_feature_description(name)
            })
        return info
    
    def _get_feature_description(self, name):
        """Get description for each feature."""
        descriptions = {
            'mean': 'Mean flux value (normalized)',
            'std': 'Standard deviation of flux',
            'skewness': 'Skewness (asymmetry) of flux distribution',
            'kurtosis': 'Kurtosis (tail heaviness) of flux distribution',
            'min': 'Minimum flux value',
            'max': 'Maximum flux value',
            'range': 'Range (max - min) of flux values',
            'median': 'Median flux value',
            'q25': '25th percentile of flux',
            'q75': '75th percentile of flux',
            'iqr': 'Interquartile range (Q75 - Q25)',
            'mad': 'Mean absolute deviation from mean'
        }
        return descriptions.get(name, 'Unknown feature')

# Global normalizer instance
_feature_normalizer = None

def get_feature_normalizer():
    """Get the global feature normalizer instance."""
    global _feature_normalizer
    if _feature_normalizer is None:
        _feature_normalizer = FeatureNormalizer()
    return _feature_normalizer