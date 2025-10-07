"""
Create Swagger-friendly test data with proper JSON formatting
"""

import json

# Test data that should work in Swagger UI
swagger_test_manual = {
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
    "predict": True
}

swagger_test_preloaded = {
    "model": "gb",
    "datasource": "pre-loaded",
    "data": "kepler",
    "predict": True
}

print("=== SWAGGER UI COMPATIBLE JSON ===")
print("\n1. Manual Features Request:")
print(json.dumps(swagger_test_manual, indent=2))

print("\n2. Pre-loaded Request:")
print(json.dumps(swagger_test_preloaded, indent=2))

print("\n=== COPY THESE EXACTLY INTO SWAGGER UI ===")
print("\nManual (compact):")
print(json.dumps(swagger_test_manual))

print("\nPre-loaded (compact):")
print(json.dumps(swagger_test_preloaded))