from deep_translator import GoogleTranslator
from languages import *
from PIL import Image
import pytesseract
import cv2
import numpy as np
import streamlit as st
import sounddevice as sd
import wave
import speech_recognition as sr
from gtts import gTTS
import tempfile
import os


languages_as_list = list((GoogleTranslator().get_supported_languages(as_dict = True)).keys())
def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    """
    Translates the given text from source_lang to target_lang.

    :param text: Text to be translated
    :param source_lang: Source language code
    :param target_lang: Target language code
    :return: Translated text
    """
    if not text:
        return "Input text is empty."

    try:
        translator = GoogleTranslator()
        languages = translator.get_supported_languages(as_dict=True)
        
        if source_lang not in languages or target_lang not in languages:
            return "Error: Invalid language name. Please check supported languages."
        
        translator.source = languages[source_lang]
        translator.target = languages[target_lang]
        
        return translator.translate(text)
    except Exception as e:
        return f"Error: Translation failed. {str(e)}"

sample_rate = 44100
channels = 1
dtype = np.int16
def record_audio(duration):
    st.write("🔴 Recording... Speak now!")
    audio_data = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=channels, dtype=dtype)
    sd.wait()
    st.write("🛑 Recording stopped.")

    # Save to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
        filename = tmpfile.name
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(audio_data.tobytes())
    return filename


# Function to convert speech to text
def speech_to_text(audio_file,source_lang):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio_data,language=voice_lang_map[source_lang]['sr'])
        except sr.UnknownValueError:
            return None

def text_to_speech(text, target_lang):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
        tts = gTTS(text=text, lang=voice_lang_map[target_lang]["google"])
        tts.save(tmpfile.name)
        return tmpfile.name
    
# Remove previous translation audio
def clear_translation_audio():
    if "translation_audio" in st.session_state:
        try:
            os.remove(st.session_state["translation_audio"])
        except FileNotFoundError:
            pass  # File might already be deleted
        del st.session_state["translation_audio"]

def translate_image(file, source_lang, target_lang):
    """
    Extracts text from an image and translates it.

    :param file: Image file
    :param source_lang: Source language name (e.g., 'english')
    :param target_lang: Target language name (e.g., 'french')
    :return: Translated text or an error message
    """
    try:
        im = Image.open(file)
        
        # Ensure source_lang exists in tess_map
        if source_lang not in tess_map:
            return "Error: Unsupported source language for OCR."
        
        text = pytesseract.image_to_string(im, lang=tess_map[source_lang]['tess'])
        text = (text.strip()).lower()
        text = text.replace("\n", " ").replace("  ", " ")
        
        return translate_text(text, source_lang, target_lang)
    except FileNotFoundError:
        return "Error: File not found."
    except pytesseract.TesseractError:
        return "Error: OCR processing failed."
    except Exception as e:
        return f"Error: Image translation failed. {str(e)}"

def image_process(captured_image):
    """
    Processes an image for better OCR readability.

    :param captured_image: Input image file
    :return: Processed PIL image
    """
    try:
        image = Image.open(captured_image)
        # Convert to OpenCV format
        open_cv_image = np.array(image)
        
        # Ensure the image has color channels
        if len(open_cv_image.shape) == 2:  # Grayscale image
            gray_image = open_cv_image
        else:
            gray_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2GRAY)
        
        # Apply adaptive thresholding
        thresh_image = cv2.adaptiveThreshold(
            gray_image, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )
        
        # Convert back to PIL format
        processed_image = Image.fromarray(thresh_image)
        return processed_image
    except FileNotFoundError:
        return "Error: Image file not found."
    except Exception as e:
        return f"Error: Image processing failed. {str(e)}"

