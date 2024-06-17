import os
import csv
from datetime import datetime

# Script variables
directory_current = os.getcwd()
directory_toolkit = os.path.dirname(directory_current)
default_input_directory = os.path.join(directory_toolkit, "_input")
default_output_directory = os.path.join(directory_toolkit, "_output")
input_wordlist_file = os.path.join(directory_toolkit, "input_wordlist.txt")

def freetext(file_path, search_queries, output_csv=None):
    try:
        if output_csv:
            output_csv = os.path.join(default_output_directory, output_csv)
            with open(output_csv, 'w', newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(['search_query', 'source_file', 'source_row_number', 'source_data'])

        if os.path.isdir(file_path):
            for root, _, files in os.walk(file_path):
                for file_name in files:
                    file_to_search = os.path.join(root, file_name)
                    print(f"Processing file: {file_to_search}")
                    for search_query in search_queries:
                        search_in_single_file(file_to_search, search_query, output_csv)
        elif os.path.isfile(file_path):
            print(f"Processing file: {file_path}")
            for search_query in search_queries:
                search_in_single_file(file_path, search_query, output_csv)
        else:
            print("Invalid path provided.")
    except Exception as e:
        print(f"An error occurred: {e}")

def search_in_single_file(file_path, search_query, output_csv=None):
    try:
        matches = []
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):
                if search_query.lower() in line.lower():
                    matches.append((search_query, file_path, line_number, line.strip()))
                    
                    if output_csv:
                        with open(output_csv, 'a', newline='', encoding='utf-8') as csv_file:
                            csv_writer = csv.writer(csv_file)
                            csv_writer.writerow([search_query, file_path, line_number, line.strip()])

        if matches:
            for match in matches:
                print(f"Search query: {match[0]}, File: {match[1]}, Line {match[2]}: {match[3]}")
        else:
            print(f"\033[31mSearch query: {search_query}, File: {file_path}, No matches found, or EOF.\033[0m")  # Print in red

    except Exception as e:
        print(f"An error occurred while processing {file_path}: {e}")

if __name__ == "__main__":
    try:
        with open(input_wordlist_file, 'r', encoding='utf-8') as f:
            search_queries = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Wordlist file not found: {input_wordlist_file}")
        exit(1)

    accept_default = input(f'Would you like to accept the default directory? (Default directory is: {default_input_directory}) (Y/N): ')
    path = default_input_directory if accept_default.lower() == 'y' else input('Please enter the file or directory path to search: ')

    current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
    default_output_csv = os.path.join(default_output_directory, f"{current_datetime}_wordlist.csv")
    output_csv = input(f'Enter the CSV file name to save results (Default: {default_output_csv}) (press Enter to skip): ') or default_output_csv

    freetext(path, search_queries, output_csv)
