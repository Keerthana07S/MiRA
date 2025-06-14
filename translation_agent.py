from googletrans import Translator #to translate from language user speaks to English
from typing import Tuple #to specify types of function parameters
from langdetect import detect, detect_langs #to detect the language of the text

class TranslationAgent:
    def __init__(self, text_to_translate: str):
        self.text_to_translate = text_to_translate #text response from the user

    def detect_language(self, text_to_translate) -> str:
        language = detect(text_to_translate) #detect language
        return language 
    
    def translate_text(self, text_to_translate: str, current_language, target_language: str = "en") -> str:
        translated_text = Translator().translate(text_to_translate, src=current_language, dest=target_language) #translate to English
        return translated_text.text
