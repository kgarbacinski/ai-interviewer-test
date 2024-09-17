import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase
import numpy as np
import wave
import os

# Hardcoded questions
questions = [
    "What is your name?",
    "How do you feel today?",
    "What are your goals for this week?"
]

# Initialize session state for recorded audio
if 'audio_responses' not in st.session_state:
    st.session_state.audio_responses = {}

# Initialize session state for recording status
if 'recording' not in st.session_state:
    st.session_state.recording = {idx: False for idx in range(len(questions))}

# Audio Processor class for WebRTC audio capture
class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.audio_frames = []
    
    def recv(self, frame):
        self.audio_frames.append(frame)
        return frame

def save_audio(frames, filename):
    """ Save the audio frames as a wav file """
    if len(frames) == 0:
        return None
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16 bits per sample
        wf.setframerate(16000)
        wf.writeframes(b''.join([frame.to_ndarray().tobytes() for frame in frames]))

# Streamlit layout
st.title("Voice-based Questionnaire")

for idx, question in enumerate(questions):
    st.subheader(f"Question {idx + 1}: {question}")
    
    # Toggle recording button
    if not st.session_state.recording[idx]:
        if st.button(f"Start Recording for Question {idx + 1}", key=f"start_{idx}"):
            st.session_state.recording[idx] = True
    else:
        webrtc_ctx = webrtc_streamer(
            key=f'webrtc_{idx}',
            mode=WebRtcMode.SENDONLY,
            audio_receiver_size=1024,
            audio_processor_factory=AudioProcessor,
            media_stream_constraints={"audio": True, "video": False}
        )
        
        if webrtc_ctx.audio_receiver:
            processor = webrtc_ctx.audio_processor
            if processor and len(processor.audio_frames) > 0:
                filename = f"response_q{idx + 1}.wav"
                save_audio(processor.audio_frames, filename)
                st.session_state.audio_responses[question] = filename
                st.audio(filename, format='audio/wav')
                st.session_state.recording[idx] = False
                st.write(f"Recording for Question {idx + 1} finished.")

# Submit button
if st.button("Submit All Responses"):
    if len(st.session_state.audio_responses) == len(questions):
        st.write("Sending responses to API...")

        # Simulating sending audio files to an external API
        for question, filename in st.session_state.audio_responses.items():
            # Here, you would send the audio files to your API
            st.write(f"Prepared response for '{question}', file: {filename}")
        
        st.success("All responses have been successfully submitted!")
    else:
        st.error("Please record responses for all questions.")
