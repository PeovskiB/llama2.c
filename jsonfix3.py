import os
import json
import argparse
import re

def clean_and_convert_json_to_utf8(filename):
    # Read the file and clean non-printable characters and normalize line endings
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        data = f.read()
    
    # Remove all non-printable characters including null characters
    data = re.sub(r'[^\x20-\x7E\n]', '', data).replace('\r\n', '\n').replace('\r', '\n')

    # Parse the cleaned data as JSON
    try:
        json_data = json.loads(data)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from file {filename}: {e}")
        return

    # Write the cleaned and normalized JSON data back to the file with UTF-8 encoding
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

def main():
    parser = argparse.ArgumentParser(description='Clean and convert JSON files to UTF-8 encoding')
    parser.add_argument('directory', type=str, help='Directory containing JSON files')
    args = parser.parse_args()

    # Iterate over JSON files in the directory
    for filename in os.listdir(args.directory):
        if filename.endswith('.json'):
            filepath = os.path.join(args.directory, filename)
            clean_and_convert_json_to_utf8(filepath)
            print(f"Cleaned and converted {filepath} to UTF-8 encoding")

if __name__ == "__main__":
    main()
