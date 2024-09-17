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
    st.session_state.audio_responses = {}

# Initialize session state for each question's audio recording
for idx in range(len(questions)):
    if f"audio_recording_{idx}" not in st.session_state:
        st.session_state[f"audio_recording_{idx}"] = None

st.title("Voice-based Questionnaire")

# Iterate through the questions
for idx, question in enumerate(questions):
    st.subheader(f"Question {idx + 1}: {question}")
    
    # Check if the user has already recorded an answer
    if st.session_state[f"audio_recording_{idx}"] is not None:
        st.write("Recorded Answer: (Re-record if needed)")
        st.audio(st.session_state[f"audio_recording_{idx}"], format="audio/wav")
    else:
        st.write("No answer recorded yet.")

    # Create a button to record answer for each question
    if st.button(f"Record Answer for Question {idx + 1}", key=f"record_btn_{idx}"):
        st.session_state.active_question = idx  # Set the active question

    # If this is the active question, show the recorder below it
    if 'active_question' in st.session_state and st.session_state.active_question == idx:
        st.write(f"Recording for Question {idx + 1}:")
        audio_bytes = st_audiorec()

        # Save the recorded audio in session state specific to this question
        if audio_bytes is not None:
            st.session_state[f"audio_recording_{idx}"] = audio_bytes
            st.success(f"Recording for Question {idx + 1} saved!")
            # Reset the active question after saving the audio
            st.session_state.active_question = None

# Submit button
if st.button("Submit All Responses"):
    # Check if all questions have been answered
    if all(st.session_state[f"audio_recording_{idx}"] is not None for idx in range(len(questions))):
        st.write("Sending responses to API...")
        
        for idx, question in enumerate(questions):
            audio = st.session_state[f"audio_recording_{idx}"]
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
