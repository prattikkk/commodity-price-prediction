import kagglehub
import os

# Download latest version
path = kagglehub.dataset_download("arjunyadav99/indian-agricultural-mandi-prices-20232025")

print("Path to dataset files:", path)
print("Contents of the directory:")
for file in os.listdir(path):
    print(f"  {file}")
