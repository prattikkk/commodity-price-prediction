import kagglehub
import os
import shutil
from pathlib import Path

# Download latest version
path = kagglehub.dataset_download("arjunyadav99/indian-agricultural-mandi-prices-20232025")

print("Path to dataset files:", path)
print("Contents of the directory:")
files = os.listdir(path)
for file in files:
    print(f"  {file}")

# Copy files to our data/raw directory
data_raw_dir = Path(__file__).parent / "data" / "raw"
data_raw_dir.mkdir(exist_ok=True)

for file in files:
    if file.endswith('.csv'):
        src = os.path.join(path, file)
        dst = data_raw_dir / f"kaggle_{file}"
        shutil.copy2(src, dst)
        print(f"Copied {file} to {dst}")

        # Read first few lines to understand structure
        with open(dst, 'r') as f:
            lines = f.readlines()[:5]
            print(f"First 5 lines of {file}:")
            for line in lines:
                print(f"  {line.strip()}")
            print()
