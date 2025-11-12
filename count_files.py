import os

DATASET = "./dataset"

for root, dirs, files in os.walk(DATASET):
    print(f"{root} → {len(files)} files")
