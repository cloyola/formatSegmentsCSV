import csv
import os
import sys

def delete_file_if_exists(folder_path, file_name):
    file_path = os.path.join(folder_path, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"File {file_name} deleted successfully.")
    else:
        print(f"File {file_name} does not exist in the specified folder.")


def validate_csv_files(folder_path):
    pattern = ['segmentlabel', 'segmentName', 'idAccountSettings', 'flat']
    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
    if not csv_files:
        print("No CSV files found in the specified folder.")
        return
    
    for csv_file in csv_files:
        with open(os.path.join(folder_path, csv_file), 'r') as file:
            csv_reader = csv.reader(file)
            for line_number, row in enumerate(csv_reader, start=1):
                if len(row) != 4:
                    print(f"Error: {csv_file}:Line {line_number} does not contain exactly 3 commas or 4 columns.")
                if len(row[2].strip()) != 32 and line_number !=1:
                    print(f"Error: {csv_file}:Line {line_number}, idAccountSettings column does not have exactly 32 characters.")
                if row[3].strip() not in ['Y', 'N', ''] and line_number !=1:
                    print(f"Error: {csv_file}:Line {line_number}, flat column does not have Y/N or empty value.")
                for i in range(3):
                    if i < len(row) and not row[i].strip():
                        print(f"Error: {csv_file}:Line {line_number} contains empty columns.")

    print(f"All CSV files in {folder_path} validated successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_csv.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]
    delete_file_if_exists(folder_path, 'ListSegment_Validos.csv')
    validate_csv_files(folder_path)
