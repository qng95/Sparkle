import os
import logging
import time
import random
from enum import Enum

import streamlit as st
from streamlit.components.v1 import html as st_html
from st_audiorec import st_audiorec
from streamlit_lottie import st_lottie

from sparkle import simpleauth

st.set_page_config(page_title="Sparkle", page_icon="🐸", layout="wide")

def init_session_data():
    logging.info("Initializing session data...")
    st.session_state.recording = None
    st.session_state.embedded_canva = None


def init_format():
    logging.info("Initializing page format...")
    st.markdown(
        """
    <style>
    .st-emotion-cache-k3d5su.e1nzilvr5 {
        margin-bottom: 0px;
    }  
        
    </style>
    """,
        unsafe_allow_html=True,
    )


@st.cache_data
def add_header():
    logging.info("Rendering header at app startup ...")
    #st.markdown("<h1 style='text-align: center;'>🐸 Sparkle 🐸</h1>", unsafe_allow_html=True)
    #st_lottie("https://lottie.host/bc17f388-eb90-4d2f-b6d7-7e7ebc949de4/mIru5msWdS.json", quality="high", height=100,
    #          speed=1)
    #st.divider()


def add_sidebar():
    logging.info("Rendering sidebar...")
    with st.sidebar:
        st.markdown("<h1 style='text-align: center; font-size: 2.5rem;'>🐸 Sparkle 🐸</h1>", unsafe_allow_html=True)
        st_lottie("https://lottie.host/bc17f388-eb90-4d2f-b6d7-7e7ebc949de4/mIru5msWdS.json", quality="high",
                  height=100,
                  speed=1)
        st.divider()

        st.markdown("<h1 style='text-align: center;'>🎙Ghi Hình 🎙️</h1>", unsafe_allow_html=True)
        #wav_audio_data = st_audiorec()
        #if wav_audio_data:
        #    st.session_state.recording = wav_audio_data
        #st.divider()

        with st.container():
            st_html(
                html="""
                <div>
                    <div>
                        <video controls autoplay muted playsinline id="videoRecorded" style="width:100%;height=200px;"></video>
                    </div>
                    <div>
                        <button type="button" id="buttonStart">Start</button>
                        <button type="button" id="buttonStop" disabled>Stop</button>
                        <button type="button" id="buttonDownload" disabled>Download</button>
                    </div>
                    <script type="text/javascript">
                        async function main () {
                            const buttonStart = document.querySelector('#buttonStart')
                            const buttonStop = document.querySelector('#buttonStop')
                            const buttonDownload = document.querySelector('#buttonDownload')
                            
                            const videoRecorded = document.querySelector('#videoRecorded')
                            
                            const stream = await navigator.mediaDevices.getUserMedia({ // <1>
                                video: true,
                                audio: true,
                            })
                            
                            // videoRecorded.srcObject = stream
                            
                            if (!MediaRecorder.isTypeSupported('video/webm')) { // <2>
                                console.warn('video/webm is not supported')
                            }
                            
                            const mediaRecorder = new MediaRecorder(stream, { // <3>
                                mimeType: 'video/webm',
                            })
                            
                            buttonStart.addEventListener('click', () => {
                                mediaRecorder.start() // <4>
                                videoRecorded.srcObject = stream
                                buttonStart.setAttribute('disabled', '')
                                buttonDownload.setAttribute('disabled', '')
                                buttonStop.removeAttribute('disabled')
                            })
                            
                            buttonStop.addEventListener('click', () => {
                                buttonStop.setAttribute('disabled', '')
                                mediaRecorder.stop() // <5>
                                videoRecorded.srcObject = null
                                videoRecorded.muted = false
                                videoRecorded.autoplay = false
                                videoRecorded.controls = true
                            })
                            
                            mediaRecorder.addEventListener('dataavailable', event => {
                                buttonStart.removeAttribute('disabled')
                                buttonDownload.removeAttribute('disabled')
                                videoRecorded.src = URL.createObjectURL(event.data) // <6>
                            })
                            
                            buttonDownload.addEventListener('click', () => {
                                const a = document.createElement('a')
                                a.download = 'video.webm'
                                a.href = videoRecorded.src
                                a.click()
                            })
                        }
                        
                        main()
                    </script>
                </div>
                """,
                height=390,
                scrolling=True,
            )

        st.divider()

        #st.markdown("""<iframe style="width:100%;max-width:360px;height:360px;"
        #            src="https://stopwatch-app.com/widget/stopwatch?theme=dark&color=green"
        #            frameborder="0"></iframe>""", unsafe_allow_html=True)

        #st.markdown("""<iframe style="width:100%;max-width:360px;height:360px;"
        #            src="https://stopwatch-app.com/widget/timer?theme=dark&color=green&hrs=0&min=60&sec=0"
        #            frameborder="0"></iframe>""", unsafe_allow_html=True)

        st.markdown("""<iframe src="https://giorgiark.github.io/stopwatch2.0/" width="100%" height="100%" border-radius="100px" style="height:200px;"></iframe>""", unsafe_allow_html=True)


def app_start():
    def on_start_btn_click():
        ...

    st.button("START", key="start-btn", on_click=on_start_btn_click(), type="primary", disabled=False,
              use_container_width=True)


def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting Sparkle app...")

    if not simpleauth.auth():
       st.stop()

    init_session_data()
    init_format()

    add_header()
    add_sidebar()

    def on_submit_btn_click():
        pass

    with st.container():
        canva_embeded = st.text_area(
            label="Nhúng thuyết trình Canva",
            placeholder="Dán embedded HTML Canva code vào đây!",
            key="canva_embeded",
        )
        button = st.button("Bắt đầu", key="button", on_click=on_submit_btn_click)
        if button:
            st.balloons()
            random_sound = random.choice(["1.mp3", "2.mp3", "3.mp3", "4.mp3"])
            st.audio(os.path.join(os.path.abspath(os.path.dirname(__file__)), "sparkle", "sound", random_sound),
                     format="audio/mpeg", end_time="1m", autoplay=True)

            left_co, cent_co, last_co = st.columns(3)
            with left_co:
                st.image(image=os.path.join(os.path.abspath(os.path.dirname(__file__)), "sparkle", "image", "chaiyo.png"))
            with cent_co:
                st.image(image=os.path.join(os.path.abspath(os.path.dirname(__file__)), "sparkle", "image", "cheer-up-cheer.gif"))
            with last_co:
                st.image(image=os.path.join(os.path.abspath(os.path.dirname(__file__)), "sparkle", "image", "positive.png"))

            st.markdown(canva_embeded, unsafe_allow_html=True)


main()
