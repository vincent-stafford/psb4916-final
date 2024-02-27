import cv2
import os
import numpy as np

#CONSTANTS
IMAGE_DIR = ".\\trimmed_image_data"
WHITESPACE_DEST = ".\\trimmed_image_data\\whitespace"

def main():
    extensions = ('.png', '.jpg', '.tif', '.tiff')
    for filename in os.listdir(IMAGE_DIR):
        if filename.lower().endswith(extensions):
            image_path = os.path.join(IMAGE_DIR, filename)
            image = cv2.imread(image_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            blur = cv2.blur(gray,(5,5))
            _, binary = cv2.threshold(blur, 40, 255, cv2.THRESH_BINARY)
            circles = cv2.HoughCircles(binary, cv2.HOUGH_GRADIENT, dp=1.2, minDist=10, param1=50, param2=15, minRadius=0, maxRadius=30)
            if circles is None:
                print("No circles Detected")
                os.rename(image_path, os.path.join(WHITESPACE_DEST, filename))
            else:
                print("Immunogold Detected")



if __name__ == '__main__':
    main()