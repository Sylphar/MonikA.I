import os
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dialogue_combination.log'),
        logging.StreamHandler()
    ]
)

def combine_dialogue_files(input_folder: str, output_file: str):
    """Combine all dialogue .txt files from input_folder into a single file."""
    try:
        # Get all .txt files in the input folder
        txt_files = [f for f in os.listdir(input_folder) if f.endswith('_dialogue.txt')]
        txt_files.sort()  # Sort files for consistent ordering
        
        logging.info(f"Found {len(txt_files)} dialogue files to combine")
        
        with open(output_file, 'w', encoding='utf-8') as outfile:
            for i, filename in enumerate(txt_files, 1):
                input_path = os.path.join(input_folder, filename)
                logging.info(f"Processing file {i}/{len(txt_files)}: {filename}")
                
                try:
                    with open(input_path, 'r', encoding='utf-8') as infile:
                        content = infile.read().strip()
                        
                    if content:  # Only write non-empty content
                        outfile.write(content)
                        # Add separation between files if not the last file
                        if i < len(txt_files):
                            outfile.write('\n\n<|im_start|>system\nNew conversation\n<|im_end|>\n\n')
                            
                except Exception as e:
                    logging.error(f"Error processing {filename}: {str(e)}")
                    continue
        
        logging.info(f"Successfully combined all dialogues into {output_file}")
        
    except Exception as e:
        logging.error(f"Error combining dialogue files: {str(e)}")

if __name__ == "__main__":
    input_folder = "dialogue_output"
    output_file = "MonikaDatabase.txt"
    combine_dialogue_files(input_folder, output_file)
