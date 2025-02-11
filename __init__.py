import os
import sys
import torch
from .nodes import ZonosTTSNode

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Node class mappings
NODE_CLASS_MAPPINGS = {
    "ZonosTTSNode": ZonosTTSNode,
}

# Node display names
NODE_DISPLAY_NAME_MAPPINGS = {
    "ZonosTTSNode": "Zonos TTS",
}

# Required dependencies
REQUIREMENTS = [
    "torch>=2.0",
    "torchaudio>=2.0",
    "safetensors>=0.3.0",
    "transformers>=4.30.0",
    "huggingface_hub>=0.16.0",
]

# Description for the node
WEB_DIRECTORY = "web"
DESCRIPTION = """
A custom node for generating speech using the Zyphra/Zonos-v0.1-hybrid text-to-speech model.
Supports multilingual text input, emotion control, and voice cloning.
"""

# Export the mappings and requirements
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY", "DESCRIPTION"]