import unittest
import requests
class CaesarAPIUnit(unittest.TestCase):
    def createapitest(self):
        data = {"caesarapis":[{
  "api_name": "Caesar Translate",
  "auth": "none",
  "content_type": "application/json",
  "data": {"caesartranslate":"hello world","response":"true","language":"fr","triggerword":"translate"},
  "method": "POST ",
  "token": "none",
  "triggerwords": "translate",
  "url": "http://0.0.0.0:7860/caesarlangtranslate",
},
        {
  "api_name": "Caesar Send Text",
  "auth": "none",
  "content_type": "application/json",
  "data": {
    "text": "hello world",
  },
  "method": "POST ",
  "token": "none",
  "triggerwords": "send text",
  "url": "http://0.0.0.0:7860/caesartext",
}]}
        response = requests.post("http://0.0.0.0:7860/createcaesaraipi",json=data)
        print(response.json())
    def getapitest(self):
        response = requests.get("http://0.0.0.0:7860/getcaesaraipi")
        print(response.json())
    def triggerapitest(self):
        data = {"user_trigger":"translate"}
        response = requests.post("http://0.0.0.0:7860/triggerapi",json=data)
        print(response.json())
    def caesarvoicetest(self):
        data = {"text":"hello world"}
        response = requests.post("http://0.0.0.0:7860/caesarvoice",json=data)
        with open('textfile.wav', 'wb') as file:
            file.write(response.content)
        print(response)
    def caesarsummarize(self):
        with open("test.txt","r") as f:
            text = f.read()
        if len(text) < 4000:
            data = {"text":text}
            response = requests.post("http://0.0.0.0:7860/caesarsummarize",json=data)
            print(response.json())
        else:
            print("original text is too large")
    def caesarstockinfo(self):
        response = requests.post("http://0.0.0.0:7860/caesarstockinfo",json={"stock":"AAPL","start_date":"2023-02-05","end_date":"2023-02-07"})
        print(response.json())
    def caesarocr(self):
        import base64
        with open("artificial neural networks.png", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('UTF-8')
        #print(encoded_string)
        response = requests.post("http://0.0.0.0:7860/caesarocr",json={"ocr_data":encoded_string})
        print(response.json())
    

      

if __name__ == "__main__":
    unittest.main()