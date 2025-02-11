class ZonosTTSNode:
    def __init__(self):
        pass
    
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
        # For testing, return dummy data
        audio_output = {
            "waveform": None,  # Replace with actual waveform
            "sampling_rate": 44000
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

# Node mappings
NODE_CLASS_MAPPINGS = {
    "ZonosTTSNode": ZonosTTSNode
}

# Display names
NODE_DISPLAY_NAME_MAPPINGS = {
    "ZonosTTSNode": "Zonos TTS"
}