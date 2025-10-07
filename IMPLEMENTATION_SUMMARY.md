# Archive URL Implementation Summary

## What Was Implemented

### 1. DV Report URLs (NASA Exoplanet Archive)
- **Format**: `http://exoplanetarchive.ipac.caltech.edu:8000/data/KeplerData/XXX/XXXXXX/XXXXXXXXX/dv/kplrXXXXXXXXX-TIMESTAMP_dvr.pdf`
- **Source**: CSV data file with exact paths and timestamps
- **Fallback**: Generated URLs using standard directory structure
- **Example**: `http://exoplanetarchive.ipac.caltech.edu:8000/data/KeplerData/003/003247/003247268/dv/kplr003247268-20160209194854_dvr.pdf`

### 2. STScI Lightcurve URLs
- **Format**: `http://archive.stsci.edu/pub/kepler/lightcurves/XXXX/KKKKKKKKK/`
- **Structure**: First 4 digits / Full 9-digit zero-padded ID
- **Example**: `http://archive.stsci.edu/pub/kepler/lightcurves/0014/001429092/`

### 3. STScI Target Pixel File URLs
- **Format**: `http://archive.stsci.edu/pub/kepler/target_pixel_files/XXXX/KKKKKKKKK/`
- **Structure**: First 4 digits / Full 9-digit zero-padded ID  
- **Example**: `http://archive.stsci.edu/pub/kepler/target_pixel_files/0014/001429092/`

## Files Created/Modified

### New Files:
1. `app/services/url_service.py` - URL generation service
2. `test_url_generation.py` - Test script for URL generation
3. `test_archive_urls.py` - API integration test
4. `quick_test.py` - Simple API test

### Modified Files:
1. `app/services/prediction_service.py` - Updated to use new URL service
2. `app/schemas/responses.py` - Added target_pixel_file_link field
3. `README.md` - Updated documentation with new URL formats

## Key Features

### 1. CSV Data Integration
- Reads exact DV report paths from `data/slected-2000-dnn-cnn.csv`
- Uses real timestamps and directory structures from NASA
- Falls back to generated URLs if data not found in CSV

### 2. Proper URL Format Generation
- Zero-pads Kepler IDs to 9 digits (e.g., 1429092 → 001429092)
- Creates correct directory structure (e.g., 0014/001429092/)
- Follows official STScI and NASA archive conventions

### 3. API Integration
- All deep learning model predictions now return 3 archive links:
  - DV Report (NASA Exoplanet Archive)
  - Lightcurve Data (STScI)
  - Target Pixel Files (STScI)

## URL Examples

For Kepler ID `1429092`:
- **DV Report**: `http://exoplanetarchive.ipac.caltech.edu:8000/data/KeplerData/001/429/001429092/dv/kplr001429092-20160209194854_dvr.pdf`
- **Lightcurve**: `http://archive.stsci.edu/pub/kepler/lightcurves/0014/001429092/`
- **Target Pixel**: `http://archive.stsci.edu/pub/kepler/target_pixel_files/0014/001429092/`

For Kepler ID `3247268` (your example):
- **DV Report**: `http://exoplanetarchive.ipac.caltech.edu:8000/data/KeplerData/003/003247/003247268/dv/kplr003247268-20160209194854_dvr.pdf` ✓ Matches your example
- **Lightcurve**: `http://archive.stsci.edu/pub/kepler/lightcurves/0032/003247268/`
- **Target Pixel**: `http://archive.stsci.edu/pub/kepler/target_pixel_files/0032/003247268/`

## API Response Format

```json
{
    "candidate_probability": 0.7234,
    "non_candidate_probability": 0.2766,
    "lightcurve_link": "http://archive.stsci.edu/pub/kepler/lightcurves/0032/003247268/",
    "target_pixel_file_link": "http://archive.stsci.edu/pub/kepler/target_pixel_files/0032/003247268/",
    "dv_report_link": "http://exoplanetarchive.ipac.caltech.edu:8000/data/KeplerData/003/003247/003247268/dv/kplr003247268-20160209194854_dvr.pdf",
    "kepid": "3247268", 
    "model_used": "CNN"
}
```

The implementation is complete and ready for use! 🚀