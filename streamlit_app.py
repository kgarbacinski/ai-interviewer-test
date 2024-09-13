import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
import asyncio
import numpy as np
import queue

st.title("Interview Questions.")

PREDEFINED_QUESTIONS = ["What are your strenghts?", "How are you?"]
NUM_AUDIO_INPUTS = len(PREDEFINED_QUESTIONS)  # Number of audio inputs

recorded_audios = [None] * NUM_AUDIO_INPUTS
uploaded_audios = [None] * NUM_AUDIO_INPUTS



for i in range(NUM_AUDIO_INPUTS):
    st.header(PREDEFINED_QUESTIONS[i])
    option = st.selectbox(f"Choose input method for Audio {i+1}", ("Record", "Upload"), key=f"input_method_{i}")

    if option == "Record":
        st.write("Click on start to record audio.")
        audio_queue = queue.Queue()
        
        webrtc_ctx = webrtc_streamer(
            key=f"audio_{i}",
            mode=WebRtcMode.SENDONLY,
            audio_receiver_size=256,
            client_settings=ClientSettings(
                rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
                media_stream_constraints={
                    "audio": True,
                    "video": False,
                },
            ),
            async_processing=True,
        )
        
        if webrtc_ctx.audio_receiver:
            audio_frames = []
            status_indicator = st.empty()
            status_indicator.write("Recording...")
            try:
                while True:
                    audio_frame = webrtc_ctx.audio_receiver.get_frame(timeout=1)
                    audio_frames.append(audio_frame.to_ndarray().flatten())
                    if not webrtc_ctx.state.playing:
                        break
            except queue.Empty:
                pass
            status_indicator.write("Recording stopped.")
            if audio_frames:
                audio_data = np.concatenate(audio_frames, axis=0)
                recorded_audios[i] = audio_data
    else:
        uploaded_file = st.file_uploader(f"Upload Audio {i+1}", type=["wav", "mp3"], key=f"uploaded_file_{i}")
        if uploaded_file is not None:
            uploaded_audios[i] = uploaded_file

if st.button("Submit"):
    st.header("Processing Results")
    # Combine recorded and uploaded audios
    audio_inputs = []
    for i in range(NUM_AUDIO_INPUTS):
        if recorded_audios[i] is not None:
            st.write(f"Audio {i+1} was recorded.")
            st.write(f"Recorded audio data shape: {recorded_audios[i].shape}")
            # Here you can add code to process recorded_audios[i]
            audio_inputs.append(recorded_audios[i])
        elif uploaded_audios[i] is not None:
            st.write(f"Audio {i+1} was uploaded.")
            st.audio(uploaded_audios[i])
            # Here you can add code to process uploaded_audios[i]
            audio_inputs.append(uploaded_audios[i])
        else:
            st.write(f"No audio input for Audio {i+1}.")
    st.success("All audios have been processed.")
