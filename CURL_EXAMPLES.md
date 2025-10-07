# Example CURL Commands for New API Format

## Test the new pre-loaded format with GB model and Kepler data:

```bash
curl -X POST "http://localhost:8000/api/ml/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "model": "gb",
       "datasource": "pre-loaded",
       "data": "kepler",
       "predict": true
     }'
```

## Test with SVM model and TESS data:

```bash
curl -X POST "http://localhost:8000/api/ml/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "model": "svm", 
       "datasource": "pre-loaded",
       "data": "tess",
       "predict": true
     }'
```

## Windows PowerShell equivalent:

```powershell
$body = @{
    model = "gb"
    datasource = "pre-loaded" 
    data = "kepler"
    predict = $true
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/ml/predict" -Method POST -Body $body -ContentType "application/json"
```

## Expected Response Format:

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
  ...
  "tenth": {
    "kepid": "6531143",
    "candidate_probability": 0.3172,
    "non_candidate_probability": 0.6828
  }
}
```