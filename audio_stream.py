from fastrtc import Stream, ReplyOnPause
import numpy as np

def echo(audio: tuple[int, np.ndarray]) -> tuple[int, np.ndarray]:
    """Echo function that returns the received audio"""
    yield audio

stream = Stream(
    handler=ReplyOnPause(echo),
    modality="audio",
    mode="send-receive"
)

# Launch the stream with UI
stream.ui.launch()