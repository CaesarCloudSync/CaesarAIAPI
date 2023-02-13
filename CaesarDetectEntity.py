import re
import spacy
import gtts
class CaesarDetectEntity:
  def __init__(self):
    self.languages = {v: k for k, v in gtts.lang.tts_langs().items()}
    self.NER = spacy.load("en_core_web_sm")
    self.main_entities = {"email":"ORG","translate":"NORP"}
  def index_of_word(self,word,text):
    matches_start = re.finditer(word.lower(), text.lower())
    matches_position_start = [match.start() for match in matches_start]

    # matches_position_end will be a list of ending index positions
    matches_end = re.finditer(word.lower(), text.lower())
    matches_position_end = [match.end() for match in matches_end]
    return matches_position_start[0],matches_position_end[0]
  def show_entites(self,text):
    text1 = self.NER(text)
    for word in text1.ents:
        print(word.text,word.label_)
  def run(self,word,text,entity="NORP"):
    try:
      text1= self.NER(text)
      target_lang = [word.text for word in text1.ents if word.label_ == entity][0]
      source_text = text[self.index_of_word(word,text)[-1]:self.index_of_word(target_lang,text)[0]].replace(" to","").replace(" into","").replace(" in","").strip()
      #api_call = f"translate({source_text},'{self.languages[target_lang.capitalize()]}')"
      return source_text,self.languages[target_lang.capitalize()]
    except (IndexError,KeyError) as kex:
      source_text = text[self.index_of_word(word,text)[-1]:].replace(" to","").replace(" into","").replace(" in","").strip()
      #api_call = f"translate({source_text},'{self.languages[target_lang.capitalize()]}')"
      languages = None
      return source_text,languages