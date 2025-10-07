"""
URL generation service for NASA Exoplanet Archive links
Generates proper DV report URLs with correct directory structure and timestamps
"""

import pandas as pd
import os
from typing import Optional


def generate_dv_report_url(kepid: str) -> str:
    """
    Generate the correct DV report URL for a given Kepler ID.
    
    The URL format follows NASA's structure:
    http://exoplanetarchive.ipac.caltech.edu:8000/data/KeplerData/XXX/XXXXXX/XXXXXXXXX/dv/kplrXXXXXXXXX-TIMESTAMP_dvr.pdf
    
    Args:
        kepid: The Kepler ID as a string
        
    Returns:
        The complete DV report URL
    """
    
    # First, try to get the exact URL from the CSV data
    csv_url = get_dv_url_from_csv(kepid)
    if csv_url:
        base_url = "http://exoplanetarchive.ipac.caltech.edu:8000/data/KeplerData"
        return f"{base_url}/{csv_url}"
    
    # Fallback: generate URL using the standard format
    # For Kepler IDs, the directory structure is based on zero-padded segments
    kepid_padded = kepid.zfill(9)  # Ensure 9 digits with leading zeros
    
    # Create directory structure: first 3 digits / next 3 digits / full kepid
    dir1 = kepid_padded[:3]
    dir2 = kepid_padded[3:6] 
    dir3 = kepid_padded
    
    # Use a default timestamp (this is a fallback when exact data isn't available)
    default_timestamp = "20160209194854"
    
    url = f"http://exoplanetarchive.ipac.caltech.edu:8000/data/KeplerData/{dir1}/{dir2}/{dir3}/dv/kplr{kepid_padded}-{default_timestamp}_dvr.pdf"
    
    return url


def get_dv_url_from_csv(kepid: str) -> Optional[str]:
    """
    Get the exact DV report path from the CSV data file.
    
    Args:
        kepid: The Kepler ID as a string
        
    Returns:
        The DV report path from the CSV, or None if not found
    """
    try:
        csv_path = "data/slected-2000-dnn-cnn.csv"
        
        if not os.path.exists(csv_path):
            return None
            
        # Read the CSV file, skipping header comments
        df = pd.read_csv(csv_path, comment='#')
        
        # Convert kepid to integer for comparison
        kepid_int = int(kepid)
        
        # Find the row with matching kepid
        matching_rows = df[df['kepid'] == kepid_int]
        
        if not matching_rows.empty:
            # Get the DV report path from koi_datalink_dvr column
            dv_path = matching_rows.iloc[0]['koi_datalink_dvr']
            return dv_path
            
    except Exception as e:
        # If there's any error reading the CSV, return None to use fallback
        print(f"Warning: Could not read DV URL from CSV for kepid {kepid}: {e}")
        return None
    
    return None


def generate_lightcurve_url(kepid: str) -> str:
    """
    Generate the STScI archive lightcurve directory URL for a given Kepler ID.
    
    Format: http://archive.stsci.edu/pub/kepler/lightcurves/XXXX/KKKKKKKKK
    where XXXX is the first 4 digits of the KIC ID (with leading zeros)
    and KKKKKKKKK is the full 9-digit zero-padded KIC ID
    
    Args:
        kepid: The Kepler ID as a string
        
    Returns:
        The complete STScI lightcurve directory URL
    """
    # Ensure kepid is zero-padded to 9 digits
    kepid_padded = kepid.zfill(9)
    
    # Get first 4 digits for directory structure
    first_four = kepid_padded[:4]
    
    return f"http://archive.stsci.edu/pub/kepler/lightcurves/{first_four}/{kepid_padded}/"


def generate_target_pixel_file_url(kepid: str) -> str:
    """
    Generate the STScI archive target pixel files directory URL for a given Kepler ID.
    
    Format: http://archive.stsci.edu/pub/kepler/target_pixel_files/XXXX/KKKKKKKKK
    where XXXX is the first 4 digits of the KIC ID (with leading zeros)
    and KKKKKKKKK is the full 9-digit zero-padded KIC ID
    
    Args:
        kepid: The Kepler ID as a string
        
    Returns:
        The complete STScI target pixel files directory URL
    """
    # Ensure kepid is zero-padded to 9 digits
    kepid_padded = kepid.zfill(9)
    
    # Get first 4 digits for directory structure
    first_four = kepid_padded[:4]
    
    return f"http://archive.stsci.edu/pub/kepler/target_pixel_files/{first_four}/{kepid_padded}/"


def get_archive_links(kepid: str) -> dict:
    """
    Get DV report, lightcurve, and target pixel file URLs for a given Kepler ID.
    
    Args:
        kepid: The Kepler ID as a string
        
    Returns:
        Dictionary containing all archive URLs
    """
    return {
        "dv_report_link": generate_dv_report_url(kepid),
        "lightcurve_link": generate_lightcurve_url(kepid),
        "target_pixel_file_link": generate_target_pixel_file_url(kepid)
    }