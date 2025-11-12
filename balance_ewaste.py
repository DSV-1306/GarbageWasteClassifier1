import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img

E_WASTE_FOLDER = "./dataset/train/e-waste"
TARGET_COUNT = 10000  # generate until we reach ~10k images

datagen = ImageDataGenerator(
    rotation_range=25,
    width_shift_range=0.2,
    height_shift_range=0.2,
    zoom_range=0.2,
    shear_range=0.15,
    horizontal_flip=True,
)

existing_files = os.listdir(E_WASTE_FOLDER)
count = len(existing_files)

print(f"Existing e-waste images: {count}")

i = 0
while count < TARGET_COUNT:
    img_path = os.path.join(E_WASTE_FOLDER, existing_files[i % len(existing_files)])
    img = load_img(img_path, target_size=(128, 128))
    x = img_to_array(img)
    x = x.reshape((1,) + x.shape)

    for _ in datagen.flow(x, batch_size=1, save_to_dir=E_WASTE_FOLDER, save_format="jpg"):
        count += 1
        if count % 500 == 0:
            print(f"Generated: {count} images...")

        if count >= TARGET_COUNT:
            break

print("\n✅ E-waste dataset balanced!")
print(f"Final image count: {count}")
