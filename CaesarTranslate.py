from googletrans import Translator, constants
from pprint import pprint
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
class CaesarLangTranslate:
    def __init__(self) -> None:
        self.translator = Translator()
    @classmethod
    def all_languages():
        print("Total supported languages:", len(constants.LANGUAGES))
        print("Languages:")
        pprint(constants.LANGUAGES)
    def translate(self,text,src="fr",lang="en",verbose=False,response=False):
        if response == True:
            src = "en"
            
            #lang = self.translator.detect(text).lang
        elif response == False:
            src = self.translator.detect(text).lang
        #print(src)
        translation = self.translator.translate(text,src=src,dest=lang)
        #print(f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")
        if verbose == True:
            pprint(translation.extra_data)
        return translation.origin,translation.text,translation.dest,src
    
