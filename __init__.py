import os
import sys
import torch
from nodes import ZonosTTSNode

NODE_CLASS_MAPPINGS = {
    "ZonosTTSNode": ZonosTTSNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ZonosTTSNode": "Zonos TTS",
}

REQUIREMENTS = [
    "torch>=2.0",
    "torchaudio>=2.0",
    "safetensors>=0.3.0",
    "transformers>=4.30.0",
    "huggingface_hub>=0.16.0",
]

WEB_DIRECTORY = "web"
DESCRIPTION = """A custom node for generating speech using the Zyphra/Zonos-v0.1-hybrid text-to-speech model.
Supports multilingual text input, emotion control, and voice cloning."""

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY", "DESCRIPTION"]