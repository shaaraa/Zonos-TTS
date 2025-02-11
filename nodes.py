import torch
import torchaudio
from zonos.model import Zonos
from zonos.conditioning import make_cond_dict

class ZonosTTSNode:
    def __init__(self):
        self.model = None
        
    def load_model(self):
        if self.model is None:
            self.model = Zonos.from_pretrained("Zyphra/Zonos-v0.1-hybrid", device="cuda")
            self.model.bfloat16()
    
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
    CATEGORY = "audio"

    def process_text(self, text, language, emotion, pitch=0.0, speaking_rate=1.0, speaker_audio=None):
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
            spk_embedding = self.model.embed_spk_audio(
                speaker_audio["waveform"], 
                speaker_audio["sampling_rate"]
            )
            cond_dict["speaker"] = spk_embedding.to(torch.bfloat16)
        
        # Generate audio
        conditioning = self.model.prepare_conditioning(cond_dict)
        codes = self.model.generate(conditioning)
        waveform = self.model.autoencoder.decode(codes)
        
        audio_output = {
            "waveform": waveform[0].cpu(),
            "sampling_rate": self.model.autoencoder.sampling_rate
        }
        
        metadata = {
            "text": text,
            "language": language,
            "emotion": emotion,
            "pitch": pitch,
            "speaking_rate": speaking_rate
        }
        
        return (audio_output, metadata)