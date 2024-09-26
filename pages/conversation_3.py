from core.questions_workflow import run_workflow

run_workflow(
    conversation_name="Conversation 3.",
    image_name="images/conv_3.png",
    questions=["How do you like the product?", "Can you easily navigate on this page?"],
    questions_audio_files=["audios/conv_3/q1.wav", "audios/conv_3/q2.wav"],
)
