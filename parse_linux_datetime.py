import os
import re
import pandas as pd
from datetime import datetime

# User-defined variables
log_directory = r"./_input/linux/"
output_file = r'./_output/'

def process_log_entry(timestamp_string, line, line_number, current_year, relative_path, channel):
    # Check if the log payload has been processed before
    if line.strip() not in processed_payloads:
        timestamp = None
        formats_to_try = [('%Y %b %d %H:%M:%S', f"{current_year} {timestamp_string}"),  # Example: '2023 Aug 09 00:33:21'
                          ('%Y %b %d %H:%M:%S.%f', f"{current_year} {timestamp_string}"),  # Example: '2023 Aug 09 00:33:21.915900'
                          ('%Y-%m-%d %H:%M:%S', timestamp_string),  # Example: '2020-07-07 19:33:19'
                          ('%d/%b/%Y:%H:%M:%S', timestamp_string)]  # Example: '09/Aug/2023:04:44:03'
        
        for format_to_try, formatted_timestamp_string in formats_to_try:
            try:
                timestamp = datetime.strptime(formatted_timestamp_string, format_to_try)
                break  # Stop trying if one format succeeds
            except ValueError:
                pass

        if timestamp:
            timestamps.append({'Time Generated': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                               'Filename': relative_path,
                               'Line': line_number,
                               'Channel': channel,
                               'Payload': line.strip()})
            processed_payloads.add(line.strip())
            print(f"Processed timestamp {timestamp.strftime('%Y-%m-%d %H:%M:%S')} in file {relative_path} (Line {line_number})")

current_year = datetime.now().year
timestamps = []
processed_payloads = set()

patterns = [r'(\w{3} \d{1,2} \d{2}:\d{2}:\d{2})',  # Example: 'Aug 09 00:33:21'
            r'(\w{3} \d{1,2} \d{2}:\d{2}:\d{2}\.\d{6})',  # Example: 'Aug 09 00:33:21.915900'
            r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})',  # Example: '2020-07-07 19:33:19'
            r'(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2})']  # Example: '09/Aug/2023:04:44:03'

print(f"Searching for log files in {log_directory} and its subdirectories...")

for root, _, files in os.walk(log_directory):
    for file in files:
        current_file = os.path.join(root, file)
        relative_path = os.path.relpath(current_file, log_directory)
        channel = channel = os.path.splitext(file)[0].split('.')[0]

        try:
            with open(current_file, 'r', encoding='unicode_escape') as reader:
                line_number = 1

                for line in reader:
                    for pattern in patterns:
                        matches = re.finditer(pattern, line)
                        for match in matches:
                            timestamp_string = match.group(1)
                            process_log_entry(timestamp_string, line, line_number, current_year, relative_path, channel)

                    line_number += 1
        except Exception as e:
            print(f"Error processing file {relative_path}: {str(e)}")

df = pd.DataFrame(timestamps)
df.to_csv(output_file, index=False)
print(f"Processing completed. Total timestamps processed: {len(timestamps)}")
