import re
import os
from pathlib import Path

def clean_dialogue(text):
    """Clean and standardize dialogue text."""
    text = re.sub(r'\[player\]', '<USER>', text, flags=re.IGNORECASE)
    text = re.sub(r'\[m_name\]', '<MONIKA>', text, flags=re.IGNORECASE)
    text = re.sub(r'\{.*?\}', '', text)
    text = re.sub(r'\(.*?\)', '', text)
    text = re.sub(r'\w{50,}', '', text)
    text = re.sub(r'([?.!,])', r' \1 ', text)
    text = re.sub(r'~', '', text)
    text = re.sub(r"'s", " is", text)
    text = re.sub(r"'m", " am", text)
    text = re.sub(r"'re", " are", text)
    text = re.sub(r"'ll", " will", text)
    text = re.sub(r"'ve", " have", text)
    text = re.sub(r"'d", " would", text)
    text = re.sub(r'\.\s*\.\s*\.', '...', text)
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()

def parse_event_data(content, start_index):
    """Extract event metadata from multi-line event definition."""
    event_data = {}
    lines = content.split('\n')
    
    # Look for event definition end
    end_index = start_index
    while end_index < len(lines) and not lines[end_index].strip().endswith(')'):
        end_index += 1
    
    # Combine lines into single string for parsing
    event_def = ' '.join(lines[start_index:end_index+1])
    
    try:
        # Extract key components
        label_match = re.search(r'eventlabel=["\']([^"\']+)["\']', event_def)
        if label_match:
            event_data['id'] = label_match.group(1)
        
        category_match = re.search(r'category=\[(.*?)\]', event_def)
        if category_match:
            categories = re.findall(r'["\']([^"\']+)["\']', category_match.group(1))
            event_data['categories'] = categories

        prompt_match = re.search(r'prompt=["\']([^"\']+)["\']', event_def)
        if prompt_match:
            event_data['prompt'] = prompt_match.group(1)

        for field in ['random', 'pool', 'unlocked']:
            if f'{field}=True' in event_def:
                event_data[field] = True
                
    except Exception as e:
        print(f"Error parsing event data: {str(e)}")
    
    return event_data, end_index

def format_metadata(event_data):
    """Format event data into metadata string."""
    parts = []
    
    if 'id' in event_data:
        parts.append(f"ID: {event_data['id']}")
    
    if 'prompt' in event_data:
        parts.append(f"Topic: {event_data['prompt']}")
    elif 'id' in event_data:
        parts.append(f"Topic: {event_data['id']}")
    
    if 'categories' in event_data:
        parts.append(f"Categories: {', '.join(event_data['categories'])}")
    
    if 'random' in event_data and event_data['random']:
        parts.append("Can occur randomly")
    elif 'pool' in event_data and event_data['pool']:
        parts.append("Can be initiated by player")
    
    return f"## {' | '.join(parts)}" if parts else ""

def get_emotion(sprite_code):
    """Extract emotion from sprite code following the order: eyes, eyebrows, blush, tears, mouth.
    Returns unique emotion tags."""
    if not sprite_code:
        return ""
        
    emotions = set()  # Using a set to avoid duplicates
    
    # Define emotion mappings by category
    # TO DO : create combinaisons lists, like happy+worried = Awkward
    # Remove [neutral] from expressions if it isn't the only emotion
    # Establish ranking of importance : combinaisons with state > State > combinaison > eyes > eyebrows > mouth. ONLY KEEP ONE EMOTIONAL TAG
    EMOTIONS = {
        'eyes': {
            'e': '[neutral]',
            'w': '[surprised]',
            's': '[excited]',
            't': '[smug]',
            'c': '[crazed]',
            'h': '[happy]',
            'r': '[pensive]',
            'l': '[pensive]',
            'd': '[sad]',
            'k': '[playful]',
            'n': '[playful]',
            'f': '[gentle]',
            'm': '[smug]',
            'g': '[smug]'
        },
        'eyebrows': {
            'f': '[intense]',
            'u': '[interested]',
            'k': '[worried]',
            't': '[thoughtful]'
        },
        'states': {
            'bl': '[blushing]',
            'bs': '[blushing]',
            'bf': '[intense blushing]',
            'ts': '[crying]',
            'td': '[dried tears]',
            'tp': '[holding back tears]',
            'tu': '[crying]'
        },
        'mouth': {
            'a': '[happy]',
            'b': '[cheerful]',
            'c': '[neutral]',
            'd': '[interested]',
            'o': '[surprised]',
            'u': '[smug]',
            'w': '[excited]',
            'x': '[angry]',
            'p': '[pouty]',
            't': '[playful]',
            'g': '[disgusted]'
        }
    }
    
    # Process in order: eyes, eyebrows, states, mouth
    if len(sprite_code) > 0 and sprite_code[0] in EMOTIONS['eyes']:
        emotions.add(EMOTIONS['eyes'][sprite_code[0]])
    
    if len(sprite_code) > 1 and sprite_code[1] in EMOTIONS['eyebrows']:
        emotions.add(EMOTIONS['eyebrows'][sprite_code[1]])
    
    # Check for two-character states
    for state in EMOTIONS['states']:
        if state in sprite_code:
            emotions.add(EMOTIONS['states'][state])
    
    if len(sprite_code) > 0 and sprite_code[-1] in EMOTIONS['mouth']:
        emotions.add(EMOTIONS['mouth'][sprite_code[-1]])
            
    return ' '.join(sorted(emotions))

def extract_dialogue(content):
    """Extract dialogue as sequential exchanges with emotions."""
    lines = content.split('\n')
    dialogue = []
    current_metadata = None
    in_dialogue = False
    choice_stack = []  # Track choice nesting
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Handle event definitions
        if 'addEvent(' in line:
            event_data, end_index = parse_event_data(content, i)
            if event_data:
                current_metadata = format_metadata(event_data)
                if current_metadata:
                    if in_dialogue:
                        dialogue.append("\n---\n")  # Add separator between topics
                    dialogue.append(current_metadata)
                    in_dialogue = True
            i = end_index + 1
            continue
        
        # Handle menu/choice sections
        # TO DO : Better this. I think the idea of ===Alternative paths=== is probably good
        elif line.strip() == "menu:":
            choice_stack.append([])
        
        # Handle choice options
        elif choice_stack and line.startswith('"'):
            choice_text = line.strip('":')
            choice_text = clean_dialogue(choice_text)
            
            # Start a new choice path
            if choice_stack[-1]:  # If not the first choice in this menu
                dialogue.append("\n=== Alternative Path ===\n")
            
            dialogue.append(f"Human: {choice_text}")
            choice_stack[-1].append(choice_text)
        
        # Handle dialogue lines
        elif 'm ' in line and '"' in line:
            try:
                sprite_match = re.search(r'm\s+\d([a-zA-Z]+)', line)
                dialogue_match = re.search(r'm [^"]*"([^"]*)"', line)
                
                if dialogue_match:
                    text = clean_dialogue(dialogue_match.group(1))
                    emotion = get_emotion(sprite_match.group(1)) if sprite_match else ""
                    
                    if text:
                        formatted_line = f"Assistant: {emotion} {text}" if emotion else f"Assistant: {text}"
                        dialogue.append(formatted_line)
            except Exception as e:
                print(f"Error processing dialogue line: {str(e)}")
        
        # Handle end of menu section
        elif line.startswith('return') and choice_stack:
            choice_stack.pop()
        
        i += 1
    
    # Clean up output by removing unnecessary alternative path markers
    cleaned_dialogue = []
    for line in dialogue:
        if line.strip() == "=== Alternative Path ===" and \
           (not cleaned_dialogue or cleaned_dialogue[-1].strip() == "=== Alternative Path ==="):
            continue
        cleaned_dialogue.append(line)
    
    return cleaned_dialogue

def process_file(input_path, output_path):
    """Process a single .rpy file."""
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        dialogue = extract_dialogue(content)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for line in dialogue:
                f.write(f"{line}\n")
                
    except Exception as e:
        print(f"Error processing {input_path}: {str(e)}")

def process_folder(input_folder, output_folder):
    """Process all .rpy files in a folder and combine outputs."""
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    
    all_dialogue = []
    
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.rpy'):
                input_path = os.path.join(root, file)
                print(f"Processing {input_path}...")
                
                try:
                    with open(input_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    dialogue_lines = extract_dialogue(content)
                    
                    # Save individual file
                    output_path = os.path.join(output_folder, file.replace('.rpy', '_dialogue.txt'))
                    with open(output_path, 'w', encoding='utf-8') as f:
                        for line in dialogue_lines:
                            f.write(f"{line}\n")
                    
                    # Add to combined output with separator
                    if dialogue_lines:  # Only add non-empty dialogues
                        if all_dialogue:  # Add separator if not first file
                            all_dialogue.append("\n\n=== New Topic ===\n\n")
                        all_dialogue.extend(dialogue_lines)
                    
                    print(f"Successfully processed {file}")
                    
                except Exception as e:
                    print(f"Error processing {file}: {str(e)}")
    
    # Save combined output
    if all_dialogue:
        combined_path = os.path.join(output_folder, "monika-database.txt")
        with open(combined_path, 'w', encoding='utf-8') as f:
            for line in all_dialogue:
                f.write(f"{line}\n")
        
        print(f"\nCreated combined database at {combined_path}")
    
    print("\nProcessing complete!")

if __name__ == "__main__":
    input_folder = "rpy_files"
    output_folder = "dialogue_output"
    process_folder(input_folder, output_folder)