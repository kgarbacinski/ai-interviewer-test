import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase
import requests
import os
import numpy as np
import wave

# Hardcoded questions
questions = [
    "What is your name?",
    "How do you feel today?",
    "What are your goals for this week?"
]

# Dictionary to store user responses
audio_responses = {}

# Define Audio Processor class for recording
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
    
    # Record button
    if st.button(f"Record Answer for Question {idx + 1}"):
        st.session_state[f'record_{idx}'] = webrtc_streamer(
            key=f'webrtc_{idx}',
            mode=WebRtcMode.SENDONLY,
            audio_receiver_size=1024,
            audio_processor_factory=AudioProcessor
        )
    
    # If the recorder was created and we finished recording
    if f'record_{idx}' in st.session_state and st.session_state[f'record_{idx}'].state.playing == False:
        st.write(f"Recording for Question {idx + 1} finished.")
        processor = st.session_state[f'record_{idx}'].audio_processor
        filename = f"response_q{idx + 1}.wav"
        
        # Save the audio
        save_audio(processor.audio_frames, filename)
        audio_responses[question] = filename
        st.audio(filename, format='audio/wav')

# Submit button
if st.button("Submit All Responses"):
    if len(audio_responses) == len(questions):
        st.write("Sending responses to API...")

        # Simulating sending audio files to an external API
        for question, filename in audio_responses.items():
            # Read the saved audio file
            with open(filename, 'rb') as f:
                pass
                # Example of sending audio to an API (adjust URL and payload accordingly)
                # response = requests.post(
                #     "https://api.example.com/submit-audio",
                #     files={"audio": f},
                #     data={"question": question}
                # )
                
            st.write(f"Sent response for '{question}' with status {response.status_code}")
    else:
        st.error("Please record responses for all questions.")
