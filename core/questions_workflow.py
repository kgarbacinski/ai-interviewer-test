import requests
import streamlit as st
from audiorecorder import audiorecorder


def send_to_api(filename: str):
    response = requests.post(
        "https://api.hume.ai/v0/registry/files/upload",
        headers={
            "X-Hume-Api-Key": "BBSW8A0GEX4B4X0DDn2ySxJdcqdJxiau5lVNX6BerXIkn962"
        },
        files={
            'file': (filename, open(filename, 'rb'), 'audio/wav')
        }
    )
    st.write(response.status_code)
    return response.status_code, response.json()


def get_emotions(file_id: str):
    response = requests.get(
        f"https://api.hume.ai/v0/registry/files/{file_id}/predictions",
        headers={
            "X-Hume-Api-Key": "BBSW8A0GEX4B4X0DDn2ySxJdcqdJxiau5lVNX6BerXIkn962"
        },
    )
    st.write(response.status_code)
    return response.status_code, response.text


def run_workflow():
    st.title("Audio Recording Questionnaire")
    st.image("images/snickers.png", caption="Images showing a snickers bar")

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
            filename = f"audio_{idx}.wav"

            # To save audio to a file, use pydub export method:
            audio.export(filename, format="wav")

            st.audio(audio.export().read())
            audio_recordings[filename] = audio.export().read()

    if st.button("Submit"):
        if audio_recordings:
            st.write("Submitting your responses...")
            for filename, audio_data in audio_recordings.items():
                status_code, response_text = send_to_api(filename)
                if status_code == 201:
                    st.success(f"Successfully submitted answer for audio: {filename}")
                    file_id = response_text['file']['id']
                    status_code, response_text = get_emotions(file_id)

                    if status_code == 200:
                        st.write(str(response_text))
                    else:
                        st.error(f"Failed to get emotions for audio: {filename}, Error: {response_text}")
                else:
                    st.error(f"Failed to submit answer for audio: {filename}, Error: {response_text}")
        else:
            st.warning("Please record at least one response before submitting.")
