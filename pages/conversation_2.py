from core.questions_workflow import run_workflow

run_workflow(
    conversation_name="Conversation 2.",
    image_name="images/conv_2.png",
    questions=["What sweets would you like to buy and for whom?"],
    questions_audio_files=["audios/conv_2/q1.wav"],
)
