from googletrans import Translator, constants
from pprint import pprint
#import library
import warnings
#from gtts import gTTS
import os

import time
import pyttsx3
warnings.filterwarnings("ignore")
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import speech_recognition as sr
class CaesarLangTranslate:
    def __init__(self) -> None:
        self.translator = Translator()
    @classmethod
    def all_languages():
        print("Total supported languages:", len(constants.LANGUAGES))
        print("Languages:")
        pprint(constants.LANGUAGES)
    def translate(self,text,src="fr",lang="en",verbose=False):
        translation = self.translator.translate(text,src=src,dest=lang)
        print(f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")
        if verbose == True:
            pprint(translation.extra_data)
        return translation.origin,translation.text,translation.dest

# Initialize recognizer class (for recognizing the speech)
engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)
recognizer = sr.Recognizer()

def speak(text,whisper_mode=None):
    if whisper_mode == 0:
        engine.say(text)
        engine.runAndWait()

def caesar_recognition(language="en-US"):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source,duration=1)
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio,language=language)
            print(said)
        except Exception as e:
            print("Exception: " + str(e))

    return said.lower()
WAKE = "hello caesar"
while True:
    print("Listening")
    text = caesar_recognition()

    if WAKE in text:
        print("How can I help you sir?")
        speak("How can I help you sir?",0)
        text = caesar_recognition()
        TRANSLATION_MODE = "translate"
        if TRANSLATION_MODE in text:
            print("What is your translation?")
            speak("What is your translation?",0)
            text = caesar_recognition(language="fr-FR")
            caesarlangtranslate = CaesarLangTranslate()
            tranlationinfo = caesarlangtranslate.translate(text)
            print(tranlationinfo)
            speak(tranlationinfo[1],0)
        else:
            print(text)