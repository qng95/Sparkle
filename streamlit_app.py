import os
import logging
import time
from enum import Enum

import streamlit as st
from st_audiorec import st_audiorec
from streamlit_lottie import st_lottie

from sparkle import simpleauth

st.set_page_config(page_title="Sparkle", page_icon="🐸")

CHAT_AVATAR = {
    'user': '🤓',
    'assistant': '🐸'
}


class Stage(str, Enum):
    # When the app is started or refreshed with F5 in the browser
    start_up = "start_up"

    welcome = "welcome"
    presentation_structure = "presentation_structure"
    recording = "recording"
    recording_transcript = "recording_transcript"
    anlysis = "analysis"
    summary = "summary"


def init_session_data():
    logging.info("Initializing session data...")
    if "recording" not in st.session_state:
        st.session_state.recording = None

    if "messages" not in st.session_state:
        logging.error("WHAT THE HELL")
        st.session_state.messages = []

    if "presentation_structure" not in st.session_state:
        st.session_state.presentation_structure = []

    if "recording_transcript" not in st.session_state:
        st.session_state.recording_transcript = None

    if "stage" not in st.session_state:
        st.session_state.stage = Stage.start_up


def init_format():
    logging.info("Initializing page format...")
    st.markdown(
        """
    <style>
        .stChatMessage.st-emotion-cache-janbn0 {
            flex-direction: row-reverse;
            text-align: right;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )


def print_as_stream(input: str):
    def stream_generator(s: str):
        for word in s.split(" "):
            yield word + " "
            time.sleep(0.01)

    st.write_stream(stream_generator(s=input))


@st.cache_data
def add_header():
    logging.info("Rendering header at app startup ...")
    st.markdown("<h1 style='text-align: center;'>🐸 Sparkle 🐸</h1>", unsafe_allow_html=True)
    st_lottie("https://lottie.host/bc17f388-eb90-4d2f-b6d7-7e7ebc949de4/mIru5msWdS.json", quality="high", height=100,
              speed=1)
    st.divider()


def add_sidebar():
    logging.info("Rendering sidebar...")
    with st.sidebar:
        st.markdown("<h1 style='text-align: center;'>🎙️Recorder 🎙️</h1>", unsafe_allow_html=True)
        wav_audio_data = st_audiorec()

        if wav_audio_data:
            st.session_state.recording = wav_audio_data


def ai_answer(response):
    with st.chat_message("assistant", avatar=CHAT_AVATAR["assistant"]):
        print_as_stream(response)
    st.session_state.messages.append({"role": "assistant", "content": response})


def generate_next_ai_response(user_input):
    match st.session_state.stage:
        case Stage.welcome:
            if user_input.strip().lower() == "yes":
                st.session_state.stage = Stage.presentation_structure

                ai_answer("Great! Now let's start with the structure of your presentation.")
                ai_answer("Can you tell me the brief overview on your presentation ?")
                ai_answer("  * What is the topic ?")
                ai_answer("  * What is the planned agenda ?")
                ai_answer("  * What are the main points that you would like to discuss ?")
                ai_answer("  * What is the final conclusion that you would like to make ?")
                ai_answer("You can type as much as you want. I am here to listen. 😊")
                ai_answer("Then whenever you feel ready, just type 'I'm done' - without quote - into the chat. 😉")

            else:
                ai_answer("If you ready, just type 'yes' - without quote - into the chat. 🙄")

        case Stage.presentation_structure:
            if user_input.strip().lower() == "i'm done":
                st.session_state.stage = Stage.recording

                ai_answer("I have noted down the structure of your presentation.")
                ai_answer("Awesome! Now, let's start recording your presentation.")
                ai_answer("I'll show you how to record your presentation.")
                ai_answer("When you're ready, press the 'Start Recording' button on left hand side to record your presentation. 🎙️")
                ai_answer(
                    "When you finished your presentation press 'Stop' button. Then you can listen to your presentation again by pressing play ▶️ button.️")
                ai_answer("If you want to record again, just press 'Reset' button and start again. 🔄")
                ai_answer("To download the recording to your machine for saving then press 'Download' button. 📥")
                ai_answer("Now enjoy! When you happy with your presentation recording. Again, tell me 'I'm done'! 📝")
            else:
                st.session_state.presentation_structure.append(user_input)

        case Stage.recording:
            if user_input.strip().lower() == "i'm done":
                st.session_state.stage = Stage.recording_transcript

                st.balloons()
                ai_answer("Congratulation! You have finished your presentation rehearsal. Hurray 🎉🎉🎉🎉")
                ai_answer("Now, I'll create a transcript of your presentation. Then you can review it and edit it if you want. 🫣🫣")

                # TODO: Call the speech-to-text API to generate the transcript
            else:
                st.session_state.presentation_structure.append(user_input)

        case Stage.recording_transcript:
            if user_input.strip().lower() == "i'm done":
                st.session_state.stage = Stage.anlysis
            else:
                st.session_state.presentation_structure.append(user_input)


def handle_user_input(user_input):
    logging.info("Handling user input...")

    # Display user message in chat message container
    st.chat_message("user", avatar=CHAT_AVATAR["user"]).markdown(user_input)

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    generate_next_ai_response(user_input=user_input)


def chat_submit_handler(**kwargs):
    logging.info(f"Callback on user input submit: {kwargs}")


def start_chat():
    logging.info("Starting chat...")
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=CHAT_AVATAR[message["role"]]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Type something here...", on_submit=chat_submit_handler):
        handle_user_input(user_input=prompt)
    else:
        if st.session_state.stage == Stage.welcome:
            with st.chat_message("assistant", avatar=CHAT_AVATAR["assistant"]):
                print_as_stream("Hey mate! Anxious about your presentation? Don't worry, I gotcha' back. 😉")
                st.session_state.messages.append({"role": "assistant", "content": "Hey mate! Anxious about your presentation? Don't worry, I gotcha' back. 😉"})

                print_as_stream("We will work together to make your presentation a big success. 🚀")
                st.session_state.messages.append({"role": "assistant",
                                                  "content": "We will work together to make your presentation a big success. 🚀"})

                print_as_stream("Now, let's do it mate! 😎")
                st.session_state.messages.append({"role": "assistant",
                                                  "content": "Now, let's do it mate! 😎"})

                print_as_stream("When ever you feel ready. Answer with 'Yes'. 😉")
                st.session_state.messages.append({"role": "assistant",
                                                  "content": "When ever you feel ready. Answer with 'Yes'. 😉"})


def app_start():
    def on_start_btn_click():
        st.session_state.stage = Stage.welcome

    st.button("START", key="start-btn", on_click=on_start_btn_click(), type="primary", disabled=False,
              use_container_width=True)


def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting Sparkle app...")

    if not simpleauth.auth():
        st.stop()

    init_session_data()
    init_format()
    if st.session_state.stage == Stage.start_up:
        add_header()
        app_start()
    else:
        add_header()
        add_sidebar()
        start_chat()


main()
