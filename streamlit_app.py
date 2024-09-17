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

st.title("Voice-based Questionnaire")

# Iterate through the questions
for idx, question in enumerate(questions):
    st.subheader(f"Question {idx + 1}: {question}")
    
    # Check if the user has already recorded an answer
    if question in st.session_state.audio_responses:
        st.write("Recorded Answer: (Re-record if needed)")
        # No need to use st.audio() because st_audiorec has a built-in player
    else:
        st.write("No answer recorded yet.")

    # Create a button to record answer for each question
    if st.button(f"Record Answer for Question {idx + 1}", key=f"record_btn_{idx}"):
        st.session_state.active_question = idx

    # If this is the active question, show the recorder below it
    if st.session_state.active_question == idx:
        st.write(f"Recording for Question {idx + 1}:")
        audio_bytes = st_audiorec()

        # If audio is recorded, save it in session state
        if audio_bytes:
            st.session_state.audio_responses[questions[idx]] = audio_bytes
            st.success(f"Recording for Question {idx + 1} saved!")
            st.session_state.active_question = None  # Reset active question after saving

# Submit button
if st.button("Submit All Responses"):
    if len(st.session_state.audio_responses) == len(
