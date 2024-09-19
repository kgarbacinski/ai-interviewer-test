import time

import pandas as pd
import requests
import streamlit as st
from audiorecorder import audiorecorder
import matplotlib.pyplot as plt


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
    return response.status_code, response.json()


def get_emotions(file_id: str):
    response = requests.get(
        f"https://api.hume.ai/v0/registry/files/{file_id}/predictions",
        headers={
            "X-Hume-Api-Key": "BBSW8A0GEX4B4X0DDn2ySxJdcqdJxiau5lVNX6BerXIkn962"
        },
    )
    return response.status_code, response.json()


def show_emotions_stats(grouped_predictions: list):
    for entry in grouped_predictions:
        for prediction in entry["predictions"]:
            text = prediction['text']
            emotions = prediction['emotions']

            st.write(f"Emotions for text: {text}")
            df = pd.DataFrame(emotions)
            top_4_emotions = df.nlargest(4, 'score')

            fig, ax = plt.subplots(figsize=(8, 6))
            ax.barh(top_4_emotions['name'], top_4_emotions['score'], color='skyblue')
            ax.set_xlabel('Score')
            ax.set_title('Top 4 Emotions by Score')
            ax.invert_yaxis()
            st.pyplot(fig)


def run_workflow():
    st.title("Questions Workflow")
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
                    st.success(f"Successfully submitted answer for audio: {filename}. Processing your response...")
                    file_id = str(response_text['file']['id'])

                    time.sleep(5) # hume ai takes some time to process the audio

                    status_code, response_json = get_emotions(file_id)

                    if status_code == 200:
                        show_emotions_stats(response_json['models']['prosody']['grouped_predictions'])
                    else:
                        st.error(f"Failed to get emotions for audio: {filename}, Error: {str(response_json)}")
                else:
                    st.error(f"Failed to submit answer for audio: {filename}, Error: {str(response_json)}")
        else:
            st.warning("Please record at least one response before submitting.")
