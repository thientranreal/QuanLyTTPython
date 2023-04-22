import cv2
import numpy as np
import os
import imgaug.augmenters as iaa
import numpy as np

def createNPY():
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

    # Load the dataset of signature images
    X = np.load("TrainModel/signatures.npy", allow_pickle=True)

    # Define an augmentation pipeline
    seq = iaa.Sequential([
        iaa.Affine(
            rotate=(-10, 10), # rotate by -10 to +10 degrees
            translate_percent={"x": (-0.1, 0.1), "y": (-0.1, 0.1)}, # translate by -10% to +10% on x and y axis
            scale={"x": (0.9, 1.1), "y": (0.9, 1.1)} # scale by 90% to 110% on x and y axis
        ),
        iaa.AdditiveGaussianNoise(scale=(10, 20)) # add gaussian noise with a scale of 10 to 20
    ])

    # Apply the augmentation pipeline to the images
    X_augmented = seq(images=X)

    # Concatenate the original and augmented images
    X = np.concatenate((X, X_augmented))

    np.save("TrainModel/signatures_augmented.npy", X)

    # Load the original labels
    y = np.load("TrainModel/labels.npy", allow_pickle=True)

    # Create the labels for the augmented images
    y_augmented = np.copy(y)

    # Concatenate the original and augmented labels
    y = np.concatenate((y, y_augmented))

    # Save the new labels to a .npy file
    np.save("TrainModel/labels_augmented.npy", y)