from fastrtc import Stream, ReplyOnPause
from fastrtc.tracks import StreamHandlerBase
import requests
import json
from dotenv import load_dotenv
import os
import cv2
import base64
from PIL import Image
import io

class AudioHandler(StreamHandlerBase):
    def __init__(self, virtual_assistant):
        super().__init__(
            expected_layout="mono",
            output_sample_rate=24000,
            output_frame_size=960,
            input_sample_rate=48000
        )
        self.virtual_assistant = virtual_assistant
    
    async def on_track(self, track):
        while True:
            try:
                # Get audio frames
                frame = await track.recv()
                # Process the audio frame
                result = self.virtual_assistant.process_audio(audio=frame)
                # Send the processed result back
                if result:
                    yield result["audio"]
            except Exception as e:
                print(f"Audio processing error: {str(e)}")
                break

class VirtualAssistant:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        # Load API key from .env
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in .env file")
        # Configure free model
        self.model = "google/gemini-2.0-flash-thinking-exp"
        # Create audio handler instance
        self.audio_handler = AudioHandler(self)
        # Initialize FastRTC streams
        self.audio_stream = Stream(
            handler=self.audio_handler,
            modality="audio",
            mode="send-receive"
        )
        self.video_stream = Stream(
            handler=self.process_video,
            modality="video",
            mode="send-receive"
        )

    def process_audio(self, audio=None):
        try:
            if audio:
                prompt = f"""
                You are a virtual assistant helping users troubleshoot technical issues.
                The user has provided audio input: {audio}
                Identify the user's problem based on the audio and provide concrete,
                step-by-step instructions to solve it. Focus on practical steps.
                """
                response = self.get_ai_response(prompt)
                return {"audio": response}
            return None
        except Exception as e:
            print(f"Error processing audio: {str(e)}")
            return None

    def frame_to_base64(self, frame):
        _, buffer = cv2.imencode('.jpg', frame)
        base64_frame = base64.b64encode(buffer).decode('utf-8')
        return base64_frame

    def process_video(self, video_frame=None):
        try:
            if video_frame:
                video_data = self.frame_to_base64(video_frame)
                prompt = f"""
                You are a virtual assistant helping users troubleshoot technical issues.
                The user has provided video input showing: {video_data}
                Identify the user's problem based on the visual information and provide
                concrete, step-by-step instructions to solve it. Focus on practical steps.
                """
                response = self.get_ai_response(prompt)
                processed_frame = self.highlight_problem_area(video_frame, response)
                return {
                    "video": processed_frame,
                    "response": response
                }
            return None
        except Exception as e:
            print(f"Error processing video: {str(e)}")
            return None

    def get_ai_response(self, prompt):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "messages": [{
                "role": "system",
                "content": """
                You are a virtual assistant with expertise in computer vision and AI.
                You analyze audio and video inputs to provide comprehensive support,
                offering concrete, step-by-step instructions to solve technical issues.
                Maintain a professional and helpful tone, being direct and concise.
                """
            }, {
                "role": "user",
                "content": prompt
            }]
        }
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(data)
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        return None

    def highlight_problem_area(self, frame, ai_response):
        try:
            cv2.putText(frame, "Problem Area Highlighted",
                       (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                       0.5, (0, 0, 255), 2)
            return frame
        except Exception as e:
            print(f"Error in highlighting: {str(e)}")
            return frame

    def run(self):
        # Launch the Gradio UI
        self.audio_stream.ui.launch(
            show_api=False,
            show_error=False,
        )
        self.video_stream.ui.launch(
            show_api=False,
            show_error=False,
        )

if __name__ == "__main__":
    app = VirtualAssistant()
    app.run()