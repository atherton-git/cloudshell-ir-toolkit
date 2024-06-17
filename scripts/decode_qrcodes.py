import os
import re
import numpy as np
import pyboof as pb

# Function to replace 't' with 'x' only in the matched part of the URL
def sanitize_url(match):
    return match.group().replace('t', 'x')

# Function to process a single image and detect QR codes
def process_image(image_path):
    detector = pb.FactoryFiducial(np.uint8).qrcode()
    image = pb.load_single_band(image_path, np.uint8)
    detector.detect(image)

    print("Detected a total of {} QR Codes in {}:".format(len(detector.detections), image_path))
    
    url_pattern = re.compile(r'https?://[^\s]+')

    for qr in detector.detections:
        sanitized_message = qr.message
        sanitized_message = url_pattern.sub(sanitize_url, sanitized_message)
        print(sanitized_message)
        # print("     at: " + str(qr.bounds))

if __name__ == "__main__":
    # Directory path containing the QR code images
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    directory_path = os.path.join(parent_dir, "_input", "qrcodes")

    # List of allowed file extensions
    allowed_extensions = [".png", ".jpg", ".jpeg"]  # Add more extensions if needed

    # Iterate through files in the directory
    for filename in os.listdir(directory_path):
        if any(filename.lower().endswith(ext) for ext in allowed_extensions):
            image_path = os.path.join(directory_path, filename)
            process_image(image_path)
