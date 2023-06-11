import cv2

# Load the image
image = cv2.imread("/home/yarobonz/Desktop/Plixel/Datasets/ITEMS/Plixel Items - 2/Tinkers.Construct/tinkers_gadgetry.png")

# Get the average color of the image
average_color = cv2.median(image)

# Print the average color
print(average_color)