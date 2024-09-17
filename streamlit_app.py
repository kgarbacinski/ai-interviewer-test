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
    st.session_state.audio_responses = {}

if 'active_question' not in st.session_state:
    st.session_state.active_question = None

if 'recorder_active' not in st.session_state:
    st.session_state.recorder_active = {idx: False for idx in range(len(questions))}

st.title("Voice-based Questionnaire")


# Function to reset all recorder states
def reset_recorders():
    for idx in range(len(questions)):
        st.session_state.recorder_active[idx] = False


# Iterate through the questions
for idx, question in enumerate(questions):
    st.subheader(f"Question {idx + 1}: {question}")

    # Check if the user has already recorded an answer
    if question in st.session_state.audio_responses:
        st.write("Recorded Answer: (Re-record if needed)")
        st.audio(st.session_state.audio_responses[question], format="audio/wav")
    else:
        st.write("No answer recorded yet.")

    # Create a button to record answer for each question
    if st.button(f"Record Answer for Question {idx + 1}", key=f"record_btn_{idx}"):
        reset_recorders()  # Reset all recorder states
        st.session_state.active_question = idx  # Set active question
        st.session_state.recorder_active[idx] = True  # Activate this recorder

    # If this is the active question, show the recorder below it
    if st.session_state.recorder_active[idx]:
        st.write(f"Recording for Question {idx + 1}:")
        audio_bytes = st_audiorec()

        # Ensure the recording is not None before saving
        if audio_bytes is not None:
            st.session_state.audio_responses[questions[idx]] = audio_bytes
            st.success(f"Recording for Question {idx + 1} saved!")
            reset_recorders()  # Reset the recorders after saving
            audio_bytes = None

# Submit button
if st.button("Submit All Responses"):
    # Check if all questions have been answered
    if all(question in st.session_state.audio_responses for question in questions):
        st.write("Sending responses to API...")

        for idx, question in enumerate(questions):
            audio = st.session_state.audio_responses[question]
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
