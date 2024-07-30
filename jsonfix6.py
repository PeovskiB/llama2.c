import os
import json
import argparse
import codecs

def clean_and_normalize_file(filename):
    # Read the file as binary
    with open(filename, 'rb') as f:
        data = f.read()

    # Try to detect the encoding
    try:
        encoding = 'utf-8'
        data.decode(encoding)
    except UnicodeDecodeError:
        try:
            encoding = 'utf-16'
            data.decode(encoding)
        except UnicodeDecodeError:
            encoding = 'latin-1'  # This should work as a fallback for any 8-bit encoding

    # Decode the data
    text = data.decode(encoding, errors='replace')

    # Remove null characters and normalize line endings
    text = text.replace('\x00', '')
    text = text.replace('\r\n', '\n').replace('\r', '\n')

    # Remove any non-printable characters except newlines
    text = ''.join(char for char in text if char.isprintable() or char == '\n')

    # Parse the cleaned data as JSON
    try:
        json_data = json.loads(text)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from file {filename}: {e}")
        return

    # Write the cleaned JSON data back to the file
    with codecs.open(filename, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

def main():
    parser = argparse.ArgumentParser(description='Clean and normalize JSON files')
    parser.add_argument('directory', type=str, help='Directory containing JSON files')
    args = parser.parse_args()

    # Iterate over JSON files in the directory
    for filename in os.listdir(args.directory):
        if filename.endswith('.json'):
            filepath = os.path.join(args.directory, filename)
            clean_and_normalize_file(filepath)
            print(f"Cleaned and normalized {filepath}")

if __name__ == "__main__":
    main()