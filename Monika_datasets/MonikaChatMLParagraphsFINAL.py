import re
import os
import json
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
        
        # Define emotion combinations
        self.EMOTION_COMBINATIONS = {
            frozenset(['happy', 'worried']): 'awkward',
            frozenset(['crying', 'happy']): 'joyfully crying',
            frozenset(['surprised', 'angry']): 'outraged',
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

        # Define emotion intensities
        self.EMOTION_INTENSITIES = {
            #High intensity combos
            'joyfully crying': 5,
            'furious tears': 5,
            'revolted': 5,
            'appalled': 5,
            'furious': 5,
            'melancholic': 5,
            'exuberant': 5,
            
            # Highest intensity emotions
            'angry': 4,
            'outraged': 4,
            'intense': 4,
            'holding back tears': 4,
            'enthusiastic': 4,
            'eager': 4,
            'bashful': 4,
            'dried tears': 4,
            'teasing': 4,
            
            # Medium-high intensity emotions
            'bittersweet': 3,
            'excited': 3,
            'happy': 3,
            'sad': 3,
            'worried': 3,
            'crying': 3,
            'mischievous': 3,
            'serene': 3,
            'somber': 3,
            'intense blushing': 3,
            
            # Medium intensity emotions
            'surprised': 2,
            'thoughtful': 2,
            'smug': 2,
            'playful': 2,
            'blushing': 2,
            'awkward': 2,
            'contemplative': 2,
            
            # Base intensity emotions
            'neutral': 1,
            'gentle': 1,
            'pensive': 1,
            'interested': 1,
            'cheerful': 1
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

    def format_to_chatml(self, dialogue_entries):
        """Convert dialogue entries to ChatML format."""
        grouped_entries = self.group_dialogue_entries(dialogue_entries)
        formatted_data = []
        prev_assistant_msg = None
        
        # Prepare initial metadata string
        metadata_lines = []
        if self.current_metadata:
            metadata_lines.append("Metadata:")
            for key, value in self.current_metadata.items():
                metadata_lines.append(f"- {key}: {value}")
        
        current_conversation = {
            "instruction": "",
            "emotions": [],
            "assistant_lines": []
        }
        
        for entry in grouped_entries:
            if entry['type'] == 'assistant':
                if entry.get('emotions'):
                    current_conversation["emotions"].extend(entry['emotions'])
                current_conversation["assistant_lines"].append(entry['text'])
                
            elif entry['type'] == 'user':
                # If we have a previous conversation, save it
                if current_conversation["assistant_lines"]:
                    # Create the system message with metadata, emotions and previous message if it exists
                    system_lines = metadata_lines.copy()
                    if current_conversation["emotions"]:
                        system_lines.append(f"Emotions of assistant: {current_conversation['emotions']}")
                    if prev_assistant_msg and entry['type'] == 'user':
                        system_lines.append(f"Previous assistant message: \"{prev_assistant_msg}\"")
                    
                    # Format the complete output with system context and assistant response
                    output = f"<|im_start|>system\n{chr(10).join(system_lines)}\n<|im_end|>\n"
                    # Store this message as previous for next iteration
                    if current_conversation["assistant_lines"]:
                        prev_assistant_msg = current_conversation["assistant_lines"][-1]
                    output += f"<|im_start|>assistant\n{chr(10).join(current_conversation['assistant_lines'])}\n<|im_end|>"
                    
                    # Add the previous conversation to formatted data
                    formatted_data.append({
                        "instruction": current_conversation["instruction"] if current_conversation["instruction"] else "*idling*",
                        "output": output
                    })
                
                # Start new conversation
                current_conversation = {
                    "instruction": entry['text'],
                    "emotions": [],
                    "assistant_lines": []
                }
        
        # Don't forget the last conversation
        if current_conversation["assistant_lines"]:
            system_lines = metadata_lines.copy()
            if current_conversation["emotions"]:
                system_lines.append(f"Emotions of assistant: {current_conversation['emotions']}")
            
            output = f"<|im_start|>system\n{chr(10).join(system_lines)}\n<|im_end|>\n"
            output += f"<|im_start|>assistant\n{chr(10).join(current_conversation['assistant_lines'])}\n<|im_end|>"
            
            formatted_data.append({
                "instruction": current_conversation["instruction"] if current_conversation["instruction"] else "*idling*",
                "output": output
            })
        
        return formatted_data

        
    def aggregate_emotions(self, emotion_lists):
        """
        Aggregate emotions from multiple consecutive messages into a single emotion set.
        Uses frequency and intensity-based weighting.
        """
        # Flatten all emotion lists
        all_emotions = [e for sublist in emotion_lists for e in sublist]
        
        # Count frequency of each emotion
        emotion_counts = {}
        for emotion in all_emotions:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            
        # Calculate weighted scores
        emotion_scores = {}
        for emotion, count in emotion_counts.items():
            intensity = self.EMOTION_INTENSITIES.get(emotion, 1)  # Default to 1 if not found
            emotion_scores[emotion] = count * intensity
            
        # Select dominant emotions (top 2 if they exist)
        dominant_emotions = sorted(
            emotion_scores.items(),
            key=lambda x: (x[1], self.EMOTION_INTENSITIES.get(x[0], 0)),
            reverse=True
        )
        
        # Return top emotions, or ['neutral'] if none found
        return [e[0] for e in dominant_emotions[:2]] if dominant_emotions else ['neutral']
    
    def group_dialogue_entries(self, entries):
        """Group consecutive assistant messages together."""
        grouped_entries = []
        current_group = None
        current_emotions = []
        
        for entry in entries:
            if entry['type'] == 'assistant':
                # Start or continue a group
                if current_group is None:
                    current_group = {
                        'type': 'assistant',
                        'text': entry['text'],
                        'emotions': []
                    }
                    current_emotions = [entry.get('emotions', ['neutral'])]
                else:
                    current_group['text'] += '\n' + entry['text']
                    current_emotions.append(entry.get('emotions', ['neutral']))
            else:  # User message or other type
                # Finish current group if it exists
                if current_group is not None:
                    current_group['emotions'] = self.aggregate_emotions(current_emotions)
                    grouped_entries.append(current_group)
                    current_group = None
                    current_emotions = []
                grouped_entries.append(entry)
        
        # Don't forget the last group
        if current_group is not None:
            current_group['emotions'] = self.aggregate_emotions(current_emotions)
            grouped_entries.append(current_group)
        
        return grouped_entries
    
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
        formatted_data = extractor.format_to_chatml(dialogue_entries)
        
        # Write as a proper JSON file with a list of conversations
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(formatted_data, f, indent=2, ensure_ascii=False)
            
        logging.info(f"Successfully processed {input_path}")
            
    except Exception as e:
        logging.error(f"Error processing {input_path}: {str(e)}")

def process_folder(input_folder: str, output_folder: str):
    """Process all .rpy files in a folder and create both individual and combined outputs."""
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    
    # List to store all dialogue data
    all_dialogues = []
    
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.rpy'):
                input_path = os.path.join(root, file)
                individual_output_path = os.path.join(
                    output_folder, 
                    file.replace('.rpy', '_dialogue.json')
                )
                
                try:
                    # Process individual file
                    with open(input_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    extractor = DialogueExtractor()
                    dialogue_entries = extractor.extract_dialogue(content)
                    formatted_data = extractor.format_to_chatml(dialogue_entries)
                    
                    # Write individual file
                    with open(individual_output_path, 'w', encoding='utf-8') as f:
                        json.dump(formatted_data, f, indent=2, ensure_ascii=False)
                    
                    # Add to combined data
                    all_dialogues.extend(formatted_data)
                    
                    logging.info(f"Successfully processed {input_path}")
                    
                except Exception as e:
                    logging.error(f"Error processing {input_path}: {str(e)}")
    
    # Write combined output
    combined_output_path = os.path.join(output_folder, "MoniDatabaseChatMLParagraphs.json")
    try:
        with open(combined_output_path, 'w', encoding='utf-8') as f:
            json.dump(all_dialogues, f, indent=2, ensure_ascii=False)
        logging.info(f"Successfully created combined output at {combined_output_path}")
    except Exception as e:
        logging.error(f"Error creating combined output: {str(e)}")

if __name__ == "__main__":
    input_folder = "rpy_files"
    output_folder = "dialogue_output"
    process_folder(input_folder, output_folder)