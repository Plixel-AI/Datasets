import os
from PIL import Image

directory = '/home/yarobonz/Desktop/Plixel/Datasets/Types/BLOCKS/Plixel Blocks ARR/BetterEnd/'  # Replace with the actual directory path

deleted_count = 0

for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)
    if os.path.isfile(file_path):
        try:
            with Image.open(file_path) as image:
                width, height = image.size
                if width != 16 or height != 16 or image.mode == 'RGBA':
                    # Check if the image is not 16x16 pixels or has an RGBA mode
                    alpha_channel = image.split()[-1]  # Get the alpha channel
                    if alpha_channel.getextrema() == (0, 0):
                        # Check if the alpha channel has 100% transparency
                        os.remove(file_path)
                        deleted_count += 1
        except (IOError, OSError, Image.UnidentifiedImageError):
            # Handle exception if the file cannot be opened as an image
            pass

print(f"Deleted {deleted_count} files.")
