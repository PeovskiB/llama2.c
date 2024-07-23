import json
import os
import math

# Function to split the list into chunks
def split_list(data, chunk_size):
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

# Read the JSON file
input_filename = 'data/single/CombinedRandomized_20240703234323.json'
with open(input_filename, 'r') as file:
    data = json.load(file)

# Check if the data is a list
if not isinstance(data, list):
    raise ValueError("The JSON data should be an array of objects")

# Determine the size of each chunk
num_chunks = 20
chunk_size = math.ceil(len(data) / num_chunks)

# Split the data into chunks
chunks = split_list(data, chunk_size)

# Create a directory to store the output files
output_dir = 'data/TinyStories_all_data'
os.makedirs(output_dir, exist_ok=True)

# Write each chunk to a separate JSON file
for i, chunk in enumerate(chunks):
    output_filename = os.path.join(output_dir, f'data_part_{i + 1}.json')
    with open(output_filename, 'w') as file:
        json.dump(chunk, file, indent=4)

print(f'Successfully split the data into {num_chunks} files.')
