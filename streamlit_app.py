import streamlit as st
import requests
from st_audiorec import st_audiorec  # Correct library name

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
        st.write("Recorded Answer: (Re-record if needed)")
        # No need to use st.audio() because st_audiorec has a built-in player
    
    # Prompt to record answer
    st.write("Click the button below to record your answer.")
    audio_bytes = st_audiorec()  # Automatically provides the recording and playback interface
    
    if audio_bytes:
        # Save the audio response to session state
        st.session_state.audio_responses[question] = audio_bytes
        st.success(f"Recording for Question {idx + 1} saved!")

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
