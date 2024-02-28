import os 
from PIL import Image
import numpy as np
import logging
from sklearn.model_selection import train_test_split
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt

#CONSTANTS
logging.basicConfig(level=logging.INFO, format="%(name)s: %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s | %(process)d >>> %(message)s")
logger = logging.getLogger("DBSCAN AI")
data_directory = ".\\particle_data"
allowed_exts = ('.tif')

def visualize_clustering_on_image(image, labels):
    # Reshape labels to match the original image shape for visualization
    labels_reshaped = labels.reshape(image.shape)
    
    # Create a figure to display original and clustered images side by side
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    
    ax[0].imshow(image, cmap='gray')
    ax[0].title.set_text('Original Image')
    ax[0].axis('off')
    
    # Display clustered image
    ax[1].imshow(labels_reshaped, cmap='nipy_spectral')
    ax[1].title.set_text('DBSCAN Clustering')
    ax[1].axis('off')
    plt.gcf().canvas.mpl_connect('key_press_event', on_key)
    plt.show()

def on_key(event):
    if event.key == 'enter':
        plt.close()  # Close the plot window

def main():
    logger.info("Creating 3d array from dataset.")
    img_list = []
    for (root,dir,file) in os.walk(data_directory, topdown=True):
        for name in file:
            if name.endswith(allowed_exts):
                final_path = os.path.join(root, name)
                if not(os.path.isfile(final_path)):
                    logger.error("FILE: " + str(final_path) + "IS NOT FOUND?")
                image = Image.open(final_path).convert('L')
                img_list.append(np.array(image))
    
    img_array = np.array(img_list) #This is a 3d np array where [x][y][z] x = image, y = rows, z = columns
    logger.info("Successful Creation of Image Array of legnth: " + str(img_array.shape[0]))
    X_train, X_test = train_test_split(img_array, test_size=0.2, random_state=42)
    logger.info("Splitting Successful.")
    logger.info("Training Set Size: " + str(X_train.shape[0]))
    logger.info("Testing Set Size: " + str(X_test.shape[0]))

    logger.info("Initalizing Model")
    logger.warning("No hyperparamaters were specified, using default values.")
    for i in range(X_train.shape[0]):
        pixels = X_train[i].reshape(-1, 1)  
        dbscan = DBSCAN(eps=0.8, min_samples=7).fit(pixels) #Remember to specify hyperparamaters
        logger.info("Starting to run DBSCAN.")
        #Testing with just 1 image.
        labels = dbscan.labels_

        visualize_clustering_on_image(X_train[i], labels)
    

if __name__ == '__main__':
    logger.info("Initalizing Program...")
    main()