from fastrtc import Stream
import cv2
import gradio as gr

def detect_objects(image, confidence_threshold=0.3):
    # Resize image for detection
    resized = cv2.resize(image, (416, 416))
    
    # Detect objects (implementation depends on chosen model)
    outputs = detect(resized)
    
    # Draw bounding boxes on original image
    for output in outputs:
        scores = output[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        
        if confidence > confidence_threshold:
            # Draw bounding box and class label
            cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)
            cv2.putText(image, f"{class_name}: {confidence:.2f}", 
                       (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                       font_scale, color, thickness)
    
    return image

stream = Stream(
    handler=detect_objects,
    modality="video",
    mode="send-receive",
    additional_inputs=[
        gr.Slider(minimum=0.0, maximum=1.0, value=0.3, 
                 label="Confidence Threshold")
    ]
)

stream.ui.launch()