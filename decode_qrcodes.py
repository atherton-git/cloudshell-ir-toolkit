import os
import numpy as np
import pyboof as pb

# Function to process a single image and detect QR codes
def process_image(image_path):
    detector = pb.FactoryFiducial(np.uint8).qrcode()
    image = pb.load_single_band(image_path, np.uint8)
    detector.detect(image)

    print("Detected a total of {} QR Codes in {}".format(len(detector.detections), image_path))
    
    for qr in detector.detections:
        print("Message: " + qr.message)
        print("     at: " + str(qr.bounds))
        print()

# Directory path containing the QR code images
directory_path = "./_input/qrcodes/"

# List of allowed file extensions
allowed_extensions = [".png", ".jpg", ".jpeg"]  # Add more extensions if needed

# Iterate through files in the directory
for filename in os.listdir(directory_path):
    if any(filename.lower().endswith(ext) for ext in allowed_extensions):
        image_path = os.path.join(directory_path, filename)
        process_image(image_path)
