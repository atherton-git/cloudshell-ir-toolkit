"""
Script: IPv4 Search
Version: 1.3
Author: Jack Atherton
Synopsis: Performs a search for IPv4 addresses in cleartext files and prints the matching lines to csv output.
"""

import os
import csv
import re
from datetime import datetime
from ipaddress import ip_address

# Script variables
directory_current = os.getcwd()
directory_toolkit = os.path.dirname(directory_current)
default_input_directory = os.path.join(directory_toolkit, "_input")
default_output_directory = os.path.join(directory_toolkit, "_output")

def ipv4_search(file_path, output_csv=None, include_private=True):
    try:
        if output_csv:
            mode = 'a' if os.path.exists(output_csv) else 'w'
            with open(output_csv, mode, newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file)
                if mode == 'w':
                    csv_writer.writerow(['source_file', 'source_row_number', 'matched_ipv4', 'source_data'])

        with open(file_path, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):
                ipv4_addresses = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', line)
                for ipv4_address in ipv4_addresses:
                    ip = ip_address(ipv4_address)
                    if include_private or not ip.is_private:
                        print(f"File: {file_path}, Line {line_number}: {ipv4_address}")

                        if output_csv:
                            with open(output_csv, 'a', newline='', encoding='utf-8') as csv_file:
                                csv_writer = csv.writer(csv_file)
                                csv_writer.writerow([file_path, line_number, ipv4_address, line.strip()])
    except Exception as e:
        print(f"An error occurred while processing {file_path}: {e}")

if __name__ == "__main__":
    accept_default = input(f'Would you like to accept the default directory? (Default directory is: {default_input_directory}) (Y/N): ')
    if accept_default.lower() == 'n':
        path = input('Please enter the file or directory path to search: ')
    else:
        path = default_input_directory
    include_private = input('Include private IPv4 addresses (RFC1918)? (Y/N): ').lower() == 'y'

    current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
    default_output_csv = os.path.join(default_output_directory, f"{current_datetime}_ipv4_addresses.csv")
    output_csv = input(f'Enter the CSV file name to save results (Default: {default_output_csv}) (press Enter to skip): ') or default_output_csv

    if os.path.isdir(path):
        for root, _, files in os.walk(path):
            for file_name in files:
                file_to_search = os.path.join(root, file_name)
                ipv4_search(file_to_search, output_csv, include_private)
    elif os.path.isfile(path):
        ipv4_search(path, output_csv, include_private)
    else:
        print("Invalid path provided.")
