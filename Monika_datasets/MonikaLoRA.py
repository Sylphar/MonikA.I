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
        self.label_map = {}  # Maps label names to their dialogue content
        self.menu_map = {}   # Maps menu choices to their target labels
        
        
    def first_pass_scan(self, files_content: Dict[str, str]):
        """
        First pass: scan all files to build maps of labels and menus.
        
        Args:
            files_content: Dictionary mapping filenames to their content
        """
        for filename, content in files_content.items():
            lines = content.split('\n')
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                
                # Find labels and store their content
                if line.startswith('label '):
                    label_name = line[6:].split(':')[0].strip()
                    label_content = []
                    j = i + 1
                    while j < len(lines) and (lines[j].strip() == '' or count_indent(lines[j]) > count_indent(lines[i])):
                        if 'm ' in lines[j] and '"' in lines[j]:
                            label_content.append(lines[j])
                        j += 1
                    self.label_map[label_name] = {
                        'content': label_content,
                        'file': filename
                    }
                    i = j
                    continue
                
                # Find menu definitions
                elif line.startswith('python:'):
                    j = i + 1
                    while j < len(lines) and count_indent(lines[j]) > count_indent(lines[i]):
                        menu_line = lines[j].strip()
                        if '(' in menu_line and ')' in menu_line and '"' in menu_line:
                            choice_match = re.search(r'"([^"]+)".*?\'([^\']+)\'', menu_line)
                            if choice_match:
                                choice_text = self.clean_dialogue(choice_match.group(1))
                                target_label = choice_match.group(2)
                                self.menu_map[choice_text] = {
                                    'label': target_label,
                                    'file': filename
                                }
                        j += 1
                    i = j
                    continue
                
                i += 1
                
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
                    metadata = entry.get('metadata')
                    
                    # If the instruction is empty, try to fill it based on metadata.
                    if not current_conversation["instruction"]:
                        parsed_metadata = None
                        if metadata:
                            # If metadata is already a dict, use it directly; otherwise try parsing it.
                            if isinstance(metadata, dict):
                                parsed_metadata = metadata
                            else:
                                try:
                                    parsed_metadata = ast.literal_eval(metadata)
                                except Exception:
                                    parsed_metadata = None
                        # Now apply our fallback rules.
                        if parsed_metadata:
                            if parsed_metadata.get('prompt'):
                                current_conversation["instruction"] = f"Hey Monika, what do you have to say about: {parsed_metadata['prompt']}"
                            elif parsed_metadata.get('random') is True:
                                current_conversation["instruction"] = "*idling*"
                            else:
                                current_conversation["instruction"] = "Oh, I see, please continue."
                        else:
                            # No metadata available – default fallback.
                            current_conversation["instruction"] = "Oh, I see, please continue."
                    
                    # Build the system string.
                    if metadata:
                        system_parts.append("Metadata = " + str(metadata))
                    if entry.get('emotions'):
                        system_parts.append("Emotions of the assistant: " + str(entry['emotions']))
                    if temp_branch_context:  # Apply the stored previous assistant message.
                        system_parts.append(f"Previous assistant message: \"{temp_branch_context}\"")
                        temp_branch_context = None  # Clear after applying.
                    current_conversation["system"] = "\n".join(system_parts)
                    system_set = True

                # Append the assistant text to the conversation's output.
                if current_conversation["output"]:
                    current_conversation["output"] += "\n"
                current_conversation["output"] += entry["text"]

            elif entry['type'] == 'user':
                # Store the branch_context temporarily for the next assistant block.
                if entry.get("branch_context"):
                    temp_branch_context = entry["branch_context"]

                if current_conversation["output"]:
                    formatted_data.append(current_conversation)
                # Use the user's text as instruction. (If it is empty, our fallback above will later fill it in.)
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
    
    def extract_dialogue(self, content: str, filename: str) -> List[Dict]:
        """
        Extract dialogue entries from the Ren'Py file.
        Now handles both traditional event-based and label-based dialogue structures,
        while preserving proper menu branching.
        """
        logging.info(f"Starting dialogue extraction for {filename}")
        lines = content.split('\n')
        dialogue_entries = []
        current_metadata = None
        in_dialogue = False
        metadata_attached = False
        branch_stack = []  # Will now store tuples of (indent_level, context, last_assistant_msg)
        last_assistant_msg = ""
        current_indent_level = 0

        # Check file type
        has_init = any('init 5 python:' in line or 'init 6 python:' in line for line in lines)
        is_label_based = not has_init and any(line.strip().startswith('label ') for line in lines)

        i = 0
        while i < len(lines):
            line = lines[i]
            stripped_line = line.strip()

            try:
                # Handle traditional event-based dialogue
                if ('init 5 python:' in stripped_line or 'init 6 python:' in stripped_line):
                    if in_dialogue:
                        dialogue_entries.append({"type": "separator"})
                    
                    j = i + 1
                    found_event = False
                    while j < min(i + 10, len(lines)):
                        if 'addEvent(' in lines[j]:
                            metadata, end_index = self.parse_event_metadata(content, j)
                            current_metadata = metadata.copy()
                            in_dialogue = True
                            metadata_attached = False
                            branch_stack = []
                            last_assistant_msg = ""
                            found_event = True
                            i = end_index
                            break
                        j += 1
                    if found_event:
                        i += 1
                        continue

                # Handle label-based dialogue
                elif is_label_based and stripped_line.startswith('label '):
                    if in_dialogue:
                        dialogue_entries.append({"type": "separator"})
                    
                    label_name = stripped_line[6:].split(':')[0].strip()
                    current_metadata = {'eventlabel': label_name}
                    in_dialogue = True
                    metadata_attached = False
                    branch_stack = []
                    last_assistant_msg = ""

                # Handle Python block menus (cross-file references)
                elif stripped_line.startswith('python:'):
                    menu_data = []
                    j = i + 1
                    current_indent = count_indent(line)
                    
                    while j < len(lines) and count_indent(lines[j]) > current_indent:
                        menu_line = lines[j].strip()
                        if '(' in menu_line and ')' in menu_line and '"' in menu_line:
                            choice_match = re.search(r'"([^"]+)".*?\'([^\']+)\'', menu_line)
                            if choice_match:
                                choice_text = self.clean_dialogue(choice_match.group(1))
                                target_label = choice_match.group(2)
                                
                                # Create menu choice entry
                                menu_entry = {
                                    'type': 'user',
                                    'text': choice_text,
                                    'branch_context': last_assistant_msg[-150:] if last_assistant_msg else "",
                                    'metadata': current_metadata if not metadata_attached else None,
                                    'target_label': target_label
                                }
                                
                                if target_label in self.label_map:
                                    label_info = self.label_map[target_label]
                                    menu_entry['label_file'] = label_info['file']
                                    if label_info['file'] != filename:
                                        menu_entry['label_content'] = label_info['content']
                                
                                menu_data.append(menu_entry)
                        j += 1
                    dialogue_entries.extend(menu_data)
                    i = j
                    continue

                # Handle regular menu marker (When entering a menu)
                elif stripped_line == "menu:":
                    logging.debug("MENU DETECTED")
                    current_indent = count_indent(line)
                    if not branch_stack:
                        # First menu: use the last assistant message before the menu
                        branch_stack.append((current_indent, last_assistant_msg[-150:] if last_assistant_msg else "", last_assistant_msg))
                        logging.debug(f"Branch stack empty. Pushed: {current_indent}, context: {branch_stack[-1][1]}")

                # Handle menu choices (both in standard menus and Python blocks)
                elif stripped_line.startswith('"'):
                    current_indent = count_indent(line)
                    
                    if not branch_stack:
                        # Shouldn't happen, but handle it just in case
                        branch_stack.append((current_indent, last_assistant_msg[-150:] if last_assistant_msg else "", last_assistant_msg))
                        logging.debug(f"Branch stack empty. Pushed: {current_indent}, context: {branch_stack[-1][1]}")
                    else:
                        # Find the appropriate parent branch by looking at indentation
                        parent_branch = None
                        for branch in reversed(branch_stack):
                            if branch[0] < current_indent:
                                parent_branch = branch
                                break
                        
                        if parent_branch:
                            # Use the last assistant message from the parent branch as context
                            branch_context = parent_branch[2][-150:] if parent_branch[2] else ""
                            branch_stack.append((current_indent, branch_context, parent_branch[2]))
                            logging.debug(f"Nested branch detected. Parent indent: {parent_branch[0]}, Current indent: {current_indent}")
                            logging.debug(f"Using context from parent: {branch_context}")
                        else:
                            # No parent found (at root level)
                            branch_context = last_assistant_msg[-150:] if last_assistant_msg else ""
                            branch_stack.append((current_indent, branch_context, last_assistant_msg))
                    
                    choice_text = self.clean_dialogue(stripped_line.strip('":'))
                    # Use the context from the current branch's parent
                    parent_context = ""
                    for branch in reversed(branch_stack[:-1]):  # Exclude current branch
                        if branch[0] < current_indent:
                            parent_context = branch[2][-150:] if branch[2] else ""
                            break
                    if not parent_context and branch_stack:
                        parent_context = branch_stack[0][2][-150:] if branch_stack[0][2] else ""
                    
                    dialogue_entries.append({
                        'type': 'user',
                        'text': choice_text,
                        'branch_context': parent_context,
                        'metadata': current_metadata if not metadata_attached else None
                    })
                    logging.debug(f"CHOICE ADDED: {choice_text} with branch context: {parent_context}")

                # Handle Monika's dialogue
                elif ('m ' in stripped_line and '"' in stripped_line) or ('extend ' in stripped_line and '"' in stripped_line):
                    sprite_match = re.search(r'm\s+\d([a-zA-Z]+)', stripped_line)
                    dialogue_match = re.search(r'm [^"]*"([^"]*)"', stripped_line)
                    
                    if dialogue_match:
                        text = self.clean_dialogue(dialogue_match.group(1))
                        current_indent = count_indent(line)
                        
                        # Update the last assistant message for the current branch level
                        if branch_stack:
                            # Find the current branch based on indentation
                            current_branch = None
                            for branch in reversed(branch_stack):
                                if branch[0] < current_indent:
                                    current_branch = branch
                                    break
                            
                            if current_branch:
                                # Update the last assistant message for this branch
                                idx = branch_stack.index(current_branch)
                                branch_stack[idx] = (current_branch[0], current_branch[1], text)
                        
                        last_assistant_msg = text
                        
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
                        metadata_attached = True

                # Handle end of menu sections
                elif stripped_line.startswith('return') and branch_stack:
                    popped = branch_stack.pop()
                    logging.debug(f"Menu section ended, popped branch: {popped}")

            except Exception as e:
                logging.error(f"Error processing line {i} in {filename}: {str(e)}")
                logging.error(f"Line content: {line}")

            i += 1

        logging.debug(f"Extracted {len(dialogue_entries)} dialogue entries from {filename}")
        return dialogue_entries

    def process_files(self, input_files: List[str], output_folder: str):
        """
        Process multiple files with cross-file reference handling.
        """
        # First, read all files
        files_content = {}
        for input_file in input_files:
            with open(input_file, 'r', encoding='utf-8') as f:
                files_content[input_file] = f.read()
        
        # First pass: build maps
        self.first_pass_scan(files_content)
        
        # Second pass: process each file with access to the maps
        for input_file in input_files:
            output_path = os.path.join(
                output_folder,
                os.path.basename(input_file).replace('.rpy', '_dialogue.json')
            )
            
            dialogue_entries = self.extract_dialogue(files_content[input_file], input_file)
            formatted_data = self.format_to_chatml(dialogue_entries)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(formatted_data, f, indent=2, ensure_ascii=False)

def load_poems_json(file_path):
    """Read and parse a poems JSON file, ignoring lines starting with '#'."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line for line in f if not line.strip().startswith('#')]
            content = ''.join(lines)
            return json.loads(content)
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON in {file_path}: {str(e)}")
        return []
    except Exception as e:
        logging.error(f"Error loading {file_path}: {str(e)}")
        return []

def get_name_replacements():
    """Prompt the user for replacements for <MONIKA> and <USER>."""
    print("Please provide replacements for <MONIKA> and <USER>. Press Enter to keep defaults.")
    monika_name = input("Replace <MONIKA> with (default: <MONIKA>): ").strip() or "<MONIKA>"
    user_name = input("Replace <USER> with (default: <USER>): ").strip() or "<USER>"
    return monika_name, user_name

def fix_empty_instructions(output_folder: str):
    """
    Process all JSON files in the output folder to replace empty or invalid instructions
    with a default instruction.
    """
    import os
    import json
    import logging
    
    default_instruction = "Monika, what do you have to say today?"
    
    for filename in os.listdir(output_folder):
        if filename.endswith('_dialogue.json'):
            file_path = os.path.join(output_folder, filename)
            try:
                # Read the file
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace problematic instructions
                content = content.replace('"instruction": ""', f'"instruction": "{default_instruction}"')
                content = content.replace('"instruction": ")"', f'"instruction": "{default_instruction}"')
                
                # Write back to file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                logging.info(f"Successfully processed instructions in {filename}")
                
            except Exception as e:
                logging.error(f"Error processing {filename}: {str(e)}")

def process_folder(input_folder: str, output_folder: str):
    """Process all .rpy files in a folder with cross-file reference handling."""
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    
    # First, collect all file contents
    files_content = {}
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.rpy'):
                input_path = os.path.join(root, file)
                with open(input_path, 'r', encoding='utf-8') as f:
                    files_content[file] = f.read()
    
    # Create extractor and build the label map
    extractor = DialogueExtractor()
    extractor.first_pass_scan(files_content)
    
    # Process each file
    all_dialogues = []
    for file, content in files_content.items():
        individual_output_path = os.path.join(
            output_folder, 
            file.replace('.rpy', '_dialogue.json')
        )
        
        try:
            dialogue_entries = extractor.extract_dialogue(content, file)
            formatted_data = extractor.format_to_chatml(dialogue_entries)
            
            # Write with custom formatting
            with open(individual_output_path, 'w', encoding='utf-8') as f:
                f.write('[\n')
                for i, entry in enumerate(formatted_data):
                    f.write('\t{\n')
                    f.write(f'\t\t"system": {json.dumps(entry["system"], ensure_ascii=False)},\n')
                    f.write(f'\t\t"instruction": {json.dumps(entry["instruction"], ensure_ascii=False)},\n')
                    f.write(f'\t\t"output": {json.dumps(entry["output"], ensure_ascii=False)}\n')
                    f.write('\t}')
                    if i < len(formatted_data) - 1:
                        f.write(',')
                    f.write('\n')
                f.write(']')
            
            all_dialogues.extend(formatted_data)
            logging.info(f"Successfully processed {file}")
            
        except Exception as e:
            logging.error(f"Error processing {file}: {str(e)}")
    
    # Load poems JSON files
    poems_files = ["My poems.json", "MAS poems.json", "Base game poems.json"]
    for poems_file in poems_files:
        file_path = os.path.join(input_folder, poems_file)
        if os.path.exists(file_path):
            poems_data = load_poems_json(file_path)
            all_dialogues.extend(poems_data)
        else:
            logging.warning(f"Poems file {poems_file} not found in {input_folder}")
    
    # Get name replacements from user
    monika_name, user_name = get_name_replacements()
    
    # Apply replacements to all dialogue entries
    for entry in all_dialogues:
        for field in ["system", "instruction", "output"]:
            if monika_name != "<MONIKA>":
                entry[field] = entry[field].replace("<MONIKA>", monika_name)
            if user_name != "<USER>":
                entry[field] = entry[field].replace("<USER>", user_name)
    
    # Write combined output with same formatting
    combined_output_path = os.path.join(output_folder, "MoniDatasetLoRA.json")
    try:
        with open(combined_output_path, 'w', encoding='utf-8') as f:
            f.write('[\n')
            for i, entry in enumerate(all_dialogues):
                f.write('\t{\n')
                f.write(f'\t\t"system": {json.dumps(entry["system"], ensure_ascii=False)},\n')
                f.write(f'\t\t"instruction": {json.dumps(entry["instruction"], ensure_ascii=False)},\n')
                f.write(f'\t\t"output": {json.dumps(entry["output"], ensure_ascii=False)}\n')
                f.write('\t}')
                if i < len(all_dialogues) - 1:
                    f.write(',')
                f.write('\n')
            f.write(']')
        logging.info(f"Successfully created combined output at {combined_output_path}")
        
        # Add the new function call here
        fix_empty_instructions(output_folder)
        logging.info("Successfully processed all empty instructions")
        
    except Exception as e:
        logging.error(f"Error in final processing: {str(e)}")


if __name__ == "__main__":
    input_folder = "rpy_files"
    output_folder = "dialogue_output"
    process_folder(input_folder, output_folder)
