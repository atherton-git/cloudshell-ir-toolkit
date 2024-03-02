"""
Script: Freesearch
Version: 1.2
Author: Jack Atherton
Synopsis: Performs a freetext search cleartext files and prints the matching lines to csv output.
"""

import os
import csv
from datetime import datetime

def freetext(file_path, search_query, output_csv=None):
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        default_input_directory = os.path.join(script_dir, "_input")
        default_output_directory = os.path.join(script_dir, "_output")

        if output_csv:
            output_csv = os.path.join(default_output_directory, output_csv)
            with open(output_csv, 'w', newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(['File', 'Line Number', 'Matched Line'])

        if os.path.isdir(file_path):
            for root, _, files in os.walk(file_path):
                for file_name in files:
                    file_to_search = os.path.join(root, file_name)
                    search_in_single_file(file_to_search, search_query, output_csv)
        elif os.path.isfile(file_path):
            search_in_single_file(file_path, search_query, output_csv)
        else:
            print("Invalid path provided.")
    except Exception as e:
        print(f"An error occurred: {e}")

def search_in_single_file(file_path, search_query, output_csv=None):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            matches_found = False
            for line_number, line in enumerate(file, start=1):
                if search_query.lower() in line.lower():
                    matches_found = True
                    highlighted_line = line.replace(search_query, f"\033[32m{search_query}\033[0m", 1)
                    print(f"File: {file_path}, Line {line_number}: {highlighted_line.strip()}")
                    
                    if output_csv:
                        with open(output_csv, 'a', newline='', encoding='utf-8') as csv_file:
                            csv_writer = csv.writer(csv_file)
                            csv_writer.writerow([file_path, line_number, highlighted_line.strip()])
                            
            if not matches_found:
                print(f"\033[31mFile: {file_path}, No matches found, or EOF.\033[0m")  # Print in red
    except Exception as e:
        print(f"An error occurred while processing {file_path}: {e}")

if __name__ == "__main__":
    # User inputs
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_input_directory = os.path.join(script_dir, "_input")
    default_output_directory = os.path.join(script_dir, "_output")

    accept_default = input(f'Would you like to accept the default directory? (Default directory is: {default_input_directory}) (Y/N): ')
    path = default_input_directory if accept_default.lower() == 'y' else input('Please enter the file or directory path to search: ')
    search_query = input('Please enter the search query: ')

    # Generating default output CSV filename
    current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
    default_output_csv = os.path.join(default_output_directory, f"{current_datetime}_freetext.csv")
    output_csv = input(f'Enter the CSV file name to save results (Default: {default_output_csv}) (press Enter to skip): ') or default_output_csv

    freetext(path, search_query, output_csv)