import os
import csv
import re
from datetime import datetime

# Script variables
directory_current = os.getcwd()
directory_toolkit = os.path.dirname(directory_current)
default_input_directory = os.path.join(directory_toolkit, "_input")
default_output_directory = os.path.join(directory_toolkit, "_output")

def regex_search(file_path, regex_file, output_csv=None):
    try:
        if output_csv:
            mode = 'a' if os.path.exists(output_csv) else 'w'
            with open(output_csv, mode, newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file)
                if mode == 'w':
                    csv_writer.writerow(['source_file', 'source_row_number', 'matched_regex', 'source_data'])

        with open(file_path, 'r', encoding='utf-8') as file:
            with open(regex_file, 'r') as regex_file:
                regex_list = [line.strip() for line in regex_file]
                
            for line_number, line in enumerate(file, start=1):
                for regex_pattern in regex_list:
                    matches = re.findall(regex_pattern, line)
                    for match in matches:
                        print(f"File: {file_path}, Line {line_number}: {match}")

                        if output_csv:
                            with open(output_csv, 'a', newline='', encoding='utf-8') as csv_file:
                                csv_writer = csv.writer(csv_file)
                                csv_writer.writerow([file_path, line_number, match, line.strip()])
    except Exception as e:
        print(f"An error occurred while processing {file_path}: {e}")

if __name__ == "__main__":
    accept_default = input(f'Would you like to accept the default directory? (Default directory is: {default_input_directory}) (Y/N): ')
    if accept_default.lower() == 'n':
        path = input('Please enter the file or directory path to search: ')
    else:
        path = default_input_directory
    regex_file = f"{directory_toolkit}/input_regex.txt"
    
    current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
    default_output_csv = os.path.join(default_output_directory, f"{current_datetime}_regex_matches.csv")
    output_csv = input(f'Enter the CSV file name to save results (Default: {default_output_csv}) (press Enter to skip): ') or default_output_csv

    if os.path.isdir(path):
        for root, _, files in os.walk(path):
            for file_name in files:
                file_to_search = os.path.join(root, file_name)
                regex_search(file_to_search, regex_file, output_csv)
    elif os.path.isfile(path):
        regex_search(path, regex_file, output_csv)
    else:
        print("Invalid path provided.")
