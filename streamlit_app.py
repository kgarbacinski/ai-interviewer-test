import streamlit as st


def main():
    st.title("Intro")
    st.audio("audios/intro.wav", format="audio/wav")

    st.write("Text version:")
    st.write(
        "Welcome to the online interview! We will show you 3 internet pages one by one and ask you to answer a couple of questions."
    )
    st.write("Select the conversation from the sidebar to start answering questions.")


if __name__ == "__main__":
    main()
