import streamlit as st
import requests
from st_audiorec import st_audiorec  # Correct import

# Hardcoded questions
questions = [
    "What is your name?",
    "How do you feel today?",
    "What are your goals for this week?"
]

# Initialize session state for audio responses and current question index
if 'audio_responses' not in st.session_state:
    st.session_state.audio_responses = {}

if 'current_question' not in st.session_state:
    st.session_state.current_question = 0  # Start with the first question

if 'recordings' not in st.session_state:
    st.session_state.recordings = {idx: None for idx in range(len(questions))}

st.title("Voice-based Questionnaire")


def move_to_next_question():
    """Helper function to move to the next question"""
    if st.session_state.current_question < len(questions) - 1:
        st.session_state.current_question += 1
    else:
        st.session_state.current_question = "submit"  # Go to submit page


# Get the current question index
current_idx = st.session_state.current_question

# Check if we are still asking questions or ready to submit
if isinstance(current_idx, int):
    st.subheader(f"Question {current_idx + 1}: {questions[current_idx]}")

    # Check if the user has already recorded an answer for this question
    if st.session_state.recordings[current_idx] is not None:
        st.write("Recorded Answer: (Re-record if needed)")
        st.audio(st.session_state.recordings[current_idx], format="audio/wav")
    else:
        st.write("No answer recorded yet.")

    # Audio recorder for the current question
    audio_bytes = st_audiorec()

    # If the user has recorded something, save the response
    if audio_bytes is not None:
        st.session_state.recordings[current_idx] = audio_bytes
        st.success(f"Recording for Question {current_idx + 1} saved!")

    # Button to move to the next question
    if st.button("Next Question"):
        if st.session_state.recordings[current_idx] is not None:
            move_to_next_question()
        else:
            st.error("Please record an answer before moving to the next question.")

else:
    # Final submission page
    st.subheader("Review and Submit Your Responses")

    # Display all recorded responses
    for idx, question in enumerate(questions):
        st.write(f"**Question {idx + 1}: {question}**")
        if st.session_state.recordings[idx] is not None:
            st.audio(st.session_state.recordings[idx], format="audio/wav")
        else:
            st.write("_No answer recorded._")

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
    
    # Option to go back and review questions
    if st.button("Go Back"):
        st.session_state.current_question = len(questions) - 1  # Go back to the last question
