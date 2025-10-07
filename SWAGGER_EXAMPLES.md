# Working JSON Examples for Swagger UI

## Manual Features Request (Copy this exactly into Swagger UI):

```json
{
  "model": "gb",
  "datasource": "manual", 
  "features": {
    "koi_period": 10.00506974,
    "koi_time0bk": 136.83029,
    "koi_impact": 0.148,
    "koi_duration": 3.481,
    "koi_depth": 143.3,
    "koi_incl": 89.61,
    "koi_model_snr": 11.4,
    "koi_count": 2,
    "koi_bin_oedp_sig": 0.4606,
    "koi_steff": 5912,
    "koi_slogg": 4.453,
    "koi_srad": 0.924,
    "koi_smass": 0.884,
    "koi_kepmag": 14.634
  },
  "predict": true
}
```

## Pre-loaded Format (Copy this exactly into Swagger UI):

```json
{
  "model": "gb",
  "datasource": "pre-loaded",
  "data": "kepler",
  "predict": true
}
```

## SVM Pre-loaded Format:

```json
{
  "model": "svm",
  "datasource": "pre-loaded",
  "data": "kepler", 
  "predict": true
}
```

## Test with TESS data:

```json
{
  "model": "gb",
  "datasource": "pre-loaded",
  "data": "tess",
  "predict": true
}
```