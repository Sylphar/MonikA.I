from IPython import display as ipd
import simpleaudio as sa
from scripts.utils import HiddenPrints
import torch
from TTS.api import TTS
import os
import json
from dataclasses import dataclass

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

@dataclass
class VITSInfo:
    model: TTS
    sampling_rate: int

def initialize_xtts():
    model = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=device.type=="cuda")
    return model

def initialize_vits(model_path):
    """Initialize VITS model with a local checkpoint"""
    print(f"Initializing VITS with model path: {model_path}")
    # Get the directory containing the model
    model_dir = os.path.dirname(model_path)
    config_path = os.path.join(model_dir, "config.json")
    
    # Verify both files exist
    print(f"Checking for model at: {model_path}")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"VITS model not found at {model_path}")
    print(f"Checking for config at: {config_path}")
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"VITS config not found at {config_path}")
    
    # Read config to get sampling rate
    with open(config_path, 'r') as f:
        config = json.load(f)
    data_config = config.get('data', {})
    # Try both possible keys, with fallback to audio section and then default
    sampling_rate = (
        data_config.get('sampling_rate') or 
        data_config.get('sample_rate') or 
        config.get('audio', {}).get('sampling_rate') or 
        config.get('audio', {}).get('sample_rate') or 
        22050  # Default fallback
    )
    print(f"Using sampling rate from config: {sampling_rate}")
    
    print("Loading VITS model...")    
    model = TTS(
        model_path=model_path,
        config_path=config_path,
        progress_bar=False,
        gpu=device.type=="cuda"
    )
    print("VITS model loaded successfully")
    return VITSInfo(model=model, sampling_rate=sampling_rate)

def play_TTS(
    step,
    msg,
    play_obj,
    sampling_rate,
    tts_model,
    voice_samples,
    conditioning_latents,
    TTS_MODEL,
    VOICE_SAMPLE_COQUI,
    uni_chr_re,
    VITS_SPEAKER=None
):
    print(f"play_TTS called with model {TTS_MODEL}")
    if step > 0:
        print("Stopping previous audio")
        play_obj.stop()
    
    msg_audio = msg.replace("\n", " ")
    msg_audio = msg_audio.replace("{i}", "")
    msg_audio = msg_audio.replace("{/i}", ".")
    msg_audio = msg_audio.replace("~", "!")
    msg_audio = uni_chr_re.sub(r'', msg_audio)
    
    print(f"Processing message: {msg_audio[:50]}...")
    
    with HiddenPrints():
        if TTS_MODEL == "Your TTS":
            print("Using Your TTS model")
            audio = tts_model.tts(
                text=msg_audio,
                speaker_wav=f'coquiai_audios/{VOICE_SAMPLE_COQUI}',
                language='en'
            )
        elif TTS_MODEL == "XTTS":
            print("Using XTTS model")
            audio = tts_model.tts(
                text=msg_audio,
                speaker_wav=f'coquiai_audios/{VOICE_SAMPLE_COQUI}',
                language='en',
                split_sentences=True,
            )
            if isinstance(audio, torch.Tensor):
                audio = audio.cpu().numpy()
        elif TTS_MODEL == "VITS":
            print("Using VITS model")
            # If tts_model is VITSInfo, get the actual model
            if isinstance(tts_model, VITSInfo):
                actual_model = tts_model.model
                current_rate = tts_model.sampling_rate
            else:
                actual_model = tts_model
                current_rate = sampling_rate

            # Get the speaker name from the ID if needed
            if hasattr(actual_model.synthesizer.tts_model, 'speaker_manager'):
                speaker_names = actual_model.synthesizer.tts_model.speaker_manager.speaker_names
                # If VITS_SPEAKER is already a name in the list, use it directly
                if VITS_SPEAKER in speaker_names:
                    actual_speaker = VITS_SPEAKER
                else:
                    # Try to convert to int and use as index
                    try:
                        speaker_idx = int(VITS_SPEAKER)
                        if 0 <= speaker_idx < len(speaker_names):
                            actual_speaker = speaker_names[speaker_idx]
                        else:
                            actual_speaker = speaker_names[0]  # Fallback to first speaker
                            print(f"Speaker index {speaker_idx} out of range, using {actual_speaker}")
                    except ValueError:
                        # If conversion fails, use first speaker
                        actual_speaker = speaker_names[0]
                        print(f"Invalid speaker specification, using {actual_speaker}")
            else:
                actual_speaker = str(VITS_SPEAKER)
            
            print(f"Using speaker: {actual_speaker}")
            audio = actual_model.tts(
                text=msg_audio,
                speaker=actual_speaker,
                language="en"
            )
            if isinstance(audio, torch.Tensor):
                audio = audio.cpu().numpy()
            print("VITS audio generated successfully")
        elif TTS_MODEL == "Tortoise TTS":
            print("Using Tortoise model")
            if device.type == "cuda":
                gen, _ = tts_model.tts_stream(
                    text=msg_audio,
                    k=1,
                    voice_samples=voice_samples,
                    conditioning_latents=conditioning_latents,
                    num_autoregressive_samples=8,
                    diffusion_iterations=20,
                    return_deterministic_state=True,
                    length_penalty=1.8,
                    max_mel_tokens=500,
                    cond_free_k=2,
                    top_p=0.85,
                    repetition_penalty=2.,
                )
            else:
                gen = tts_model.tts(
                    text=msg_audio,
                    k=1,
                    voice_samples=voice_samples,
                    conditioning_latents=conditioning_latents,
                    num_autoregressive_samples=8,
                    length_penalty=1.8,
                    max_mel_tokens=500,
                    top_p=0.85,
                    repetition_penalty=2.,
                )
            audio = gen.squeeze(0).cpu().numpy()
    
    print(f"Converting audio with rate {sampling_rate}")
    if TTS_MODEL == "VITS" and isinstance(tts_model, VITSInfo):
        current_rate = tts_model.sampling_rate
    else:
        current_rate = 24000 if TTS_MODEL == "XTTS" else sampling_rate
        
    audio = ipd.Audio(audio, rate=current_rate)
    play_obj = sa.play_buffer(audio.data, 1, 2, current_rate)
    print("Audio playback started")
    return play_obj
