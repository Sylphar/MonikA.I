import os
import sys
import tkinter as tk
import json

# Configuration
args = sys.argv[1:]

root = tk.Tk()
root.title("MonikA.I. Submod")
root.geometry("900x500")

#colors
doki_white = "#F9F3F9"
doki_dark_pink = '#F9B7DB'
doki_light_pink = '#F4DCEA'
doki_purple = '#AB6999'
menu_background_pink = '#EC9DC8'

bg_image = tk.PhotoImage(file=r"images\login\login_background.png")
background_label = tk.Label(root, image=bg_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

def load_from_json(variable, entry):
    try:
        with open("config.json", "r") as file:
            config = json.load(file)
        variable_to_insert = config[variable]
        entry.delete(0, tk.END)
        entry.insert(0, variable_to_insert)
    except FileNotFoundError:
        pass

def get_input():
    global GAME_PATH
    global WEBUI_PATH
    global USE_TTS
    global LAUNCH_YOURSELF
    global LAUNCH_YOURSELF_WEBUI
    global USE_ACTIONS
    global TTS_MODEL
    global USE_SPEECH_RECOGNITION
    global VOICE_SAMPLE_TORTOISE
    global VOICE_SAMPLE_COQUI
    global VITS_SPEAKER
    global VITS_MODEL_PATH
    USE_TTS = use_tts.get()
    GAME_PATH = game_path.get()
    WEBUI_PATH = webui_path.get()
    LAUNCH_YOURSELF = launch_yourself.get()
    LAUNCH_YOURSELF_WEBUI = launch_yourself_webui.get()
    USE_ACTIONS = use_actions.get()
    TTS_MODEL = tts_model.get()
    USE_SPEECH_RECOGNITION = use_speech_recognition.get()
    VOICE_SAMPLE_TORTOISE = voice_sample_tortoise.get()
    VOICE_SAMPLE_COQUI = voice_sample_coqui.get()
    VITS_SPEAKER = vits_speaker.get()
    root.destroy()

other_frame = tk.LabelFrame(
    root,
    bg=menu_background_pink,
    text="General Settings",
    fg='white',
    font=("Helvetica", 16, "bold"),
    bd = 5
)
other_frame.place(anchor="c", relx=.5, rely=0.21)

use_tts = tk.StringVar()
game_path = tk.StringVar()
webui_path = tk.StringVar()
launch_yourself = tk.StringVar()
launch_yourself_webui = tk.StringVar()
use_actions = tk.StringVar()
tts_model = tk.StringVar()
use_speech_recognition = tk.StringVar()
voice_sample_tortoise = tk.StringVar()  
voice_sample_coqui = tk.StringVar()
vits_speaker = tk.StringVar()
character_json = tk.StringVar()

# Use default VITS model path
VITS_MODEL_PATH = os.path.join("VITS_model", "model.pth")
if not os.path.exists("VITS_model"):
    os.makedirs("VITS_model")
    
def verify_vits_model():
    if not os.path.exists(VITS_MODEL_PATH):
        tk.messagebox.showwarning(
            "VITS Model Missing",
            f"VITS model not found at {VITS_MODEL_PATH}. Please ensure you have a trained VITS model."
        )

# General Settings
bold_font = ('helvetic', 10, 'bold')

# Create all labels but don't grid them yet
game_path_label = tk.Label(other_frame, text="Game Path", bg=menu_background_pink, fg='white', font=bold_font)
launch_yourself_label1 = tk.Label(other_frame, text="Launch Yourself", bg=menu_background_pink, fg='white', font=bold_font)
use_actions_label = tk.Label(other_frame, text="Use Actions", bg=menu_background_pink, fg='white', font=bold_font)
use_tts_label = tk.Label(other_frame, text="Use TTS", bg=menu_background_pink, fg='white', font=bold_font)
tts_model_label = tk.Label(other_frame, text="TTS model", bg=menu_background_pink, fg='white', font=bold_font)
speech_recognition_label = tk.Label(other_frame, text="Use Speech Recognition", bg=menu_background_pink, fg='white', font=bold_font)
tortoise_label = tk.Label(other_frame, text="Tortoise Voice Sample", bg=menu_background_pink, fg='white', font=bold_font)
voice_sample_label = tk.Label(other_frame, text="Voice Sample", bg=menu_background_pink, fg='white', font=bold_font)
vits_speaker_label = tk.Label(other_frame, text="VITS Speaker", bg=menu_background_pink, fg='white', font=bold_font)
webui_path_label = tk.Label(other_frame, text="WebUI Path", bg=menu_background_pink, fg='white', font=bold_font)
launch_yourself_label2 = tk.Label(other_frame, text="Launch Yourself", bg=menu_background_pink, fg='white', font=bold_font)

# Grid the permanent labels
game_path_label.grid(row=1, column=0)
launch_yourself_label1.grid(row=1, column=3)
use_actions_label.grid(row=2, column=0)
use_tts_label.grid(row=3, column=0)
tts_model_label.grid(row=3, column=3)
speech_recognition_label.grid(row=6, column=0)
webui_path_label.grid(row=9, column=0)
launch_yourself_label2.grid(row=9, column=3)

# Voice-related labels will be managed by update_speaker_options()
tortoise_label.grid(row=7, column=0)
voice_sample_label.grid(row=7, column=3)

# Textual Inputs
game_path_entry = tk.Entry(other_frame, textvariable=game_path, width=25, bg=doki_white, fg='black')
game_path_entry.grid(row=1, column=1)
webui_path_entry = tk.Entry(other_frame, textvariable=webui_path, width=25, bg=doki_white, fg='black')
webui_path_entry.grid(row=9, column=1)

load_from_json("GAME_PATH", game_path_entry)
load_from_json("WEBUI_PATH", webui_path_entry)

def update_speaker_options(*args):
    if tts_model.get() == "VITS":
        # Verify VITS model exists when selected
        verify_vits_model()
        # Show VITS options
        vits_speaker_entry.grid(row=8, column=1)
        vits_speaker_label.grid(row=8, column=0)
        # Hide other voice sample options
        voice_menu_tortoise.grid_remove()
        voice_menu_coqui.grid_remove()
        tortoise_label.grid_remove()
        voice_sample_label.grid_remove()
    else:
        # Hide VITS options
        vits_speaker_entry.grid_remove()
        vits_speaker_label.grid_remove()
        # Show other voice sample options
        voice_menu_tortoise.grid(row=7, column=1)
        voice_menu_coqui.grid(row=7, column=4)
        tortoise_label.grid(row=7, column=0)
        voice_sample_label.grid(row=7, column=3)

tts_menu = tk.OptionMenu(other_frame, tts_model, "Your TTS", "XTTS", "Tortoise TTS", "VITS")
tts_menu.config(bg=doki_white, fg='black')
tts_menu.grid(row=3, column=4)
tts_model.trace('w', update_speaker_options)

# VITS speaker selection
vits_speaker_entry = tk.Entry(other_frame, textvariable=vits_speaker, width=25, bg=doki_white, fg='black')
vits_speaker_entry.grid(row=8, column=1)
vits_speaker_entry.grid_remove()

# Voice sample selections
all_voices_tortoise = os.listdir("tortoise_audios")
all_voices_tortoise = [x for x in all_voices_tortoise if not x.endswith(".txt")]
voice_menu_tortoise = tk.OptionMenu(other_frame, voice_sample_tortoise, *all_voices_tortoise)
voice_menu_tortoise.config(bg=doki_white, fg='black')
voice_menu_tortoise.grid(row=8, column=1)

all_voices_coquiai = os.listdir("coquiai_audios")
all_voices_coquiai = [x for x in all_voices_coquiai if x.endswith(".wav")]
if len(all_voices_coquiai) == 0:
    all_voices_coquiai = ["No voices found"]
voice_menu_coqui = tk.OptionMenu(other_frame, voice_sample_coqui, *all_voices_coquiai)
voice_menu_coqui.config(bg=doki_white, fg='black')
voice_menu_coqui.grid(row=8, column=4)

aspect_params = {
    "bg": menu_background_pink,
    "activeforeground": 'white',
    "fg": 'white',
    "activebackground": doki_light_pink,
    "selectcolor": doki_purple,
    "font": bold_font
}

tk.Radiobutton(other_frame, text="Yes", variable=launch_yourself, value=True, **aspect_params).grid(row=1, column=4)
tk.Radiobutton(other_frame, text="No", variable=launch_yourself, value=False, **aspect_params).grid(row=1, column=5)

tk.Radiobutton(other_frame, text="Yes", variable=use_actions, value=True, **aspect_params).grid(row=2, column=1)
tk.Radiobutton(other_frame, text="No", variable=use_actions, value=False, **aspect_params).grid(row=2, column=2)

tk.Radiobutton(other_frame, text="Yes", variable=use_tts, value=True, **aspect_params).grid(row=3, column=1)
tk.Radiobutton(other_frame, text="No", variable=use_tts, value=False, **aspect_params).grid(row=3, column=2)

tk.Radiobutton(other_frame, text="Yes", variable=use_speech_recognition, value=True, **aspect_params).grid(row=6, column=1)
tk.Radiobutton(other_frame, text="No", variable=use_speech_recognition, value=False, **aspect_params).grid(row=6, column=2)

tk.Radiobutton(other_frame, text="Yes", variable=launch_yourself_webui, value=True, **aspect_params).grid(row=9, column=4)
tk.Radiobutton(other_frame, text="No", variable=launch_yourself_webui, value=False, **aspect_params).grid(row=9, column=5)

button_background = tk.PhotoImage(file=r"images\login\button_background.png")
button = tk.Button(root, image=button_background, height=40, width=214, command=get_input, bd=0)
button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

if not os.path.exists("config.json"):
    # Set default values
    launch_yourself.set(0)
    launch_yourself_webui.set(0)
    use_tts.set(0)
    use_actions.set(0)
    tts_model.set("Your TTS")
    use_speech_recognition.set(0)
    voice_sample_tortoise.set("Choose a Tortoise voice sample")
    voice_sample_coqui.set("Choose a voice sample")
    vits_speaker.set("0")

else:
    with open("config.json", "r") as f:
        config = json.load(f)
    GAME_PATH = config["GAME_PATH"]
    WEBUI_PATH = config["WEBUI_PATH"]
    USE_TTS = config["USE_TTS"]
    LAUNCH_YOURSELF = config["LAUNCH_YOURSELF"]
    LAUNCH_YOURSELF_WEBUI = config["LAUNCH_YOURSELF"]
    USE_ACTIONS = config["USE_ACTIONS"]
    TTS_MODEL = config["TTS_MODEL"]
    USE_SPEECH_RECOGNITION = config["USE_SPEECH_RECOGNITION"]
    VOICE_SAMPLE_COQUI = config["VOICE_SAMPLE_COQUI"]
    VOICE_SAMPLE_TORTOISE = config["VOICE_SAMPLE_TORTOISE"]
    VITS_SPEAKER = config.get("VITS_SPEAKER", "Speaker1")
    # Set saved values
    launch_yourself.set(LAUNCH_YOURSELF)
    launch_yourself_webui.set(LAUNCH_YOURSELF_WEBUI)
    use_tts.set(USE_TTS)
    use_actions.set(USE_ACTIONS)
    tts_model.set(TTS_MODEL)
    use_speech_recognition.set(USE_SPEECH_RECOGNITION)
    voice_sample_tortoise.set(VOICE_SAMPLE_TORTOISE)
    voice_sample_coqui.set(VOICE_SAMPLE_COQUI)
    vits_speaker.set(VITS_SPEAKER)

def on_closing():
    root.destroy()
    raise SystemExit

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

# Convert string to int (0 or 1, False or True)
USE_TTS = int(USE_TTS)
LAUNCH_YOURSELF = int(LAUNCH_YOURSELF)
LAUNCH_YOURSELF_WEBUI = int(LAUNCH_YOURSELF_WEBUI)
USE_ACTIONS = int(USE_ACTIONS)
USE_SPEECH_RECOGNITION = int(USE_SPEECH_RECOGNITION)

CONFIG = {
    "GAME_PATH": GAME_PATH,
    "WEBUI_PATH": WEBUI_PATH,
    "USE_TTS": USE_TTS,
    "LAUNCH_YOURSELF": LAUNCH_YOURSELF,
    "LAUNCH_YOURSELF_WEBUI": LAUNCH_YOURSELF_WEBUI,
    "USE_ACTIONS": USE_ACTIONS,
    "TTS_MODEL": TTS_MODEL,
    "USE_SPEECH_RECOGNITION": USE_SPEECH_RECOGNITION,
    "VOICE_SAMPLE_TORTOISE": VOICE_SAMPLE_TORTOISE,
    "VOICE_SAMPLE_COQUI": VOICE_SAMPLE_COQUI,
    "VITS_SPEAKER": VITS_SPEAKER,
    "VITS_MODEL_PATH": VITS_MODEL_PATH
}

with open("config.json", "w") as f:
    json.dump(CONFIG, f)
