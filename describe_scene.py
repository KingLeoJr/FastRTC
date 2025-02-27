from fastrtc import Stream, ReplyOnPause, get_stt_model, get_tts_model
import cv2
import gradio as gr
from openai import OpenAI
import numpy as np

class MultimodalAIStream:
    def __init__(self):
        self.stt_model = get_stt_model()
        self.tts_model = get_tts_model()
        self.stt_client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1")

        
        # Command mappings
        self.commands = {
            "detect": self.detect_objects,
            "track": self.track_objects,
            "describe": self.describe_scene
        }
        
    def process_command(self, audio):
        # Convert speech to text
        prompt = self.stt_model.stt(audio)
        
        # Process command
        if prompt.lower() in self.commands:
            return self.commands[prompt.lower()]()
        else:
            return self.tts_model.stream_tts_sync(
                f"Available commands: {', '.join(self.commands.keys())}"
            )
    
    def detect_objects(self):
        # Object detection logic
        return self.tts_model.stream_tts_sync(
            "Object detection mode activated"
        )
    
    def track_objects(self):
        # Object tracking logic
        return self.tts_model.stream_tts_sync(
            "Object tracking mode activated"
        )
    
    def describe_scene(self):
        # Scene description logic
        return self.tts_model.stream_tts_sync(
            "Scene description mode activated"
        )

# Define UI arguments
ui_args = {
    "icon_radius": 50,  # Default icon radius (adjust as needed)
}

# Create and configure stream
stream = Stream(
    handler=ReplyOnPause(MultimodalAIStream().process_command),
    modality="audio-video",
    mode="send-receive",
    additional_inputs=[
        gr.Slider(minimum=0.1, maximum=1.0, value=0.5, label="Detection Threshold"),
        gr.CheckboxGroup(
            choices=["detect", "track", "describe"],
        )
    ],
    ui_args=ui_args  # Pass the ui_args dictionary
)

# Launch with UI
stream.ui.launch()