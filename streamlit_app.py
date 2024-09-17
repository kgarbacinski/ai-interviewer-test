import streamlit as st
import requests
from st_audiorec import st_audiorec  # Correct import

# Hardcoded questions
questions = [
    "What is your name?",
    "How do you feel today?",
    "What are your goals for this week?"
]

# Initialize session state for audio responses and active recording question
if 'audio_responses' not in st.session_state:
    st.session_state.audio_responses = {question: None for question in questions}

if 'recorder_active' not in st.session_state:
    st.session_state.recorder_active = {idx: False for idx in range(len(questions))}

if 'recordings' not in st.session_state:
    st.session_state.recordings = {idx: None for idx in range(len(questions))}

st.title("Voice-based Questionnaire")


# Iterate through the questions
for idx, question in enumerate(questions):
    st.subheader(f"Question {idx + 1}: {question}")

    # Check if the user has already recorded an answer
    if st.session_state.recordings[idx] is not None:
        st.write("Recorded Answer: (Re-record if needed)")
        st.audio(st.session_state.recordings[idx], format="audio/wav")
    else:
        st.write("No answer recorded yet.")

    # Create a button to record answer for each question
    if st.button(f"Record Answer for Question {idx + 1}", key=f"record_btn_{idx}"):
        st.session_state.recorder_active[idx] = True  # Activate this recorder

    # If this is the active question, show the recorder below it
    if st.session_state.recorder_active[idx]:
        st.write(f"Recording for Question {idx + 1}:")

        # This creates a new audio recorder per question
        audio_bytes = st_audiorec()

        # Ensure the recording is not None before saving
        if audio_bytes is not None:
            st.session_state.recordings[idx] = audio_bytes
            st.session_state.recorder_active[idx] = False  # Reset the active recorder state
            st.success(f"Recording for Question {idx + 1} saved!")

# Submit button
if st.button("Submit All Responses"):
    # Check if all questions have been answered
    if all(st.session_state.recordings[idx] is not None for idx in range(len(questions))):
        st.write("Sending responses to API...")

        for idx, question in enumerate(questions):
            audio = st.session_state.recordings[idx]
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
