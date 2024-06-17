import os
import csv
from datetime import datetime
import re

# Script variables
directory_current = os.getcwd()
directory_toolkit = os.path.dirname(directory_current)
default_input_directory = os.path.join(directory_toolkit, "_input")
default_output_directory = os.path.join(directory_toolkit, "_output")
input_regex_file = os.path.join(directory_toolkit, "input_regex.txt")

def freetext(file_path, regex_patterns, output_csv=None):
    try:
        if output_csv:
            output_csv = os.path.join(default_output_directory, output_csv)
            with open(output_csv, 'w', newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(['regex_pattern', 'pattern_description', 'source_file', 'source_row_number', 'source_data'])

        if os.path.isdir(file_path):
            for root, _, files in os.walk(file_path):
                for file_name in files:
                    file_to_search = os.path.join(root, file_name)
                    print(f"Processing file: {file_to_search}")
                    for pattern, description in regex_patterns.items():
                        search_in_single_file(file_to_search, pattern, description, output_csv)
        elif os.path.isfile(file_path):
            print(f"Processing file: {file_path}")
            for pattern, description in regex_patterns.items():
                search_in_single_file(file_path, pattern, description, output_csv)
        else:
            print("Invalid path provided.")
    except Exception as e:
        print(f"An error occurred: {e}")

def search_in_single_file(file_path, regex_pattern, pattern_description, output_csv=None):
    try:
        matches = []
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):
                if re.search(regex_pattern, line):
                    matches.append((regex_pattern, pattern_description, file_path, line_number, line.strip()))
                    
                    if output_csv:
                        with open(output_csv, 'a', newline='', encoding='utf-8') as csv_file:
                            csv_writer = csv.writer(csv_file)
                            csv_writer.writerow([regex_pattern, pattern_description, file_path, line_number, line.strip()])

        if matches:
            for match in matches:
                print(f"Regex pattern: {match[0]}, Description: {match[1]}, File: {match[2]}, Line {match[3]}: {match[4]}")
        else:
            print(f"\033[31mRegex pattern: {regex_pattern}, Description: {pattern_description}, File: {file_path}, No matches found, or EOF.\033[0m")  # Print in red

    except Exception as e:
        print(f"An error occurred while processing {file_path}: {e}")

if __name__ == "__main__":
    try:
        with open(input_regex_file, 'r', encoding='utf-8') as f:
            regex_patterns = {}
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '#' in line:
                    pattern, description = line.split('#', 1)
                    regex_patterns[pattern.strip()] = description.strip()
    except FileNotFoundError:
        print(f"Regex file not found: {input_regex_file}")
        exit(1)

    accept_default = input(f'Would you like to accept the default directory? (Default directory is: {default_input_directory}) (Y/N): ')
    path = default_input_directory if accept_default.lower() == 'y' else input('Please enter the file or directory path to search: ')

    current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
    default_output_csv = os.path.join(default_output_directory, f"{current_datetime}_regex.csv")
    output_csv = input(f'Enter the CSV file name to save results (Default: {default_output_csv}) (press Enter to skip): ') or default_output_csv

    freetext(path, regex_patterns, output_csv)
