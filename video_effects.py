from fastrtc import Stream
import numpy as np
import gradio as gr

def apply_effects(image, blur_amount=0, brightness=1.0):
    # Apply blur if enabled
    if blur_amount > 0:
        image = cv2.GaussianBlur(image, 
                               ksize=(blur_amount*2+1, blur_amount*2+1),
                               sigmaX=0)
    
    # Adjust brightness
    image = cv2.convertScaleAbs(image, alpha=brightness, beta=0)
    
    return image

stream = Stream(
    handler=apply_effects,
    modality="video",
    mode="send-receive",
    additional_inputs=[
        gr.Slider(minimum=0, maximum=10, value=0, label="Blur Amount"),
        gr.Slider(minimum=0.5, maximum=2.0, value=1.0, label="Brightness")
    ]
)

stream.ui.launch()