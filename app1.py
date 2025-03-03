import streamlit as st
import json
from translation import *
from languages import *
from handle_translation import *
from pydub import AudioSegment
import os
from streamlit_lottie import st_lottie
import json

st.set_page_config(page_title="Translation App", page_icon="🌐", layout="centered")
st.title("Translation App")

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

lottie_animation = load_lottiefile("trans_animate.json")
st_lottie(lottie_animation, speed=1, height=200, key="initial")

# Single unified input component
input_type = st.radio("Choose input type", ["Text", "Audio", "Image"], horizontal=True)
handle_translation(input_type)

