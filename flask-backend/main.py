import cv2
import numpy as np
from sklearn.cluster import KMeans

def find_predominant_color(image_path):
    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Unable to read the image at path: {image_path}")
    # Calculate the center region of the image
    h, w, _ = image.shape
    center_x, center_y = w // 2, h // 2
    size = min(w, h) // 4  # Use a quarter of the smallest dimension for the square size
    center_region = image[center_y-size//2:center_y+size//2, center_x-size//2:center_x+size//2]

    # Reshape the center region to a 2D array of color values (for k-means)
    reshaped = center_region.reshape((-1, 3))

    # Use k-means clustering to find the most predominant color in the center region
    kmeans = KMeans(n_clusters=1, random_state=0).fit(reshaped)
    predominant_color = kmeans.cluster_centers_.astype(int)[0]

    # Convert BGR to RGB
    predominant_color = predominant_color[::-1]

    return tuple(predominant_color)

if __name__ == "__main__":
    image_path = "./berry.jpg"
    color = find_predominant_color(image_path)
    print(f"The predominant color in the center of the image is: {color}")
