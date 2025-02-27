import os
from fastrtc import (ReplyOnPause, Stream, get_stt_model, get_tts_model)
from fastrtc.tracks import StreamHandlerBase
import cv2
import gradio as gr
from openai import OpenAI
import numpy as np

openrouter_client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1")
model="google/gemini-2.0-flash-thinking-exp"
stt_model = get_stt_model()

# Define a class that inherits from StreamHandlerBase
class MyStreamHandler(StreamHandlerBase):
    def __init__(self, stt_model):
        super().__init__()
        self.stt_model = stt_model

    def process_stream(self, audio=None, video_frame=None):
        if audio:
            # Process voice commands
            prompt = self.stt_model.stt(audio)
            
            if "detect" in prompt.lower():
                # Activate detection mode
                return self.process_detection(video_frame)
            elif "track" in prompt.lower():
                # Activate tracking mode
                return self.process_tracking(video_frame)
        
        return video_frame

    def process_detection(self, frame):
        # Convert to grayscale and detect edges
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    def process_tracking(self, frame):
        # Placeholder for tracking logic
        return frame  # Replace with actual tracking implementation

# Instantiate the handler
stream_handler = MyStreamHandler(stt_model)

stream = Stream(
    handler=stream_handler,  # Pass the stream_handler object
    modality="audio-video",
    mode="send-receive",
    additional_inputs=[
        gr.Slider(minimum=50, maximum=150, value=100, label="Detection Sensitivity"),
        gr.Checkbox(label="Enable Voice Commands", value=True)
    ]
)

stream.ui.launch()