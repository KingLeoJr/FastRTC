import os
from fastrtc import (ReplyOnPause, Stream, get_stt_model, get_tts_model)
from openai import OpenAI

openrouter_client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1")
model="google/gemini-2.0-flash-thinking-exp"
stt_model = get_stt_model()
tts_model = get_tts_model()

def ai_response(audio):
    prompt = stt_model.stt(audio)
    response = openrouter_client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
    )
    response_text = response.choices[0].message.content
    for audio_chunk in tts_model.stream_tts_sync(response_text):
        yield audio_chunk

stream = Stream(
    handler=ReplyOnPause(ai_response),
    modality="audio",
    mode="send-receive"
)
stream.ui.launch()