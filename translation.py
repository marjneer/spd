from deep_translator import GoogleTranslator
from languages import lang_map
from PIL import Image
import pytesseract
import cv2
import numpy as np


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

    translator = GoogleTranslator()
    languages = translator.get_supported_languages(as_dict = True)
    translator.source = languages[source_lang] #here, source_lang is the dict key. eg. 'english'. it passes the lang code value to translator.source
    translator.target = languages[target_lang]
    return translator.translate(text)

def translate_image(file,source_lang,target_lang):
    im = Image.open(file)
    text = pytesseract.image_to_string(im,lang=lang_map[source_lang]['tess'])
    text = (text.strip()).lower()
    text = text.replace("\n", " ").replace("  ", " ")
    return translate_text(text,source_lang,target_lang)

def image_process(captured_image):
    image = Image.open(captured_image)
    # Convert to OpenCV format
    open_cv_image = np.array(image)
    # Convert to grayscale
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
