import os
from tika import parser

# Script variables
directory_current = os.getcwd()
directory_toolkit = os.path.dirname(directory_current)
default_input_directory = os.path.join(directory_toolkit, "_input")
default_output_directory = os.path.join(directory_toolkit, "_input")

def extract_text_with_tika(input_file, output_directory):
    # Parse the file using Tika
    try:
        parsed = parser.from_file(input_file)
        content = parsed.get("content", "")
    except Exception as e:
        print("Error:", e)
        return False

    # Generate output filename based on input filename
    base_filename = os.path.splitext(os.path.basename(input_file))[0]
    file_extension = os.path.splitext(input_file)[1][1:]  # Get the extension without the dot
    output_filename = f"{base_filename}_{file_extension}.txt"
    output_path = os.path.join(output_directory, output_filename)

    # Write text to output file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        print("Error:", e)
        return False

    print("Text extracted successfully and saved to", output_path)
    
    # Remove the original file
    os.remove(input_file)
    print("Original file removed:", input_file)
    
    return True

def process_files(input_directory, output_directory):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Iterate over files in the input directory
    for filename in os.listdir(input_directory):
        input_file = os.path.join(input_directory, filename)
        if filename.endswith((".docx", ".xlsx", ".pptx", ".pdf", ".msg")):
            extract_text_with_tika(input_file, output_directory)
        else:
            print("Skipping file:", input_file)

if __name__ == '__main__':
    process_files(default_input_directory, default_output_directory)
