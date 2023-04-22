import cv2
import numpy as np
from keras.models import load_model

def predictSignature(path, modelPath):
    # Load the trained model
    model = load_model(modelPath)
    
    # Load and preprocess a new signature image
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (200, 200))
    img = cv2.GaussianBlur(img, (5, 5), 0)
    img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)[1]
    img = img.flatten()
    # img = np.expand_dims(img, axis=0)
    # img = img.reshape(1, 40000)
    
    # Make a prediction using the loaded model
    prediction = model.predict(np.array([img]))
    predicted_label = np.argmax(prediction[0])
    
    print(predicted_label)
    
    if (prediction[0][predicted_label] == 0):
        return -1
    
    # Print the predicted label
    return predicted_label

# print(predictSignature('tuan.png', 'signature_model.h5'))