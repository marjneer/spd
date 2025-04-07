import streamlit as st
import json
from translation import *
from languages import *
from handle_translation import *
from streamlit_lottie import st_lottie
import json

st.set_page_config(page_title="TranslateIt", page_icon="🌐", layout="centered")
st.title("TranslateIt")

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

lottie_animation = load_lottiefile("trans_animate.json")
st_lottie(lottie_animation, speed=1, height=200, key="initial")

# Ensure theme state is stored
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False  # Default to Light Mode

if st.sidebar.button("🌙 Toggle Dark Mode" if not st.session_state.dark_mode else "☀️ Toggle Light Mode"):
    st.session_state.dark_mode = not st.session_state.dark_mode  # Toggle the mode

# Define Theme Colors
theme = {
    "light": {"bg": "#FFFFFF", "text": "#000000", "button": "#DDDDDD", "hover": "#BBBBBB", "input_bg": "#F5F5F5"},
    "dark": {"bg": "#000000", "text": "#FFFFFF", "button": "#333333", "hover": "#555555", "input_bg": "#222222"}
}

mode = "dark" if st.session_state.dark_mode else "light"
st.markdown(
    f"""
    <style>
        .stApp {{background-color: {theme[mode]['bg']}; color: {theme[mode]['text']};}}
        h1, h2, h3, h4, h5, h6, p, span, div, label, .stTextInput label, .stTextArea label, .stSelectbox label, .stRadio label {{color: {theme[mode]['text']} !important;}}
        div.stButton > button {{background-color: {theme[mode]['button']} !important; color: {theme[mode]['text']} !important; border-radius: 10px; padding: 10px; transition: 0.3s;}}
        div.stButton > button:hover {{background-color: {theme[mode]['hover']} !important;}}
    </style>
    """,
    unsafe_allow_html=True
)

# Input Type Selection
st.sidebar.markdown("## 📝 Choose Input Type")
st.sidebar.markdown("---")
input_type = st.sidebar.radio("Select", ["Text", "Audio", "Image","Translate Document"], horizontal=True)

# Main Content Display
st.markdown("---")
st.markdown(f"### 🚀 Translating from {input_type}...")
handle_translation(input_type)

