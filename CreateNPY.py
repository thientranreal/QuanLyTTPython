import cv2
import numpy as np
import os

# Set the path to the dataset
dataset_path = "SignatureImg"

# Create empty lists to store the images and labels
images = []
labels = []

# Loop over the subfolders in the dataset
for label, folder in enumerate(os.listdir(dataset_path)):
    # Set the path to the subfolder
    folder_path = os.path.join(dataset_path, folder)

    # Loop over the images in the subfolder
    for filename in os.listdir(folder_path):
        # Set the path to the image
        image_path = os.path.join(folder_path, filename)

        # Load the image
        img = cv2.imread(image_path)

        # Append the image and label to the lists
        images.append(img)
        labels.append(label)

# Convert the lists to NumPy arrays
images = np.array(images)
labels = np.array(labels)

# Save the NumPy arrays to .npy files
np.save("TrainModel/signatures.npy", images)
np.save("TrainModel/labels.npy", labels)