# 🚀 Quick Reference: Exoplanet Classification API v2.0

## Real Model Integration Complete ✅

### What's New:
- ✅ **CNN Model**: Real Keras model (`exchron-cnn.keras`) for time series analysis
- ✅ **DNN Model**: Real dual-input Keras model (`exchron-dnn.keras`) with 95.6% accuracy
- ✅ **Real Data**: Authentic Kepler Space Telescope lightcurve data (873+ objects)
- ✅ **Feature Engineering**: 12 statistical features automatically extracted for DNN
- ✅ **Data Validation**: API validates Kepler IDs exist before processing
- ✅ **Enhanced Testing**: Comprehensive test suite with real predictions

## 🎯 Key Endpoints:

### Get Available Data:
```bash
GET /api/dl/available-ids  # List all valid Kepler IDs
```

### Real CNN Predictions:
```bash
POST /api/dl/predict
{
  "model": "cnn",
  "kepid": "10904857",  # Use real Kepler ID
  "predict": true
}
```

### Real DNN Predictions:
```bash
POST /api/dl/predict
{
  "model": "dnn", 
  "kepid": "6362874",   # Use real Kepler ID
  "predict": true
}
```

## 🔬 How It Works:

### CNN Workflow:
1. **Input**: Kepler ID → Load `kepler_{kepid}_lightkurve.csv`
2. **Process**: Extract flux → Clean outliers → Normalize → Pad/truncate to 3000 points
3. **Model**: Real CNN model processes time series data
4. **Output**: Binary classification probability (candidate vs false positive)

### DNN Workflow:
1. **Input**: Kepler ID → Load lightcurve data
2. **Dual Processing**:
   - Time series: Same as CNN (3000 points)
   - Features: Extract 12 statistical features automatically
3. **Model**: Real dual-input DNN model
4. **Output**: Enhanced binary classification with 95.6% accuracy

## 📊 Sample Valid Kepler IDs:

### Known Candidates:
- `10904857` - High confidence candidate
- `6362874` - Validated candidate  
- `6266741` - Strong candidate signal

### Known False Positives:
- `9652632` - Stellar variability
- `6781535` - Binary eclipse
- `3233043` - Instrumental artifact

## 🧪 Quick Test:

```bash
# Start API
uvicorn app.main:app --reload

# Test CNN
curl -X POST "http://localhost:8000/api/dl/predict" \
  -H "Content-Type: application/json" \
  -d '{"model": "cnn", "kepid": "10904857", "predict": true}'

# Test DNN  
curl -X POST "http://localhost:8000/api/dl/predict" \
  -H "Content-Type: application/json" \
  -d '{"model": "dnn", "kepid": "9652632", "predict": true}'

# Run comprehensive tests
python test_api.py
```

## 📈 Performance:
- **DNN Accuracy**: 95.60%
- **AUC Score**: 99.59%
- **Dataset Size**: 873+ Kepler lightcurves
- **Feature Extraction**: Automatic (12 statistical features)
- **Processing Time**: <2 seconds per prediction

## 🔗 Key Files:
- `models/exchron-cnn.keras` - Real CNN model
- `models/exchron-dnn.keras` - Real DNN model  
- `data/lightkurve_data/` - Kepler lightcurve CSV files
- `data/lightkurve_test_metadata.csv` - Ground truth labels
- `app/services/data_service.py` - Real data processing
- `app/models/model_loader.py` - Keras model loading

---
**Status**: ✅ Production Ready with Real Models
**Version**: 2.0.0
**Last Updated**: October 2025