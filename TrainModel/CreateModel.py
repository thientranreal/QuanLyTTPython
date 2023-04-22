import cv2
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split

def CreateModel():
    Xpath = "TrainModel/signatures.npy"
    X_augmentedPath = "TrainModel/signatures_augmented.npy"
    yPath = "TrainModel/labels.npy"
    y_augmentedPath = "TrainModel/labels_augmented.npy"
    modelPath = "TrainModel/signature_model.h5"
    
    # Load the dataset of signature images and labels
    X = np.load(Xpath, allow_pickle=True)
    X_augmented = np.load(X_augmentedPath, allow_pickle=True)

    # Concatenate the original and augmented images
    X = np.concatenate((X, X_augmented))

    y = np.load(yPath, allow_pickle=True)
    y_augmented = np.load(y_augmentedPath, allow_pickle=True)

    # Concatenate the original and augmented images
    y = np.concatenate((y, y_augmented))

    num_classes = len(np.unique(y))
    y = to_categorical(y, num_classes)

    X = np.array([cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) for img in X])
    X = np.array([cv2.resize(img, (200, 200)) for img in X])
    X = np.array([cv2.GaussianBlur(img, (5, 5), 0) for img in X])
    X = np.array([cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)[1] for img in X])
    X = np.array([img.flatten() for img in X])

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2)

    model = Sequential()
    model.add(Dense(128, input_dim=X.shape[1], activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=10)
    
    # Evaluate the trained model on the validation set
    loss, accuracy = model.evaluate(X_val, y_val)
    print(f'Validation accuracy: {accuracy:.2f}')

    # Save the trained model
    model.save(modelPath)