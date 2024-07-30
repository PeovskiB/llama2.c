import os
import json
import argparse

def clean_null_characters(filename):
    # Read the file as binary to avoid encoding errors
    with open(filename, 'rb') as f:
        data = f.read()

    # Remove null bytes and decode to UTF-8, ignoring errors
    data = data.replace(b'\x00', b'').decode('utf-8', errors='ignore')

    # Normalize newlines
    data = data.replace('\r\n', '\n').replace('\r', '\n')

    # Parse the cleaned data as JSON
    try:
        json_data = json.loads(data)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from file {filename}: {e}")
        return

    # Write the cleaned JSON data back to the file with UTF-8 encoding
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

def main():
    parser = argparse.ArgumentParser(description='Remove null characters from JSON files and ensure UTF-8 encoding')
    parser.add_argument('directory', type=str, help='Directory containing JSON files')
    args = parser.parse_args()

    # Iterate over JSON files in the directory
    for filename in os.listdir(args.directory):
        if filename.endswith('.json'):
            filepath = os.path.join(args.directory, filename)
            clean_null_characters(filepath)
            print(f"Cleaned null characters from {filepath} and ensured UTF-8 encoding")

if __name__ == "__main__":
    main()