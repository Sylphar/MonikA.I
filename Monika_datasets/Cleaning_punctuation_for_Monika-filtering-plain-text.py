import re
import os

def remove_spaces_before_punctuation(text):
    # This regex matches spaces before punctuation (including ellipses) and removes them
    return re.sub(r'\s([?.!,;:…](?:\s|$))', r'\1', text)

def move_emotional_tags(text):
    # This regex finds emotional tags after "Assistant:" and moves them in front
    return re.sub(r'Assistant:\s*((?:\[[^\]]+\]\s*)+)', r'\1Assistant:', text)

def replace_player_nickname(text):
    # Replace [mas_get_player_nickname] with <USER>
    return text.replace('[mas_get_player_nickname]', '<USER>')

def process_file(input_file, output_file):
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # Process each line
    cleaned_lines = []
    for line in lines:
        # Remove spaces before punctuation
        line = remove_spaces_before_punctuation(line)
        # Move emotional tags in front of "Assistant:"
        line = move_emotional_tags(line)
        # Replace [mas_get_player_nickname] with <USER>
        line = replace_player_nickname(line)
        cleaned_lines.append(line)
    
    # Write the cleaned lines to the output file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(cleaned_lines)
# Define file paths
input_file_path = os.path.join('dialogue_output', 'monika-database.txt')
output_file_path = os.path.join('dialogue_output', 'monika-database-cleaned.txt')

# Process the file
process_file(input_file_path, output_file_path)

print(f"Cleaned dataset saved to: {output_file_path}")