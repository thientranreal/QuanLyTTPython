from MainInterface import MainInterface as mGui

mGui.MainInterface()

# import cv2
# import numpy as np

# # Load image
# image = cv2.imread('SignatureImg/KH01/1.png')

# # Convert to HSV format
# hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# # Define lower and upper color threshold
# lower = np.array([90, 38, 0])
# upper = np.array([145, 255, 255])

# # Generate mask
# mask = cv2.inRange(hsv, lower, upper)

# # Detect signature
# contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# for cnt in contours:
#     x,y,w,h = cv2.boundingRect(cnt)
#     if w > 50 and h > 50:
#         signature = image[y:y+h,x:x+w]

# # Create new image
# new_image = np.zeros((512,512,3), np.uint8)

# # Copy signature to new image
# new_image[100:100+signature.shape[0], 100:100+signature.shape[1]] = signature

# # Show result
# cv2.imshow('Result', new_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()