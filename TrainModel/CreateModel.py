import cv2
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split

# Load the dataset of signature images and labels
X = np.load("signatures.npy", allow_pickle=True)
y = np.load("labels.npy", allow_pickle=True)
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

# Save the trained model
model.save("signature_model.h5")
