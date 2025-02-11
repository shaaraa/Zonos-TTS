from nodes import AudioNode
import torch
import torchaudio
from safetensors.torch import load_file
from transformers import AutoConfig
from huggingface_hub import snapshot_download
import os

class ZonosTTSNode:
    def __init__(self):
        self.model = None
        self.config = None
        self.model_dir = os.path.join("models", "Zonos-v0.1-hybrid")
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
                "language": (["en-us", "ja", "zh", "fr", "de"], {"default": "en-us"}),
                "emotion": (["neutral", "happiness", "anger", "sadness", "fear"], {"default": "neutral"}),
            },
            "optional": {
                "speaker_audio": ("AUDIO",),
                "pitch": ("FLOAT", {"default": 0.0, "min": -1.0, "max": 1.0}),
                "speaking_rate": ("FLOAT", {"default": 1.0, "min": 0.5, "max": 2.0}),
            }
        }

    RETURN_TYPES = ("AUDIO", "JSON")
    FUNCTION = "process_text"

    def download_model(self):
        """Download the model from Hugging Face if it doesn't exist."""
        if not os.path.exists(self.model_dir):
            os.makedirs(self.model_dir, exist_ok=True)
        
        # Check if model files already exist
        required_files = ["config.json", "model.safetensors"]
        if all(os.path.exists(os.path.join(self.model_dir, f)) for f in required_files):
            return
        
        # Download from Hugging Face Hub
        print("Downloading Zonos-v0.1-hybrid model from Hugging Face...")
        snapshot_download(
            repo_id="Zyphra/Zonos-v0.1-hybrid",
            local_dir=self.model_dir,
            allow_patterns=["config.json", "model.safetensors"],
            resume_download=True
        )
        print("Model downloaded successfully!")

    def load_model(self):
        """Load the model from disk."""
        if self.model is None:
            self.download_model()  # Ensure model is downloaded
            
            # Load config
            config_path = os.path.join(self.model_dir, "config.json")
            self.config = AutoConfig.from_pretrained(config_path)
            
            # Load model weights from safetensors
            model_path = os.path.join(self.model_dir, "model.safetensors")
            state_dict = load_file(model_path)
            
            # Initialize model (replace with actual model class)
            self.model = ZonosModel(self.config)
            self.model.load_state_dict(state_dict)
            self.model.to("cuda")
            self.model.eval()

    def process_text(self, text, language, emotion, speaker_audio=None, pitch=0.0, speaking_rate=1.0):
        self.load_model()
        
        # Generate speech conditioning parameters
        cond_dict = {
            "text": text,
            "language": language,
            "emotion": emotion,
            "pitch": pitch,
            "speaking_rate": speaking_rate
        }
        
        # Load speaker embedding if provided
        if speaker_audio:
            wav, sr = torchaudio.load(speaker_audio)
            cond_dict["speaker_embedding"] = self.model.extract_speaker_embedding(wav, sr)
        
        # Generate speech
        with torch.no_grad():
            audio = self.model.generate(cond_dict)
        
        return (audio, {"parameters": cond_dict})