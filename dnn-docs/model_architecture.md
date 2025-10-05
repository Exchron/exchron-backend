# Exoplanet Classification Model Architecture

## Overview
This document provides a comprehensive description of the dual-input deep neural network architecture designed for exoplanet candidate classification.

**Generated on:** 2025-10-05 08:25:36

## Model Summary

- **Model Type:** Dual-Input Deep Neural Network (DNN)
- **Architecture:** Combined LSTM and Dense layers for time series and tabular data
- **Total Parameters:** 3,151,905
- **Trainable Parameters:** 3,150,817
- **Non-trainable Parameters:** 1,088
- **Final Test Accuracy:** 0.9560
- **AUC Score:** 0.9959

## Architecture Details

### Input Specifications

#### 1. Time Series Input (Light Curves)
- **Shape:** `(3000, 1)`
- **Description:** Normalized light curve data representing flux measurements over time
- **Preprocessing:** 
  - Sequence padding/truncation to fixed length
  - Normalization using StandardScaler
  - Missing value handling

#### 2. Engineered Features Input
- **Shape:** `(12,)`
- **Features:** 12 engineered statistical features
- **Description:** Hand-crafted features extracted from light curves including:
  - Statistical moments (mean, std, skewness, kurtosis)
  - Frequency domain features
  - Transit-specific features
  - Variability metrics

### Network Architecture

### Layer Details

#### Layer 1: time_series_input (InputLayer)
- **Type:** InputLayer
- **Output Shape:** Variable
- **Parameters:** 0

#### Layer 2: reshape (Reshape)
- **Type:** Reshape
- **Output Shape:** Variable
- **Parameters:** 0

#### Layer 3: conv1d (Conv1D)
- **Type:** Conv1D
- **Output Shape:** Variable
- **Parameters:** 256
- **Activation:** relu

#### Layer 4: batch_normalization (BatchNormalization)
- **Type:** BatchNormalization
- **Output Shape:** Variable
- **Parameters:** 128

#### Layer 5: max_pooling1d (MaxPooling1D)
- **Type:** MaxPooling1D
- **Output Shape:** Variable
- **Parameters:** 0

#### Layer 6: dropout (Dropout)
- **Type:** Dropout
- **Output Shape:** Variable
- **Parameters:** 0
- **Dropout Rate:** 0.25

#### Layer 7: conv1d_1 (Conv1D)
- **Type:** Conv1D
- **Output Shape:** Variable
- **Parameters:** 10,304
- **Activation:** relu

#### Layer 8: batch_normalization_1 (BatchNormalization)
- **Type:** BatchNormalization
- **Output Shape:** Variable
- **Parameters:** 256

#### Layer 9: max_pooling1d_1 (MaxPooling1D)
- **Type:** MaxPooling1D
- **Output Shape:** Variable
- **Parameters:** 0

#### Layer 10: dropout_1 (Dropout)
- **Type:** Dropout
- **Output Shape:** Variable
- **Parameters:** 0
- **Dropout Rate:** 0.3

#### Layer 11: conv1d_2 (Conv1D)
- **Type:** Conv1D
- **Output Shape:** Variable
- **Parameters:** 24,704
- **Activation:** relu

#### Layer 12: batch_normalization_2 (BatchNormalization)
- **Type:** BatchNormalization
- **Output Shape:** Variable
- **Parameters:** 512

#### Layer 13: feature_input (InputLayer)
- **Type:** InputLayer
- **Output Shape:** Variable
- **Parameters:** 0

#### Layer 14: max_pooling1d_2 (MaxPooling1D)
- **Type:** MaxPooling1D
- **Output Shape:** Variable
- **Parameters:** 0

#### Layer 15: dense_2 (Dense)
- **Type:** Dense
- **Output Shape:** Variable
- **Parameters:** 832
- **Units:** 64
- **Activation:** relu

#### Layer 16: dropout_2 (Dropout)
- **Type:** Dropout
- **Output Shape:** Variable
- **Parameters:** 0
- **Dropout Rate:** 0.4

#### Layer 17: batch_normalization_3 (BatchNormalization)
- **Type:** BatchNormalization
- **Output Shape:** Variable
- **Parameters:** 256

#### Layer 18: flatten (Flatten)
- **Type:** Flatten
- **Output Shape:** Variable
- **Parameters:** 0

#### Layer 19: dropout_4 (Dropout)
- **Type:** Dropout
- **Output Shape:** Variable
- **Parameters:** 0
- **Dropout Rate:** 0.3

#### Layer 20: dense (Dense)
- **Type:** Dense
- **Output Shape:** Variable
- **Parameters:** 3,047,680
- **Units:** 256
- **Activation:** relu

#### Layer 21: dense_3 (Dense)
- **Type:** Dense
- **Output Shape:** Variable
- **Parameters:** 2,080
- **Units:** 32
- **Activation:** relu

#### Layer 22: dropout_3 (Dropout)
- **Type:** Dropout
- **Output Shape:** Variable
- **Parameters:** 0
- **Dropout Rate:** 0.5

#### Layer 23: batch_normalization_4 (BatchNormalization)
- **Type:** BatchNormalization
- **Output Shape:** Variable
- **Parameters:** 128

#### Layer 24: dense_1 (Dense)
- **Type:** Dense
- **Output Shape:** Variable
- **Parameters:** 32,896
- **Units:** 128
- **Activation:** relu

#### Layer 25: dropout_5 (Dropout)
- **Type:** Dropout
- **Output Shape:** Variable
- **Parameters:** 0
- **Dropout Rate:** 0.3

#### Layer 26: concatenate (Concatenate)
- **Type:** Concatenate
- **Output Shape:** Variable
- **Parameters:** 0

#### Layer 27: dense_4 (Dense)
- **Type:** Dense
- **Output Shape:** Variable
- **Parameters:** 20,608
- **Units:** 128
- **Activation:** relu

#### Layer 28: batch_normalization_5 (BatchNormalization)
- **Type:** BatchNormalization
- **Output Shape:** Variable
- **Parameters:** 512

#### Layer 29: dropout_6 (Dropout)
- **Type:** Dropout
- **Output Shape:** Variable
- **Parameters:** 0
- **Dropout Rate:** 0.4

#### Layer 30: dense_5 (Dense)
- **Type:** Dense
- **Output Shape:** Variable
- **Parameters:** 8,256
- **Units:** 64
- **Activation:** relu

#### Layer 31: batch_normalization_6 (BatchNormalization)
- **Type:** BatchNormalization
- **Output Shape:** Variable
- **Parameters:** 256

#### Layer 32: dropout_7 (Dropout)
- **Type:** Dropout
- **Output Shape:** Variable
- **Parameters:** 0
- **Dropout Rate:** 0.4

#### Layer 33: dense_6 (Dense)
- **Type:** Dense
- **Output Shape:** Variable
- **Parameters:** 2,080
- **Units:** 32
- **Activation:** relu

#### Layer 34: batch_normalization_7 (BatchNormalization)
- **Type:** BatchNormalization
- **Output Shape:** Variable
- **Parameters:** 128

#### Layer 35: dropout_8 (Dropout)
- **Type:** Dropout
- **Output Shape:** Variable
- **Parameters:** 0
- **Dropout Rate:** 0.4

#### Layer 36: output (Dense)
- **Type:** Dense
- **Output Shape:** Variable
- **Parameters:** 33
- **Units:** 1
- **Activation:** sigmoid


### Training Configuration

- **Time Series Length:** 3000
- **Batch Size:** 32
- **Learning Rate:** 0.001
- **Max Epochs:** 100
- **Early Stopping Patience:** 15
- **Validation Split:** 0.2
- **Test Split:** 0.15

### Model Compilation

- **Optimizer:** Adam
- **Loss Function:** binary_crossentropy
- **Metrics:** <Mean name=loss>, <CompileMetrics name=compile_metrics>

### Performance Metrics

| Metric | Value |
|--------|--------|
| Test Accuracy | 0.9560 |
| Test Precision | 0.9213 |
| Test Recall | 0.9880 |
| AUC Score | 0.9959 |

## Model Architecture Rationale

### Dual-Input Design
The model employs a dual-input architecture to leverage both temporal patterns in light curves and statistical features:

1. **LSTM Branch:** Processes sequential light curve data to capture temporal dependencies and transit patterns
2. **Dense Branch:** Processes engineered features to capture statistical properties and domain-specific characteristics
3. **Fusion Layer:** Combines both representations for final classification

### Key Design Decisions

1. **LSTM for Time Series:** Captures long-term dependencies in light curve data, essential for detecting periodic transit signals
2. **Feature Engineering:** Incorporates domain knowledge through hand-crafted features that complement learned representations
3. **Dropout Regularization:** Prevents overfitting in the high-dimensional feature space
4. **Binary Classification:** Optimized for distinguishing between exoplanet candidates and false positives

## Data Pipeline

### Preprocessing Steps
1. Light curve normalization and cleaning
2. Sequence padding/truncation to fixed length
3. Feature engineering from raw time series
4. Train/validation/test splitting with stratification
5. Feature scaling using StandardScaler

### Augmentation Techniques
- Temporal shifts and scaling (if implemented)
- Noise injection for robustness
- Class balancing strategies

## Model Files

- **Keras Format:** `models/dual_input_dnn_model.keras` (Recommended)
- **H5 Format:** `models/dual_input_dnn_model.h5` (Compatibility)
- **Architecture Summary:** `models/model_architecture_summary.txt`
- **Training Logs:** `logs/training_history.png`

## Usage Instructions

```python
import tensorflow as tf

# Load the model
model = tf.keras.models.load_model('models/dual_input_dnn_model.keras')

# Make predictions
predictions = model.predict([time_series_data, engineered_features])
```

## References

- Kepler Space Telescope Data
- NASA Exoplanet Archive
- TensorFlow/Keras Documentation

---
*This documentation was automatically generated by the Exoplanet Classification Training Pipeline.*
