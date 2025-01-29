import re
import os
from pathlib import Path
import logging
from typing import Dict, List, Optional, Tuple, Set

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dialogue_extraction.log'),
        logging.StreamHandler()
    ]
)

class DialogueExtractor:
    def __init__(self):
        self.current_metadata = {}
        # Define emotion mappings
        self.EMOTIONS = {
            'eyes': {
                'e': 'neutral',
                'w': 'surprised',
                's': 'excited',
                't': 'smug',
                'c': 'crazed',
                'h': 'happy',
                'r': 'pensive',
                'l': 'pensive',
                'd': 'sad',
                'k': 'playful',
                'n': 'playful',
                'f': 'gentle',
                'm': 'smug',
                'g': 'smug'
            },
            'eyebrows': {
                'f': 'intense',
                'u': 'interested',
                'k': 'worried',
                't': 'thoughtful'
            },
            'states': {
                'bl': 'blushing',
                'bs': 'blushing',
                'bf': 'intense blushing',
                'ts': 'crying',
                'td': 'dried tears',
                'tp': 'holding back tears',
                'tu': 'crying'
            },
            'mouth': {
                'a': 'happy',
                'b': 'cheerful',
                'c': 'neutral',
                'd': 'interested',
                'o': 'surprised',
                'u': 'smug',
                'w': 'excited',
                'x': 'angry',
                'p': 'pouty',
                't': 'playful',
                'g': 'disgusted'
            }
        }
        
        # Define emotion combinations that create new states
        self.EMOTION_COMBINATIONS = {
            frozenset(['happy', 'worried']): 'awkward',
            frozenset(['crying', 'happy']): 'joyfully crying',
            frozenset(['surprised', 'angry']): 'shocked',
            frozenset(['happy', 'sad']): 'bittersweet',
            frozenset(['excited', 'playful']): 'enthusiastic',
            frozenset(['sad', 'thoughtful']): 'melancholic',
            frozenset(['disgusted', 'angry']): 'revolted',
            frozenset(['smug', 'playful']): 'teasing',
            frozenset(['blushing', 'happy']): 'bashful',
            frozenset(['intense', 'angry']): 'furious',
            frozenset(['pensive', 'sad']): 'somber',
            frozenset(['interested', 'excited']): 'eager',
            frozenset(['playful', 'surprised']): 'mischievous',
            frozenset(['crying', 'angry']): 'furious tears',
            frozenset(['neutral', 'pensive']): 'contemplative',
            frozenset(['cheerful', 'excited']): 'exuberant',
            frozenset(['gentle', 'happy']): 'serene',
            frozenset(['thoughtful', 'worried']): 'concerned',
            frozenset(['disgusted', 'surprised']): 'appalled'
        }

    def get_emotions(self, sprite_code: str) -> List[str]:
        """Extract highest priority emotion from sprite code."""
        if not sprite_code:
            return ['neutral']

        # Step 1: Collect all present emotions
        emotions = set()
        state_emotions = set()
        eye_emotions = set()
        mouth_emotions = set()
        eyebrow_emotions = set()
        
        # Process eyes
        if sprite_code and sprite_code[0] in self.EMOTIONS['eyes']:
            eye_emotions.add(self.EMOTIONS['eyes'][sprite_code[0]])
        
        # Process eyebrows
        if len(sprite_code) > 1 and sprite_code[1] in self.EMOTIONS['eyebrows']:
            eyebrow_emotions.add(self.EMOTIONS['eyebrows'][sprite_code[1]])
        
        # Process states
        for state in self.EMOTIONS['states']:
            if state in sprite_code:
                state_emotions.add(self.EMOTIONS['states'][state])
        
        # Process mouth
        if sprite_code and sprite_code[-1] in self.EMOTIONS['mouth']:
            mouth_emotions.add(self.EMOTIONS['mouth'][sprite_code[-1]])

        # Combine all emotions for combination checking
        emotions = emotions.union(state_emotions, eye_emotions, mouth_emotions, eyebrow_emotions)

        # Step 2: Check for combinations
        combinations_present = []
        for combo in self.EMOTION_COMBINATIONS:
            if all(emotion in emotions for emotion in combo):
                # If this combination includes a state emotion
                if any(emotion in state_emotions for emotion in combo):
                    return [self.EMOTION_COMBINATIONS[combo]]  # Highest priority: state-including combination
                combinations_present.append(self.EMOTION_COMBINATIONS[combo])
        
        # If we found any non-state combinations
        if combinations_present:
            return [combinations_present[0]]  # Return first non-state combination
        
        # Step 3: Return single highest priority emotion
        if state_emotions:
            return [next(iter(state_emotions))]  # Return first state emotion
        if eye_emotions:
            return [next(iter(eye_emotions))]    # Return first eye emotion
        if mouth_emotions:
            return [next(iter(mouth_emotions))]  # Return first mouth emotion
        if eyebrow_emotions:
            return [next(iter(eyebrow_emotions))]# Return first eyebrow emotion
        
        return ['neutral']  # Default emotion if none found

    def clean_dialogue(self, text: str) -> str:
        """Clean and standardize dialogue text."""
        try:
            text = re.sub(r'\[player\]', '<USER>', text, flags=re.IGNORECASE)
            text = re.sub(r'\[m_name\]', '<MONIKA>', text, flags=re.IGNORECASE)
            text = re.sub(r'\{.*?\}', '', text)  # Remove timing tags
            text = re.sub(r'\(.*?\)', '', text)  # Remove parentheses
            text = re.sub(r'\w{50,}', '', text)  # Remove very long words
            text = re.sub(r'\s*([?.!,])\s*', r'\1 ', text)  # Fix spacing around punctuation
            text = re.sub(r'~', '', text)
            text = re.sub(r'\s{2,}', ' ', text)
            text = re.sub(r'\s+([?.!,])', r'\1', text)  # Remove space before punctuation
            return text.strip()
        except Exception as e:
            logging.error(f"Error in clean_dialogue: {str(e)}")
            return text

    def parse_event_metadata(self, content: str, start_index: int) -> Tuple[Dict, int]:
        """Extract event metadata from event definition."""
        logging.debug(f"Parsing event metadata starting at line {start_index}")
        metadata = {}
        lines = content.split('\n')
        
        # Look for event definition end
        end_index = start_index
        try:
            while end_index < len(lines) and not lines[end_index].strip().endswith(')'):
                end_index += 1
            
            # Combine lines into single string for parsing
            event_def = ' '.join(lines[start_index:end_index+1])
            
            # Extract components
            label_match = re.search(r'eventlabel=["\']([^"\']+)["\']', event_def)
            if label_match:
                metadata['eventlabel'] = label_match.group(1)
            
            category_match = re.search(r'category=\[(.*?)\]', event_def)
            if category_match:
                categories = re.findall(r'["\']([^"\']+)["\']', category_match.group(1))
                metadata['categories'] = categories
            
            prompt_match = re.search(r'prompt=["\']([^"\']+)["\']', event_def)
            if prompt_match:
                metadata['prompt'] = prompt_match.group(1)

            # Extract other possible metadata
            for field in ['random', 'pool', 'unlocked']:
                if f'{field}=True' in event_def:
                    metadata[field] = True
                    
            logging.debug(f"Extracted metadata: {metadata}")
            
        except Exception as e:
            logging.error(f"Error parsing event metadata: {str(e)}")
            
        return metadata, end_index

    def format_to_chatml(self, dialogue_entries: List[Dict]) -> str:
        """Convert dialogue entries to ChatML format."""
        output = []
        prev_assistant_msg = None
        
        # Add initial metadata if available
        if self.current_metadata:
            output.append("<|im_start|>system")
            output.append("Metadata:")
            for key, value in self.current_metadata.items():
                output.append(f"- {key}: {value}")
            output.append("<|im_end|>\n")
        
        for i, entry in enumerate(dialogue_entries):
            if entry.get('type') == 'assistant':
                # Add system context for emotions and/or previous message
                if entry.get('emotions') or (i > 0 and dialogue_entries[i-1].get('type') == 'user'):
                    output.append("<|im_start|>system")
                    
                    # Add emotions if present
                    if entry.get('emotions'):
                        output.append(f"Emotions of the assistant: {entry['emotions']}")
                    
                    # Add previous message context if this follows a user input
                    if i > 0 and dialogue_entries[i-1].get('type') == 'user':
                        if prev_assistant_msg:
                            output.append(f'Previous assistant message: "{prev_assistant_msg}"')
                    
                    output.append("<|im_end|>")
                
                # Add assistant message
                output.append("<|im_start|>assistant")
                output.append(entry['text'])
                output.append("<|im_end|>")
                prev_assistant_msg = entry['text']
                
            elif entry.get('type') == 'user':
                output.append("<|im_start|>user")
                output.append(entry['text'])
                output.append("<|im_end|>")
        
        return '\n'.join(output)

    def extract_dialogue(self, content: str) -> List[Dict]:
        """Extract dialogue as sequential exchanges."""
        logging.info("Starting dialogue extraction")
        lines = content.split('\n')
        dialogue_entries = []
        choice_stack = []
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            try:
                # Handle event definitions
                if 'addEvent(' in line:
                    logging.debug(f"Found event definition at line {i}")
                    metadata, end_index = self.parse_event_metadata(content, i)
                    self.current_metadata = metadata
                    i = end_index + 1
                    continue
                
                # Handle menu/choice sections
                elif line.strip() == "menu:":
                    choice_stack.append([])
                    logging.debug("Found menu section")
                
                # Handle choice options
                elif choice_stack and line.startswith('"'):
                    choice_text = line.strip('":')
                    choice_text = self.clean_dialogue(choice_text)
                    dialogue_entries.append({
                        'type': 'user',
                        'text': choice_text
                    })
                    choice_stack[-1].append(choice_text)
                    logging.debug(f"Added choice: {choice_text}")
                
                # Handle Monika's dialogue
                elif 'm ' in line and '"' in line:
                    sprite_match = re.search(r'm\s+\d([a-zA-Z]+)', line)
                    dialogue_match = re.search(r'm [^"]*"([^"]*)"', line)
                    
                    if dialogue_match:
                        text = self.clean_dialogue(dialogue_match.group(1))
                        emotions = []
                        if sprite_match:
                            sprite_code = sprite_match.group(1)
                            emotions = self.get_emotions(sprite_code)
                        else:
                            emotions = ['neutral']
                        
                        dialogue_entries.append({
                            'type': 'assistant',
                            'text': text,
                            'emotions': emotions
                        })
                        logging.debug(f"Added assistant dialogue: {text}")
                
                # Handle end of menu section
                elif line.startswith('return') and choice_stack:
                    choice_stack.pop()
                    logging.debug("End of menu section")
                
            except Exception as e:
                logging.error(f"Error processing line {i}: {str(e)}")
                logging.error(f"Line content: {line}")
            
            i += 1
        
        return dialogue_entries

def process_file(input_path: str, output_path: str):
    """Process a single .rpy file."""
    logging.info(f"Processing file: {input_path}")
    extractor = DialogueExtractor()
    
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        dialogue_entries = extractor.extract_dialogue(content)
        formatted_dialogue = extractor.format_to_chatml(dialogue_entries)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(formatted_dialogue)
            
        logging.info(f"Successfully processed {input_path}")
            
    except Exception as e:
        logging.error(f"Error processing {input_path}: {str(e)}")

def process_folder(input_folder: str, output_folder: str):
    """Process all .rpy files in a folder."""
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.rpy'):
                input_path = os.path.join(root, file)
                output_path = os.path.join(
                    output_folder, 
                    file.replace('.rpy', '_dialogue.txt')
                )
                process_file(input_path, output_path)

if __name__ == "__main__":
    input_folder = "rpy_files"
    output_folder = "dialogue_output"
    process_folder(input_folder, output_folder)