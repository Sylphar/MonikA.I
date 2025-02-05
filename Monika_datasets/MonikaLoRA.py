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
# Helper: Count the indentation (leading spaces or tabs)
def count_indent(line: str) -> int:
    """Return the number of leading whitespace characters."""
    return len(line) - len(line.lstrip(' \t'))

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
        pass
        
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
            #Direct replacements
            text = re.sub(r'\[player\]', '<USER>', text, flags=re.IGNORECASE)
            text = re.sub(r'\[p_nickname\]', 'my love', text, flags=re.IGNORECASE)
            text = re.sub(r'\[mas_get_player_nickname\(.*?\)\]', 'my love', text)
            text = re.sub(r'\[bf\]', 'boyfriend', text)
            text = re.sub(r'\[m_name\]', '<MONIKA>', text, flags=re.IGNORECASE)
            
            #Formatting
            text = re.sub(r'\{i\}(.*?)\{/i\}', r'_\1_', text)  # Italics → _text_
            text = re.sub(r'\{b\}(.*?)\{/b\}', r'**\1**', text)  # Bold → **text**
            text = re.sub(r'\{s\}(.*?)\{/s\}', r'~~\1~~', text)  # Strikethrough → ~~text~~
            text = re.sub(r'\{u\}(.*?)\{/u\}', r'<u>\1</u>', text)  # Underline → <u>text</u>
            
            #timing tags
            text = re.sub(r'\{w=[^}]*\}', '', text)  # {w=...}
            text = re.sub(r'\{nw\}', '', text)       # {nw}
            text = re.sub(r'\{fast\}', '', text)     # {fast}
            text = re.sub(r'\{w\}', '', text)        # {w}
            text = re.sub(r'\[_and\]', '', text)     # [_and]
            
            #Other small cases
            text = re.sub(r'\(.*?\)', '', text)  # Remove parentheses
            text = re.sub(r'\w{50,}', '', text)  # Remove very long words
            text = re.sub(r'\s*([?.!,])\s*', r'\1 ', text)  # Fix spacing around punctuation
            text = re.sub(r'~', '', text)
            text = re.sub(r'\s{2,}', ' ', text)
            text = re.sub(r'\{alt\}.*?\{/alt\}', '', text, flags=re.DOTALL) # Remove {alt} alternative text blocks entirely
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

    def format_to_chatml(self, dialogue_entries: List[Dict]) -> List[Dict]:
        """
        Group dialogue entries into conversation blocks and format them as ChatML.
        Each conversation block is separated by a 'separator' entry.
        For a user message, if it has a branch_context, store it temporarily and apply it to the next assistant block.
        """
        formatted_data = []
        current_conversation = {"system": "", "instruction": "", "output": ""}
        system_set = False
        temp_branch_context = None  # Store the previous assistant message for the NEXT assistant block

        for entry in dialogue_entries:
            if entry['type'] == "separator":
                if current_conversation["output"]:
                    formatted_data.append(current_conversation)
                    logging.debug(f"Conversation block finished with system: {current_conversation['system']}")
                current_conversation = {"system": "", "instruction": "", "output": ""}
                system_set = False
                temp_branch_context = None  # Reset stored branch context
                continue

            if entry['type'] == 'assistant':
                if not system_set:
                    system_parts = []
                    if entry.get('metadata'):
                        system_parts.append("Metadata = " + str(entry['metadata']))
                    if entry.get('emotions'):
                        system_parts.append("Emotions of the assistant: " + str(entry['emotions']))
                    if temp_branch_context:  # Apply the stored previous assistant message
                        system_parts.append(f"Previous assistant message: \"{temp_branch_context}\"")
                        temp_branch_context = None  # Clear after applying
                    current_conversation["system"] = "\n".join(system_parts)
                    system_set = True
                if current_conversation["output"]:
                    current_conversation["output"] += "\n"
                current_conversation["output"] += entry["text"]

            elif entry['type'] == 'user':
                # Store the branch_context temporarily for the next assistant block
                if entry.get("branch_context"):
                    temp_branch_context = entry["branch_context"]

                if current_conversation["output"]:
                    formatted_data.append(current_conversation)
                current_conversation = {"system": "", "instruction": entry["text"], "output": ""}
                system_set = False

        if current_conversation["output"]:
            formatted_data.append(current_conversation)
            logging.debug(f"Final conversation block added with system: {current_conversation['system']}")

        return formatted_data


    def create_continuation_instruction(self, prev_messages):
        """Create instruction for continuation points."""
        if not prev_messages:
            return "*continuation*"
        
        # Take last 100 chars of each message
        truncated_msgs = [msg[-100:] for msg in prev_messages]
        return f"Create a common continuation to these dialogue bits: {', '.join(truncated_msgs)}"
        
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
        """
        Extract dialogue entries from the Ren'Py file.
        A new conversation block is forced whenever a new event is encountered.
        In each conversation block, only the first assistant message gets metadata.
        Additionally, for each user choice line, we record the branch context (the last assistant message trimmed to 150 characters)
        using indentation levels.
        """
        logging.info("Starting dialogue extraction")
        lines = content.split('\n')
        dialogue_entries = []
        # branch_stack: each element is a tuple (indent_level, branch_context)
        branch_stack = []
        current_metadata = None
        in_dialogue = False
        metadata_attached = False  # Flag: whether metadata has been attached in the current conversation block
        last_assistant_msg = ""    # Holds the full text of the most recent assistant message

        i = 0
        while i < len(lines):
            line = lines[i]
            stripped_line = line.strip()
            try:
                # --- Detect start of a new dialogue event ---
                if 'init 5 python:' in stripped_line:
                    # If already inside a dialogue block, insert a separator entry.
                    if in_dialogue:
                        dialogue_entries.append({"type": "separator"})
                        logging.debug("Inserted conversation separator before new event")
                    # Look ahead for an addEvent call to extract metadata.
                    j = i + 1
                    found_event = False
                    while j < min(i + 10, len(lines)):
                        if 'addEvent(' in lines[j]:
                            metadata, end_index = self.parse_event_metadata(content, j)
                            current_metadata = metadata.copy()
                            in_dialogue = True
                            metadata_attached = False  # Reset for new conversation block
                            branch_stack = []  # Reset branch contexts
                            last_assistant_msg = ""
                            logging.debug(f"NEW CONVERSATION STARTED - Metadata: {current_metadata}")
                            found_event = True
                            i = end_index  # Skip metadata definition lines
                            break
                        j += 1
                    if found_event:
                        i += 1
                        continue

                # --- Detect end of dialogue section ---
                if (('init' in stripped_line and 'python' in stripped_line and in_dialogue) or ('return "derandom"' in stripped_line)):
                    logging.debug("ENDING CONVERSATION - Resetting metadata and branch stack")
                    in_dialogue = False
                    current_metadata = None
                    metadata_attached = False
                    branch_stack = []
                    i += 1
                    continue

                # --- Process lines if inside a dialogue section ---
                if in_dialogue:
                    # When we encounter a menu marker (this line alone may not change branch context)
                    if stripped_line == "menu:":
                        logging.debug("MENU DETECTED")
                        # (We don’t push anything yet; we'll use the first option line below.)
                        
                    # Process a user choice line (one that starts with a quotation mark)
                    elif stripped_line.startswith('"'):
                        current_indent = count_indent(line)
                        # Manage the branch stack using the indentation level.
                        if not branch_stack:
                            branch_context = last_assistant_msg[-150:] if last_assistant_msg else ""
                            branch_stack.append((current_indent, branch_context))
                            logging.debug(f"Branch stack empty. Pushed: {(current_indent, branch_context)}")
                        else:
                            top_indent, top_context = branch_stack[-1]
                            if current_indent > top_indent:
                                # Entering a nested branch: push the new context.
                                branch_context = last_assistant_msg[-150:] if last_assistant_msg else ""
                                branch_stack.append((current_indent, branch_context))
                                logging.debug(f"Nested branch detected. Pushed: {(current_indent, branch_context)}")
                            elif current_indent < top_indent:
                                # Exiting one or more nested branches.
                                while branch_stack and branch_stack[-1][0] > current_indent:
                                    popped = branch_stack.pop()
                                    logging.debug(f"Popped branch context: {popped}")
                                if branch_stack:
                                    branch_context = branch_stack[-1][1]
                                else:
                                    branch_context = last_assistant_msg[-150:] if last_assistant_msg else ""
                                    branch_stack.append((current_indent, branch_context))
                            else:
                                # current_indent == top_indent; same level: update the context.
                                branch_context = last_assistant_msg[-150:] if last_assistant_msg else ""
                                branch_stack[-1] = (current_indent, branch_context)
                        # Append the user choice entry with the current branch context.
                        choice_text = self.clean_dialogue(stripped_line.strip('":'))
                        dialogue_entries.append({
                            'type': 'user',
                            'text': choice_text,
                            'branch_context': branch_context,
                            'metadata': current_metadata if not metadata_attached else None
                        })
                        logging.debug(f"CHOICE ADDED: {choice_text} with branch context: {branch_context}")

                    # Process an assistant dialogue line (look for a line starting with 'm ' or 'extend' and containing quoted text)
                    elif ('m ' in stripped_line and '"' in stripped_line) or ('extend ' in stripped_line and '"' in stripped_line):
                        sprite_match = re.search(r'm\s+\d([a-zA-Z]+)', stripped_line)
                        dialogue_match = re.search(r'm [^"]*"([^"]*)"', stripped_line)
                        if dialogue_match:
                            text = self.clean_dialogue(dialogue_match.group(1))
                            last_assistant_msg = text  # Update the current assistant message
                            if sprite_match:
                                sprite_code = sprite_match.group(1)
                                emotions = self.get_emotions(sprite_code)
                            else:
                                emotions = ['neutral']
                            entry = {
                                'type': 'assistant',
                                'text': text,
                                'emotions': emotions,
                                'metadata': current_metadata if not metadata_attached else None
                            }
                            dialogue_entries.append(entry)
                            logging.debug(f"ASSISTANT LINE ADDED: {text} - Metadata: {entry['metadata']}")
                            if not metadata_attached:
                                logging.debug("Metadata attached to first message of this block")
                            metadata_attached = True

                    # If a menu ends, indicated by a 'return' line when a branch exists, pop the branch.
                    elif stripped_line.startswith('return') and branch_stack:
                        popped = branch_stack.pop()
                        logging.debug(f"MENU SECTION ENDED, popped branch context: {popped}")
            # End if in_dialogue
            # (Any other lines are ignored.)
            # End try
            except Exception as e:
                logging.error(f"Error processing line {i}: {str(e)}")
                logging.error(f"Line content: {line}")
            i += 1

        logging.debug(f"TOTAL DIALOGUE ENTRIES: {len(dialogue_entries)}")
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
