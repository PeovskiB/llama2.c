import json
import os
import sys
import glob

def chunk_json_file(input_file, output_dir, chunk_size_mb=300):
    chunk_size_bytes = chunk_size_mb * 1024 * 1024
    chunk_number = 1
    current_chunk = []
    current_chunk_size = 0

    base_filename = os.path.splitext(os.path.basename(input_file))[0]

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for item in data:
        item_size = sys.getsizeof(json.dumps(item))
        if current_chunk_size + item_size > chunk_size_bytes and current_chunk:
            write_chunk(current_chunk, output_dir, base_filename, chunk_number)
            chunk_number += 1
            current_chunk = []
            current_chunk_size = 0

        current_chunk.append(item)
        current_chunk_size += item_size

    if current_chunk:
        write_chunk(current_chunk, output_dir, base_filename, chunk_number)

def write_chunk(chunk, output_dir, base_filename, chunk_number):
    output_file = os.path.join(output_dir, f"{base_filename}_chunk_{chunk_number}.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(chunk, f)
    print(f"Chunk {chunk_number} written to {output_file}")

def process_directory(input_dir, output_dir, chunk_size_mb=300):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for input_file in glob.glob(os.path.join(input_dir, '*.json')):
        print(f"Processing {input_file}...")
        chunk_json_file(input_file, output_dir, chunk_size_mb)

if __name__ == "__main__":
    input_dir = "data/processed"
    output_dir = "data/TinyStories_all_data"
    chunk_size_mb = 300  # You can change this if needed
    process_directory(input_dir, output_dir, chunk_size_mb)