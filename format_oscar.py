import os
import json

def process_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    data = []
    for line in lines:
        json_line = json.loads(line)
        if 'content' in json_line:
            entry = {"text": json_line['content']}
            data.append(entry)
    
    return data

def save_to_json(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

def process_directory(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(".jsonl"):
            input_file = os.path.join(input_dir, filename)
            output_file = os.path.join(output_dir, filename.replace('.jsonl', '.json'))
            
            data = process_text_file(input_file)
            save_to_json(data, output_file)
            
            print(f"Processed {input_file} and saved to {output_file}")

# Example usage
input_directory = "data/unprocessed"
output_directory = "data/processed"

process_directory(input_directory, output_directory)
