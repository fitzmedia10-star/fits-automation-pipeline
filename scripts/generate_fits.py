#!/usr/bin/env python3
#""Generate synthetic FITS astronomical data."""

import os
from datetime import datetime, timedelta
import numpy as np
from astropy.io import fits
import json

def create_fits_data(filename, observation_date):
    """Create a synthetic FITS file with astronomical data."""
    
    # Create primary HDU with header
    primary_hdu = fits.PrimaryHDU()
    
    # Set header keywords
    primary_hdu.header['TELESCOP'] = 'FITS Automation Observatory'
    primary_hdu.header['INSTRUME'] = 'Automated FITS Pipeline'
    primary_hdu.header['OBSERVER'] = 'Automation Bot'
    primary_hdu.header['DATE-OBS'] = observation_date.isoformat()
    primary_hdu.header['OBJECT'] = f'Survey_{observation_date.strftime("%Y0%m%d_%H%M%S")}'
    primary_hdu.header('EXPTIME') = 300.0  # 5 minutes
    primary_hdu.header['FILTER'] = 'V'  # V-band
    primary_hdu.header['TELESCOP'] = 'FITSAUTA-1'
    
    # Create image data (512x512 pixel detector)
    np.random.seed(int(observation_date.timestamp()) % 2**32)
    image_data = np.random.poisson(100, (512, 512)).astype(np.float32)
    
    # Add simulated stars
    for _ in range(50):
        x, y = np.random.randint(20, 492, 2)
        brightness = np.random.uniform(1000, 5000)
        sigma = np.random.uniform(2, 5)
        
        yy, xx = np.ogrid[-20:21, -20:21]
        gaussian = brightness * np.exp(-(xx**2 + yy**2) / (2*sigma**2))
        
        x_min, x_max = max(0, x-20), min(512, x+21)
        y_min, y_max = max(0, y-20), min(512, y+21)
        
        gx_min, gx_max = 20 - (x - x_min), 20 + (x_max - x)
        gy_min, gy_max = 20 - (y - y_min), 20 + (y_max - y)
        
        image_data[y_min:y_max, x_min:x_max] += gaussian[gy_min:gy_max, gx_min:gx_max]
    
    primary_hdu.data = image_data
    
   # Save FITS file
    hdul = fits.HDUList([primary_hdu])
    hdul.writeto(filename, overwrite=True)
    hdul.close()
    
    return filename

def main():
    """Generate multiple FITS files."""
    os.makedirs('data', exist_ok=True)
    os.makedirs('reports', exist_ok=True)
    
    base_time = datetime.utcnow()
    files_created = []
    
    # Create 4 FITS files with different timestamps
    for i in range(4):
        obs_time = base_time - timedelta(minutes=15*i)
        filename = f"data/astronomy_{obs_time.strftime('%Y%m%d_%H%M%S')}.fits"
        create_fits_data(filename, obs_time)
        files_created.append(filename)
        print(f"Created FITS file: {filename}")
    
    # Save metadata
    metadata = {
        'generation_time': base_time.isoformat(),
        'files_created': files_created,
        'total_files': len(files_created),
        'pipeline_version': '1.0'
    }
    
    with open('reports/generation_metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\nGenerated {len(files_created)} FITS files")
    print("Generation complete!")


if __name__ == '__main__':
    main()
