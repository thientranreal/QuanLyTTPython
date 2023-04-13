import cv2
import numpy as np
from keras.models import load_model

def predictSignature(path, modelPath):
    # Load the trained model
    model = load_model(modelPath)
    
    img = cv2.imread(path)
    img = cv2.resize(img, (200, 200))
    
    # Preprocess the signature image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV)
    
    # Extract features from the binary image
    features = thresh.flatten()
    
    # Predict the identity of the person who signed the signature
    prediction = np.argmax(model.predict(np.array([features]))[0])
    
    # Print the result
    return prediction

# print(predictSignature('tuan.png', 'signature_model.h5'))