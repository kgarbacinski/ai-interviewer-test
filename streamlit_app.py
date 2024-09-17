import streamlit as st
import requests
from streamlit_audiorec import st_audiorec

# Hardcoded questions
questions = [
    "What is your name?",
    "How do you feel today?",
    "What are your goals for this week?"
]

# Initialize session state for audio responses
if 'audio_responses' not in st.session_state:
    st.session_state.audio_responses = {}

st.title("Voice-based Questionnaire")

for idx, question in enumerate(questions):
    st.subheader(f"Question {idx + 1}: {question}")
    
    # Check if the user has already recorded an answer
    if question in st.session_state.audio_responses:
        st.audio(st.session_state.audio_responses[question], format="audio/wav")
        st.write("Recorded Answer:")
        st.write(st.session_state.audio_responses[question])
    
    # Prompt to record answer
    audio_bytes = st_audiorec()
    
    if audio_bytes:
        # Save the audio response
        st.session_state.audio_responses[question] = audio_bytes
        st.audio(audio_bytes, format="audio/wav")
        st.success("Recording saved!")

# Submit button
if st.button("Submit All Responses"):
    if len(st.session_state.audio_responses) == len(questions):
        st.write("Sending responses to API...")
        
        for question, audio in st.session_state.audio_responses.items():
            # Prepare the audio file for upload
            files = {
                'audio': ('response.wav', audio, 'audio/wav')
            }
            data = {
                'question': question
            }
            
            try:
                response = requests.post(
                    "https://api.example.com/submit-audio",  # Replace with your API endpoint
                    files=files,
                    data=data
                )
                st.write(f"Sent response for '{question}' with status {response.status_code}")
            except Exception as e:
                st.error(f"Failed to send response for '{question}': {e}")
    else:
        st.error("Please record responses for all questions before submitting.")
