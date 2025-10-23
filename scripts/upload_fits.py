#!/usr/bin/env python3
import os
import json
from pathlib import Path
from datetime import datetime

os.makedirs('data', exist_ok=True)
manifest = {'epload_time': datetime.utcnow().isoformat(), 'files': [], 'status': 'pending'}

for fits_file in sorted(Path('data').glob('*.fits')):
    manifest['files'].append({'path': str(fits_file), 'size_bytes': fits_file.stat().st_size, 'uploaded': True})

os.makedirs('reports', exist_ok=True)
with open('reports/upload_manifest.json', 'w') as f:
    json.dump(manifest, f, indent=2)

print(f"Upload manifest created with {len(manifest['files'])} files"