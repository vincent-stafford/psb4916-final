import cv2
import os
import numpy as np

#Constants!!!
PIXEL_TRIM_AMOUNT = 67 #The sample images in this dataset come with a scale bar at the bottom of the image. 
GRID_COUNT = 8 #Change this to change the number of subimages made. it provides n^2 subimages. 

def trim_and_skin(path, end_dir, div_count):
    
    filename_without_extension, extension = os.path.splitext(path)

    # Load the image
    image = cv2.imread(path)
    if image is None:
        exit(1)

    pixels_to_trim = PIXEL_TRIM_AMOUNT
    trimmed_image = image[:-pixels_to_trim, :]
    
    heightnew, widthnew = trimmed_image.shape[:2]
    # Define the number of pieces horizontally and vertically
    num_pieces_horizontal = div_count
    num_pieces_vertical = div_count

    # Calculate the size of each piece
    piece_height = heightnew // num_pieces_vertical
    piece_width = widthnew // num_pieces_horizontal

    # Slice the image into pieces
    for i in range(num_pieces_vertical):
        for j in range(num_pieces_horizontal):
            # Calculate the coordinates of the current piece
            start_row = i * piece_height
            end_row = (i + 1) * piece_height
            start_col = j * piece_width
            end_col = (j + 1) * piece_width
            
            # Extract the piece and save or display it
            piece = trimmed_image[start_row:end_row, start_col:end_col]
            path = os.path.join(end_dir, filename_without_extension+"_"+str(i)+str(j)+".tif")
            cv2.imwrite(path, piece)

def main():
    base_dir = "C:\\Users\\Chloe\\Downloads\\OneDrive_2024-02-02\\Gold Particle Labelling\\labeled replica - Test Data from Synapses"
    folder = "..\\trimmed_image_data"
    image_extensions = ['.jpg', '.jpeg', '.png', '.tif', '.tiff', '.bmp', '.gif']

    for filename in os.listdir(base_dir):
        if any(filename.lower().endswith(ext) for ext in image_extensions):
            trim_and_skin(filename, folder, GRID_COUNT)

if __name__ == '__main__':
    main()