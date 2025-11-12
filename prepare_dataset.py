import os
import shutil

SRC = "./dataset_original"
DST = "./dataset"

folders = ["organic", "recyclable", "e-waste"]

for c in folders:
    os.makedirs(os.path.join(DST, "train", c), exist_ok=True)
    os.makedirs(os.path.join(DST, "test", c), exist_ok=True)

def move(src, dst):
    if not os.path.exists(src):
        print(f"❌ Folder NOT found: {src}")
        return

    files = os.listdir(src)
    print(f"📂 Copying {len(files)} files → {dst}")

    for f in files:
        shutil.copy(os.path.join(src, f), dst)

# ✅ COPY ORGANIC
move(f"{SRC}/TRAIN/Organic",     f"{DST}/train/organic")
move(f"{SRC}/TEST/Organic",      f"{DST}/test/organic")

# ✅ COPY RECYCLABLE
move(f"{SRC}/TRAIN/Recyclable",  f"{DST}/train/recyclable")
move(f"{SRC}/TEST/Recyclable",   f"{DST}/test/recyclable")

# ✅ COPY E-WASTE
move(f"{SRC}/TRAIN/E-Waste",     f"{DST}/train/e-waste")
move(f"{SRC}/TEST/E-Waste",      f"{DST}/test/e-waste")

print("\n✅ COPYING COMPLETE")
