from nodes import AudioNode
import torch
import torchaudio
from safetensors.torch import load_file
from transformers import AutoConfig, PreTrainedModel
from huggingface_hub import snapshot_download
import os

class ZonosModel(PreTrainedModel):
    def __init__(self, config):
        super().__init__(config)
        self.config = config
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
    def forward(self, cond_dict):
        return torch.randn(1, 16000)
    
    def generate(self, cond_dict):
        return self.forward(cond_dict)
    
    def extract_speaker_embedding(self, wav, sr):
        return torch.randn(1, 128)

class ZonosTTSNode(AudioNode):
    def __init__(self):
        super().__init__()
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
    CATEGORY = "audio"

    def download_model(self):
        if not os.path.exists(self.model_dir):
            os.makedirs(self.model_dir, exist_ok=True)
        
        required_files = ["config.json", "model.safetensors"]
        if all(os.path.exists(os.path.join(self.model_dir, f)) for f in required_files):
            return
        
        snapshot_download(
            repo_id="Zyphra/Zonos-v0.1-hybrid",
            local_dir=self.model_dir,
            allow_patterns=["config.json", "model.safetensors"],
            resume_download=True
        )

    def load_model(self):
        if self.model is None:
            self.download_model()
            
            config_path = os.path.join(self.model_dir, "config.json")
            self.config = AutoConfig.from_pretrained(config_path)
            
            model_path = os.path.join(self.model_dir, "model.safetensors")
            state_dict = load_file(model_path)
            
            self.model = ZonosModel(self.config)
            self.model.load_state_dict(state_dict)
            self.model.to("cuda" if torch.cuda.is_available() else "cpu")
            self.model.eval()

    def process_text(self, text, language, emotion, speaker_audio=None, pitch=0.0, speaking_rate=1.0):
        self.load_model()
        
        cond_dict = {
            "text": text,
            "language": language,
            "emotion": emotion,
            "pitch": pitch,
            "speaking_rate": speaking_rate
        }
        
        if speaker_audio:
            wav, sr = torchaudio.load(speaker_audio)
            cond_dict["speaker_embedding"] = self.model.extract_speaker_embedding(wav, sr)
        
        with torch.no_grad():
            audio = self.model.generate(cond_dict)
        
        return (audio, {"parameters": cond_dict})