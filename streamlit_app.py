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

if 'current_question' not in st.session_state:
    st.session_state.current_question = 0  # Start at the first question

st.title("Voice-based Questionnaire")

# Helper function to save audio and move to the next question
def save_audio_and_next(audio_bytes, question_idx):
    if audio_bytes is not None:
        st.session_state.audio_responses[questions[question_idx]] = audio_bytes
        st.success(f"Recording for '{questions[question_idx]}' saved!")
        # Move to the next question
        if question_idx + 1 < len(questions):
            st.session_state.current_question += 1
        else:
            st.session_state.current_question = "submit"  # Go to submit page

# Display the current question page
current_idx = st.session_state.current_question

if isinstance(current_idx, int):
    st.subheader(f"Question {current_idx + 1}: {questions[current_idx]}")
    
    # Check if the user has already recorded an answer for this question
    if questions[current_idx] in st.session_state.audio_responses:
        st.write("Recorded Answer: (Re-record if needed)")
        st.audio(st.session_state.audio_responses[questions[current_idx]], format="audio/wav")
    else:
        st.write("No answer recorded yet.")

    # Audio recorder
    audio_bytes = st_audiorec()

    # Save and move to the next question button
    if audio_bytes is not None:
        if st.button("Save and Next"):
            save_audio_and_next(audio_bytes, current_idx)

else:
    # Final submission page
    st.subheader("Review and Submit Your Responses")
    
    # Display all recorded responses
    for idx, question in enumerate(questions):
        st.write(f"**Question {idx + 1}: {question}**")
        if question in st.session_state.audio_responses:
            st.audio(st.session_state.audio_responses[question], format="audio/wav")
        else:
            st.write("_No answer recorded._")

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
    
    # Add a button to go back and review questions
    if st.button("Go Back"):
        st.session_state.current_question = len(questions) - 1  # Go back to the last question
