from core.questions_workflow import run_workflow

run_workflow(conversation_name="Conversation 1.", image_name="images/conv_1.png",
             questions=["How do you normally shop online?", "Have you ever purchased sweets online?"],
             questions_audio_files=["audios/conv_1/q1.wav", "audios/conv_1/q2.wav"])
