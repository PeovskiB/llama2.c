import os
import json
import argparse
import codecs
import re

def clean_and_normalize_file(filename):
    # Read the file as binary
    with open(filename, 'rb') as f:
        data = f.read()

    # Decode the data as UTF-8, replacing any characters that can't be decoded
    text = data.decode('utf-8', errors='replace')

    # Replace LS and PS with standard newline
    text = text.replace('\u2028', '\n').replace('\u2029', '\n')

    # Normalize other line endings
    text = text.replace('\r\n', '\n').replace('\r', '\n')

    # Remove null characters
    text = text.replace('\x00', '')

    # Remove any non-printable characters except newlines
    text = ''.join(char for char in text if char.isprintable() or char == '\n')

    # Remove invalid control characters that could break JSON parsing
    text = re.sub(r'[\x00-\x1F\x7F]', '', text)

    # Parse the cleaned data as JSON
    try:
        json_data = json.loads(text)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from file {filename}: {e}")
        return

    # Clean the text in each JSON entry
    for item in json_data:
        if 'text' in item:
            item['text'] = clean_text(item['text'])

    # Write the cleaned JSON data back to the file
    with codecs.open(filename, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

def clean_text(text):
    # Replace LS and PS with standard newline
    text = text.replace('\u2028', '\n').replace('\u2029', '\n')
    # Normalize other line endings
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    # Remove any control characters except newline
    text = ''.join(char for char in text if ord(char) >= 32 or char == '\n')
    # Remove any non-ASCII characters (optional, uncomment if needed)
    # text = re.sub(r'[^\x00-\x7F]+', '', text)
    return text

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
