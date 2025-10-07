# 🔧 Swagger UI Troubleshooting Guide

## ✅ **The Problem**
The Swagger UI at `http://localhost:8000/docs` is giving a 422 "JSON decode error" when trying to test the API, even though the same requests work perfectly in Python scripts.

## ✅ **The Solution**

### **Use These Exact JSON Examples in Swagger UI:**

#### **1. Manual Features Request:**
Copy this EXACTLY into the Swagger UI request body:

```json
{
  "model": "gb",
  "datasource": "manual",
  "features": {
    "koi_period": 10.005,
    "koi_time0bk": 136.83,
    "koi_impact": 0.148,
    "koi_duration": 3.481,
    "koi_depth": 143.3,
    "koi_incl": 89.61,
    "koi_model_snr": 11.4,
    "koi_count": 2,
    "koi_bin_oedp_sig": 0.461,
    "koi_steff": 5912.0,
    "koi_slogg": 4.453,
    "koi_srad": 0.924,
    "koi_smass": 0.884,
    "koi_kepmag": 14.634
  },
  "predict": true
}
```

#### **2. Pre-loaded Request (NEW FORMAT):**
Copy this EXACTLY into the Swagger UI request body:

```json
{
  "model": "gb",
  "datasource": "pre-loaded",
  "data": "kepler",
  "predict": true
}
```

#### **3. SVM Pre-loaded Request:**
```json
{
  "model": "svm",
  "datasource": "pre-loaded", 
  "data": "kepler",
  "predict": true
}
```

## ⚠️ **Common Swagger UI Issues**

### **1. Boolean Values**
- ❌ Wrong: `"predict": True` (Python format)
- ✅ Correct: `"predict": true` (JSON format)

### **2. Number Precision**
- ❌ Problematic: Very long decimal numbers
- ✅ Better: Round to reasonable precision (e.g., 10.00506974 → 10.005)

### **3. Trailing Commas**
- ❌ Wrong: `"predict": true,}` (trailing comma)
- ✅ Correct: `"predict": true}` (no trailing comma)

### **4. Copy-Paste Issues**
- Make sure you're copying the entire JSON block
- Check for any hidden characters or formatting issues
- Try typing the JSON manually if copy-paste doesn't work

## 🧪 **Testing Steps**

1. **Go to:** `http://localhost:8000/docs`
2. **Find:** `POST /api/ml/predict` endpoint
3. **Click:** "Try it out" button
4. **Clear** the existing JSON in the request body
5. **Copy-paste** one of the exact examples above
6. **Click:** "Execute"
7. **Expect:** 200 response with prediction results

## ✅ **Expected Responses**

### **Manual Features Response:**
```json
{
  "candidate_probability": 0.7922,
  "non_candidate_probability": 0.2078
}
```

### **Pre-loaded Response:**
```json
{
  "candidate_probability": 0.4270,
  "non_candidate_probability": 0.5730,
  "first": {
    "kepid": "7537660",
    "candidate_probability": 0.0357,
    "non_candidate_probability": 0.9643
  },
  "second": {
    "kepid": "3219037",
    "candidate_probability": 0.9254,
    "non_candidate_probability": 0.0746
  },
  ... (continues through "tenth")
}
```

## 🐛 **Still Having Issues?**

If Swagger UI still doesn't work, you can:

1. **Use curl instead:**
```bash
curl -X POST "http://localhost:8000/api/ml/predict" \
     -H "Content-Type: application/json" \
     -d '{"model": "gb", "datasource": "pre-loaded", "data": "kepler", "predict": true}'
```

2. **Use the Python test script:** `simple_test.py`

3. **Check the server logs** for any error messages

4. **Try refreshing** the Swagger UI page (Ctrl+F5)

The API is working correctly - this is just a Swagger UI JSON formatting issue!