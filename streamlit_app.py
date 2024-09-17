import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
import numpy as np
import queue

st.title("Interview Questions.")

PREDEFINED_QUESTIONS = ["What are your strengths?", "How are you?"]
NUM_AUDIO_INPUTS = len(PREDEFINED_QUESTIONS)  # Number of audio inputs

# Initialize session state for recorded audio data
if "recorded_audios" not in st.session_state:
    st.session_state.recorded_audios = [None] * NUM_AUDIO_INPUTS
if "uploaded_audios" not in st.session_state:
    st.session_state.uploaded_audios = [None] * NUM_AUDIO_INPUTS
if "audio_frames" not in st.session_state:
    st.session_state.audio_frames = [None] * NUM_AUDIO_INPUTS

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
            status_indicator = st.empty()

            # Only start collecting audio if the context is playing
            if webrtc_ctx.state.playing:
                status_indicator.write("Recording...")
                try:
                    audio_frame = webrtc_ctx.audio_receiver.get_frame(timeout=1)
                    audio_ndarray = audio_frame.to_ndarray().flatten()

                    # Accumulate audio frames for the current question
                    if st.session_state.audio_frames[i] is None:
                        st.session_state.audio_frames[i] = audio_ndarray
                    else:
                        st.session_state.audio_frames[i] = np.concatenate(
                            [st.session_state.audio_frames[i], audio_ndarray]
                        )
                except queue.Empty:
                    pass

            # When the user clicks stop (automatically stops when stream stops)
            if not webrtc_ctx.state.playing and st.session_state.audio_frames[i] is not None:
                status_indicator.write("Recording stopped.")
                st.session_state.recorded_audios[i] = st.session_state.audio_frames[i]
    else:
        uploaded_file = st.file_uploader(f"Upload Audio {i+1}", type=["wav", "mp3"], key=f"uploaded_file_{i}")
        if uploaded_file is not None:
            st.session_state.uploaded_audios[i] = uploaded_file

# Button to submit the audio responses
if st.button("Submit"):
    st.header("Processing Results")
    audio_inputs = []
    
    for i in range(NUM_AUDIO_INPUTS):
        if st.session_state.recorded_audios[i] is not None:
            st.write(f"Audio {i+1} was recorded.")
            st.write(f"Recorded audio data shape: {st.session_state.recorded_audios[i].shape}")
            # Here you can add code to process the recorded audio
            audio_inputs.append(st.session_state.recorded_audios[i])
        elif st.session_state.uploaded_audios[i] is not None:
            st.write(f"Audio {i+1} was uploaded.")
            st.audio(st.session_state.uploaded_audios[i])
            # Here you can add code to process the uploaded audio
            audio_inputs.append(st.session_state.uploaded_audios[i])
        else:
            st.write(f"No audio input for Audio {i+1}.")
    
    st.success("All audios have been processed.")
