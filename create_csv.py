import os
import csv
import sys
from datetime import datetime
from collections import defaultdict

def delete_file_if_exists(folder_path, file_name):
    file_path = os.path.join(folder_path, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"File {file_name} deleted successfully.")
    else:
        print(f"File {file_name} does not exist in the specified folder.")

def merge_csv_files(folder_path, output_file):
    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
    if not csv_files:
        print("No CSV files found in the specified folder.")
        return
    
    with open(output_file, 'w', newline='') as output:
        csv_writer = csv.writer(output)
        for csv_file in csv_files:
            with open(os.path.join(folder_path, csv_file), 'r') as input_file:
                csv_reader = csv.reader(input_file)
                csv_writer.writerows(csv_reader)

    print(f"All CSV files in {folder_path} merged into {output_file} successfully.")


def delete_row_by_pattern(csv_file, pattern):
    rows_to_keep = []
    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if pattern not in row:
                rows_to_keep.append(row)

    with open(csv_file, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(rows_to_keep)

    print(f"Header deleted from {csv_file} successfully.")

def count_values_in_first_column(csv_file):
    value_counts = defaultdict(int)

    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header if it exists
        for row in csv_reader:
            if row:  # Skip empty rows
                first_column_value = row[1].strip()
                value_counts[first_column_value] += 1

    return value_counts

def add_header_to_csv(csv_file, header_row):
    with open(csv_file, 'r+') as file:
        csv_reader = csv.reader(file)
        rows = list(csv_reader)
        file.seek(0)
        file.truncate(0)  # Clear the file content
        csv_writer = csv.writer(file, lineterminator='\n')
        csv_writer.writerow(header_row)
        csv_writer.writerows(rows)

    print(f"Header row added to {csv_file} successfully.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python create_csv.py <csv_folder>")
        sys.exit(1)

#Identify work folder
#folder_path = datetime.now().strftime('%Y%m%d') + '_bases_popup'
folder_path = sys.argv[1]
print(f"Folder path: {folder_path}")

#Delete file if exist
delete_file_if_exists(folder_path, 'ListSegment_Validos.csv')

#Create new file ListSegment_Validos.csv inside the folder
output_file = folder_path + '\ListSegment_Validos.csv'
print(f"Output file: {output_file}")

pattern = ['segmentlabel', 'segmentName', 'idAccountSettings', 'flat']
merge_csv_files(folder_path, output_file)
delete_row_by_pattern(output_file, pattern)

#Write all segments uploaded
counts = count_values_in_first_column(output_file)
for value, count in counts.items():
    print(f"Segment: {value}, Count: {count}")

add_header_to_csv(output_file, pattern)
