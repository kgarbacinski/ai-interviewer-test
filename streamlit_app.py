import streamlit as st
import requests
from st_audiorec import st_audiorec  # Correct import

# Hardcoded questions
questions = [
    "What is your name?",
    "How do you feel today?",
    "What are your goals for this week?"
]

# Initialize session state for audio responses
if 'audio_responses' not in st.session_state:
    st.session_state.audio_responses = {idx: None for idx in range(len(questions))}

if 'recording_active' not in st.session_state:
    st.session_state.recording_active = {idx: False for idx in range(len(questions))}

st.title("Voice-based Questionnaire")

# Function to stop all recordings
def stop_all_recordings():
    for idx in range(len(questions)):
        st.session_state.recording_active[idx] = False

# Iterate through the questions
for idx, question in enumerate(questions):
    st.subheader(f"Question {idx + 1}: {question}")
    
    # Check if the user has already recorded an answer
    if st.session_state.audio_responses[idx]:
        st.write("Recorded Answer: (Re-record if needed)")
        st.audio(st.session_state.audio_responses[idx], format="audio/wav")
    else:
        st.write("No answer recorded yet.")

    # Start recording button
    if not st.session_state.recording_active[idx] and st.button(f"Start Recording for Question {idx + 1}", key=f"start_btn_{idx}"):
        stop_all_recordings()  # Stop any active recordings
        st.session_state.recording_active[idx] = True  # Activate this question's recorder

    # Stop recording button
    if st.session_state.recording_active[idx] and st.button(f"Stop Recording for Question {idx + 1}", key=f"stop_btn_{idx}"):
        audio_bytes = st_audiorec()  # Trigger the recording
        if audio_bytes:
            st.session_state.audio_responses[idx] = audio_bytes  # Save the recorded audio
            st.success(f"Recording for Question {idx + 1} saved!")
        st.session_state.recording_active[idx] = False  # Deactivate recorder after saving

# Submit button
if st.button("Submit All Responses"):
    # Check if all questions have been answered
    if all(st.session_state.audio_responses[idx] for idx in range(len(questions))):
        st.write("Sending responses to API...")
        
        for idx, question in enumerate(questions):
            audio = st.session_state.audio_responses[idx]
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
