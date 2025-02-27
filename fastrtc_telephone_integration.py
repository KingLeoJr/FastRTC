import os
from fastrtc import Stream
import gradio as gr
import numpy as np
from dotenv import load_dotenv
from fastrtc.tracks import StreamHandlerBase
import ssl  # Import the ssl module

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

# Set the default SSL context for the entire Python process (less recommended)
try:
    ssl._create_default_https_context = ssl.create_default_context
    context = ssl.create_default_context()
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    ssl._create_default_https_context = lambda: context
except AttributeError:
    print("TLS 1.2 or higher not supported on this Python version. Skipping TLS enforcement.")

class AIHandler(StreamHandlerBase):
    def __init__(self):
        super().__init__()

    def process_frame(self, audio_frame):
        """
        This is a placeholder for your AI-powered audio processing.
        Replace this with your actual audio processing logic.
        For example, you could use a speech-to-text model to transcribe the audio,
        or an audio classification model to detect events.
        """
        # Convert audio frame to numpy array (example)
        audio_data = np.frombuffer(audio_frame, dtype=np.float32)

        # Placeholder: Simulate some AI processing
        processed_audio = audio_data * 0.5  # Example: Reduce volume

        # Convert back to bytes
        processed_frame = processed_audio.tobytes()
        return processed_frame

stream = Stream(
    handler=AIHandler(),
    modality="audio",
    mode="send-receive",
)

try:
    stream.fastphone(
        token=HF_TOKEN,  # Optional: If None, will use the default token in your machine or read from the HF_TOKEN environment variable
        host="127.0.0.1",
        port=8000,
    )
except Exception as e:
    print(f"Error launching fastphone: {e}")
    print("Please ensure you have a valid Hugging Face token and the necessary dependencies installed.")

