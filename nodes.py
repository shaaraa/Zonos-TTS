# nodes.py
import os
import torch
import torchaudio
from zonos.model import Zonos
from zonos.conditioning import make_cond_dict

class ZonosTTSNode:
    def __init__(self):
        self.model = None
        
    def load_model(self):
        if self.model is None:
            # Get the current directory where nodes.py is located
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Construct path to model directory
            model_path = os.path.join(current_dir, "models", "Zonos-v0.1-hybrid")
            
            if not os.path.exists(model_path):
                raise ValueError(f"Model directory not found at {model_path}")
                
            print(f"Loading Zonos model from {model_path}")
            self.model = Zonos.from_pretrained(model_path, device="cuda")
            self.model.bfloat16()
            print("Model loaded successfully")
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": "Hello, world!"}),
                "language": (["en-us", "ja", "zh", "fr", "de"], {"default": "en-us"}),
                "emotion": (["neutral", "happiness", "anger", "sadness", "fear"], {"default": "neutral"}),
                "pitch": ("FLOAT", {"default": 0.0, "min": -1.0, "max": 1.0, "step": 0.1}),
                "speaking_rate": ("FLOAT", {"default": 1.0, "min": 0.5, "max": 2.0, "step": 0.1}),
            },
            "optional": {
                "speaker_audio": ("AUDIO",),
            }
        }

    RETURN_TYPES = ("AUDIO", "JSON")
    RETURN_NAMES = ("audio", "metadata")
    FUNCTION = "process_text"
    CATEGORY = "audio/tts"

    def process_text(self, text, language, emotion, pitch=0.0, speaking_rate=1.0, speaker_audio=None):
        try:
            self.load_model()
            
            # Create conditioning dictionary
            cond_dict = make_cond_dict(
                text=text,
                language=language,
                emotion=emotion,
                pitch=pitch,
                speaking_rate=speaking_rate
            )
            
            # Add speaker embedding if provided
            if speaker_audio is not None:
                waveform = speaker_audio["waveform"]
                sample_rate = speaker_audio["sampling_rate"]
                
                # Convert to appropriate device and format
                waveform = waveform.to(self.model.device)
                if sample_rate != self.model.sample_rate:
                    waveform = torchaudio.functional.resample(waveform, sample_rate, self.model.sample_rate)
                
                spk_embedding = self.model.embed_spk_audio(waveform, self.model.sample_rate)
                cond_dict["speaker"] = spk_embedding.to(torch.bfloat16)
            
            # Generate audio
            conditioning = self.model.prepare_conditioning(cond_dict)
            codes = self.model.generate(conditioning)
            waveform = self.model.autoencoder.decode(codes)
            
            audio_output = {
                "waveform": waveform[0].cpu(),  # Return first item from batch
                "sampling_rate": self.model.autoencoder.sampling_rate
            }
            
            metadata = {
                "text": text,
                "language": language,
                "emotion": emotion,
                "pitch": pitch,
                "speaking_rate": speaking_rate,
                "has_speaker": speaker_audio is not None
            }
            
            return (audio_output, metadata)
            
        except Exception as e:
            print(f"Error generating audio: {str(e)}")
            # Return silent audio in case of error to avoid crashes
            silent_audio = torch.zeros((1, 44000), dtype=torch.float32, device="cpu")
            return ({"waveform": silent_audio, "sampling_rate": 44000}, metadata)

# Node mappings
NODE_CLASS_MAPPINGS = {
    "ZonosTTSNode": ZonosTTSNode
}

# Display names
NODE_DISPLAY_NAME_MAPPINGS = {
    "ZonosTTSNode": "Zonos TTS"
}