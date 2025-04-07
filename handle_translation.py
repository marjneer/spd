import streamlit as st
import os
from pydub import AudioSegment
from translation import *
from languages import *
from docx import Document
import certifi
import requests


def handle_translation(input_type):
    col1, col2 = st.columns(2)
    
    if input_type != "Translate Document":
        with col1:
            source_lang = st.selectbox("Source Language", get_languages(input_type), index=0)
    else:
        source_lang = None  # No source language needed for document translation

    with col2:
        target_lang = st.selectbox("Target Language", get_languages(input_type), index=1)
    
    if input_type == "Text":
        text_input = st.text_area("Enter text to translate", height=100)
        if st.button("Translate"):
            if text_input.strip():
                translation = translate_text(text_input, source_lang, target_lang)
                st.success(f"Translated Text: {translation}")
            else:
                st.error("Please enter text to translate.")
        st.markdown("</div>", unsafe_allow_html=True)  # Closing the div
    
    elif input_type == "Audio":
        handle_audio_translation(source_lang, target_lang)
    
    elif input_type == "Image":
        handle_image_translation(source_lang, target_lang)

    elif input_type == "Translate Document":
        st.sidebar.header("🔑 API Configuration")
        api_token = st.sidebar.text_input("Enter your APYHub API Key for document translation", type="password")
        uploaded_file = st.file_uploader("Choose a DOCX file", type=["docx"])
        language = target_lang  # Directly using the selected target language
        lang_code = api_langs.get(language)
        

        if uploaded_file and language:
            if not api_token:
                st.error("⚠️ Please enter your APYHub API key in the sidebar.")
                return None
            st.info("Translating document... Please wait.")
            translated_file_path = translate_document(uploaded_file, lang_code, api_token)
            if translated_file_path:
                with open(translated_file_path, "rb") as file:
                    st.download_button(
                        label="Download Translated Document",
                        data=file,
                        file_name="translated_document.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )

def get_languages(input_type):
    if input_type == "Text":
        return languages_as_list
    elif input_type == "Audio":
        return list(voice_lang_map.keys())
    elif input_type == "Image":
        return list(tess_map.keys())
    elif input_type == "Translate Document":
        return list(api_langs.keys())
    return []

def handle_audio_translation(source_lang, target_lang):
    input_method = st.selectbox("Select Input Method:", ["Upload Audio File", "Record Live"])
    
    audio_file = None
    if input_method == "Upload Audio File":
        uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3", "aac"])
        if uploaded_file:
            audio_file = convert_audio_if_needed(uploaded_file)
    elif input_method == "Record Live":
        duration = st.slider("⏱ Select Recording Duration (seconds)", min_value=3, max_value=30, value=5)
        if st.button("Start Recording"):
            audio_file = record_audio(duration)
    
    if audio_file:
        st.audio(audio_file)
        text = speech_to_text(audio_file, source_lang)
        if text:
            st.write("Transcribed Text:", text)
            translation = translate_text(text, source_lang, target_lang)
            st.success(f"Translation: {translation}")
            st.session_state["translation_audio"] = text_to_speech(translation, target_lang)
            
            if st.button("🔊 Speak Translation"):
                st.audio(st.session_state["translation_audio"])
        else:
            st.error("⚠️ Could not recognize speech.")
        
        os.remove(audio_file)

def convert_audio_if_needed(uploaded_file):
    if uploaded_file.name.endswith('.mp3'):
        sound = AudioSegment.from_mp3(uploaded_file)
        sound.export("uploaded.wav", format="wav")
        return "uploaded.wav"
    return uploaded_file

def handle_image_translation(source_lang, target_lang):
    option = st.radio("How will you give the image?", ["Upload image", "Open Camera"], horizontal=True)
    image_to_translate = None
    
    if option == "Upload image":
        image_to_translate = st.file_uploader("Upload image file", type=["jpg", "png", "jpeg", "webp"])
    else:
        image_to_translate = st.camera_input("Take a picture to translate text")
    
    if image_to_translate:
        st.image(image_to_translate, caption="Selected Image", use_column_width=True)
        if st.button("Translate Image"):
            translation = translate_image(image_to_translate, source_lang, target_lang)
            st.success(f"Translated Text: {translation}")
    else:
        st.error("Please provide an image for translation.")

def translate_document(file, target_language, api_token):
    url = 'https://api.apyhub.com/translate/file'
    
    headers = {'apy-token': api_token}
    data = {'language': target_language}
    
    try:
        files = {'file': file}
        response = requests.post(url, headers=headers, files=files, data=data, verify=certifi.where())

        if response.status_code == 200:
            response_json = response.json()
            translated_text = response_json.get("translation")

            if not translated_text:
                st.error("No translated text found. Check API response structure.")
                return None

            # Load original DOCX file
            doc = Document(file)
            paragraphs = doc.paragraphs

            # Replace original text with translated text
            translated_lines = translated_text.split("\n")
            for i, para in enumerate(paragraphs):
                if i < len(translated_lines):
                    para.text = translated_lines[i]

            # Save translated document
            output_path = "translated_document.docx"
            doc.save(output_path)
            return output_path
        else:
            st.error(f"Failed with status code {response.status_code}. Error: {response.json().get('message', 'Unknown error')}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error making API request: {e}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None
