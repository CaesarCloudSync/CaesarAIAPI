from gtts import gTTS

class CaesarVoice:
    @classmethod
    def synthesise(self,text,filename="temp.wav",lang='en'):
        caesargtts = gTTS(text=text, lang=lang)
        caesargtts.save(filename)