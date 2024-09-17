import streamlit as st
from audiorecorder import audiorecorder
import requests
import base64

# Function to send audio to the external API
def send_to_api(question, audio_data):
    api_url = "https://your-api-endpoint.com/upload"  # Replace with actual API endpoint
    headers = {"Content-Type": "application/json"}
    payload = {
        "question": question,
        "audio": base64.b64encode(audio_data).decode('utf-8')
    }
    response = requests.post(api_url, json=payload, headers=headers)
    return response.status_code, response.text

# Main function for the Streamlit app
def main():
    st.title("Audio Recording Questionnaire")

    # Hardcoded questions
    questions = [
        "What is your name?",
        "What is your favorite color?",
        "Tell us about your favorite hobby."
    ]

    # Dictionary to store the recordings
    audio_recordings = {}

    # Loop through the questions and create the corresponding recording button
    for idx, question in enumerate(questions):
        st.write(f"**Question {idx+1}:** {question}")

        # Record button for the current question with unique key
        audio = audiorecorder("Record", "Recording...", key=f"audio_{idx}")

        # If there is a recorded audio, store it in the dictionary
        if len(audio) > 0:
            st.audio(audio.tobytes())
            audio_recordings[question] = audio.tobytes()

    # Submit button to send the recordings
    if st.button("Submit"):
        if audio_recordings:
            st.write("Submitting your responses...")
            for question, audio_data in audio_recordings.items():
                status_code, response_text = send_to_api(question, audio_data)
                if status_code == 200:
                    st.success(f"Successfully submitted answer for: {question}")
                else:
                    st.error(f"Failed to submit answer for: {question}, Error: {response_text}")
        else:
            st.warning("Please record at least one response before submitting.")

if __name__ == "__main__":
    main()
