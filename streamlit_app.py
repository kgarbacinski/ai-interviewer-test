import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings, AudioProcessorBase
import numpy as np
import av

st.title("Interview Questions.")

PREDEFINED_QUESTIONS = ["What are your strengths?", "How are you?"]
NUM_AUDIO_INPUTS = len(PREDEFINED_QUESTIONS)  # Number of audio inputs

# Initialize session state for recorded audio data and recording status
if "recorded_audios" not in st.session_state:
    st.session_state.recorded_audios = [None] * NUM_AUDIO_INPUTS
if "uploaded_audios" not in st.session_state:
    st.session_state.uploaded_audios = [None] * NUM_AUDIO_INPUTS
if "is_recording" not in st.session_state:
    st.session_state.is_recording = [False] * NUM_AUDIO_INPUTS  # Status of recording for each stage


class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.frames = []

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        # Convert audio frame to numpy array
        audio_data = frame.to_ndarray()
        
        # Append to the frames buffer
        self.frames.append(audio_data)

        return frame

    def get_audio_data(self):
        # Combine all the audio frames
        if len(self.frames) > 0:
            return np.concatenate(self.frames, axis=1)
        return None


def handle_recording(i, webrtc_ctx):
    """Handle the audio recording using WebRTC."""
    if webrtc_ctx.state.playing:
        st.session_state.is_recording[i] = True
        st.write(f"Recording for question {i+1} is active...")
    else:
        if st.session_state.is_recording[i]:
            st.write(f"Recording for question {i+1} has stopped.")
            st.session_state.is_recording[i] = False
            audio_data = webrtc_ctx.audio_processor.get_audio_data()
            if audio_data is not None:
                st.session_state.recorded_audios[i] = audio_data
                st.write(f"Audio for question {i+1} recorded successfully.")
        else:
            st.write(f"Recording for question {i+1} is not active.")


for i in range(NUM_AUDIO_INPUTS):
    st.header(PREDEFINED_QUESTIONS[i])
    option = st.selectbox(f"Choose input method for Audio {i+1}", ("Record", "Upload"), key=f"input_method_{i}")

    if option == "Record":
        st.write("Click on start to record audio.")
        
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
            audio_processor_factory=AudioProcessor,  # Add audio processor
            async_processing=True,
        )

        # Handle recording status and collect data
        if webrtc_ctx.state.playing:
            handle_recording(i, webrtc_ctx)

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
