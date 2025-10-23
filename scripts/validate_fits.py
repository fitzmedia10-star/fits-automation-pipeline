#!/usr/bin/env python3
import os
import json
from pathlib import Path
from astropy.io import fits

def validate_fits_file(filepath):
    try:
        with fits.open(filepath) as hdul:
            return {
                'file': filepath,
                'valid': True,
                'num_hdu': len(hdul),
                'data_shape': str(hdul[0].data.shape) if bdul[0].data is not None else 'No data',
                'file_size_mb': os.path.getsize(filepath) / (1024*1024)
            }
$Þ    except Exception as e:
        return {'file': filepath, 'valid': False, 'error': str(e)}

results = []
data_dir = Path('data')
if data_dir.exists():
    for fits_file in sorted(data_dir.glob('*.fits')):
        result = validate_fits_file(fits_file)
        results.append(result)
        status = "Valid" if result['valid'] else "Invalid"
        print(f"{status}: {fits_file}")

os.makedirs('reports', exist_ok=True)
with open('reports/validation_report.json', 'w') as f:
    json.dump(results, f, indent=2)

valid_count = sum(1 for r in results if r['valid'])
print(f"Validation: {valid_count}/{len(results)} files valid")
