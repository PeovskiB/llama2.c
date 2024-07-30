import os
import json
import argparse
import codecs

def clean_and_normalize_file(input_filename, output_filename):
    buffer_size = 1024 * 1024  # 1 MB buffer size

    # Read the file as binary in chunks
    with open(input_filename, 'rb') as input_file, open(output_filename, 'wb') as output_file:
        while chunk := input_file.read(buffer_size):
            output_file.write(chunk.replace(b'\x00', b''))

    # Try to detect the encoding
    with open(output_filename, 'rb') as f:
        data = f.read()
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

    # Normalize line endings
    text = text.replace('\r\n', '\n').replace('\r', '\n')

    # Remove any non-printable characters except newlines
    text = ''.join(char for char in text if char.isprintable() or char == '\n')

    # Parse the cleaned data as JSON
    try:
        json_data = json.loads(text)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from file {input_filename}: {e}")
        return

    # Write the cleaned JSON data back to the file
    with codecs.open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

def main():
    parser = argparse.ArgumentParser(description='Clean and normalize JSON files')
    parser.add_argument('--directory', type=str, help='Directory containing JSON files')
    parser.add_argument('--output_directory', type=str, help='Directory to save cleaned JSON files', default=None)
    args = parser.parse_args()

    output_directory = args.output_directory if args.output_directory else args.directory

    # Create output directory if it does not exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Iterate over JSON files in the directory
    for filename in os.listdir(args.directory):
        if filename.endswith('.json'):
            input_filepath = os.path.join(args.directory, filename)
            output_filepath = os.path.join(output_directory, filename)
            clean_and_normalize_file(input_filepath, output_filepath)
            print(f"Cleaned and normalized {input_filepath} to {output_filepath}")

if __name__ == "__main__":
    main()
