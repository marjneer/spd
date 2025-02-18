import streamlit as st
import json
from PIL import Image
from translation import translate_text,translate_image,languages_as_list,image_process
from languages import lang_map

# Load Lottie animation (Optional)
def load_lottie(filepath: str):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

st.set_page_config(page_title="Translation App", page_icon="🌐", layout="centered")
st.title("Translation App")

# Single unified input component
input_type = st.radio("Choose input type", ["Text", "Audio", "Image"], horizontal=True)


# Language Selection


# Unified Input Handling
if input_type == "Text":
    col1, col2 = st.columns(2)
    with col1:
        source_lang = st.selectbox("Source Language", languages_as_list, index=0)
    with col2:
        target_lang = st.selectbox("Target Language", languages_as_list, index=1)
    text_input = st.text_area("Enter text to translate", height=100)
    if st.button("Translate"):
        st.write(translate_text(text_input,source_lang,target_lang))
        st.success("Translated Text: [Placeholder for translated text]")
elif input_type == "Audio":
    audio_file = st.file_uploader("Upload audio file", type=["wav", "mp3"])
    if audio_file:
        st.audio(audio_file, format="audio/wav")
        if st.button("Translate Audio"):
            st.success("Translated Text: [Placeholder for translated text]")
elif input_type == "Image":
    col1, col2 = st.columns(2)
    with col1:
        source_lang = st.selectbox("Source Language", list(lang_map.keys()), index=0)
    with col2:
        target_lang = st.selectbox("Target Language", list(lang_map.keys()), index=1)
    option=st.radio("How will you give the image?",["Upload image","Open Camera"],horizontal=True)
    if option=="Upload image":
        image_to_translate = st.file_uploader("Upload image file", type=["jpg", "png", "jpeg","webp"])
        if image_to_translate:
            st.image(image_to_translate, caption="Uploaded Image", use_column_width=True)
    else:
        image_to_translate = st.camera_input("Take a picture to translate text")
        if image_to_translate is not None:
            # Open the captured image
            processed_image = image_process(image_to_translate)
            # Display the captured image
            st.image(processed_image, caption='Captured Image', use_column_width=True)
    if st.button("Translate Image"):
        st.write(translate_image(image_to_translate,source_lang,target_lang))
        st.success("Translated Text: [Placeholder for translated text]")

