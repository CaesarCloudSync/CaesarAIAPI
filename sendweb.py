import cv2 
import numpy as np
import requests
import base64
import time
import websockets
import asyncio
import cv2
import json
class CaesarSendWeb:
    @classmethod
    def send_video_https(self,uri = "https://palondomus-caesarai.hf.space/caesarobjectdetect"):
        cap = cv2.VideoCapture(0)
        while True:
            _, image = cap.read()
            #uri = "http://0.0.0.0:7860/caesarobjectdetect"
            response = requests.post(uri,json={"frame":base64.b64encode(image).decode(),"shape":[image.shape[0],image.shape[1]]})
            valresp = response.json()
            
            imagebase64 = np.array(valresp["frame"])
            
            image = np.frombuffer(base64.b64decode(imagebase64),dtype="uint8").reshape(valresp["shape"][0],valresp["shape"][1],3)
            cv2.imshow("image", image)
            if ord("q") == cv2.waitKey(1):
                break

        cap.release()
        cv2.destroyAllWindows()
    @classmethod
    def send_video_websocket(self,uri = 'wss://palondomus-caesarai.hf.space/caesarobjectdetectws',jsondata=None):

        camera = cv2.VideoCapture(0)

        async def main():
            # Connect to the server
            #uri = 'ws://0.0.0.0:7860/sendvideows'
            #uri = 'ws://0.0.0.0:7860/caesarobjectdetectws'
            async with websockets.connect(uri) as ws:
                while True:
                    success, frame = camera.read()
                    #print(success)
                    #print(frame.shape)
                    if not success:
                        break
                    else:
                        ret, buffer = cv2.imencode('.png', frame)
                        await ws.send(buffer.tobytes())
                        if jsondata:
                            await ws.send(json.dumps(jsondata))
                        
                        contents = await ws.recv()
                        if type(contents) == bytes:
                            arr = np.frombuffer(contents, np.uint8)
                            frameobj = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)
                            cv2.imshow('frame',frameobj)
                            cv2.waitKey(1)
                        if type(contents) == str:
                            print(json.loads(contents))
        asyncio.run(main())
    @classmethod
    def send_image_recieve_text(self,uri ="https://palondomus-caesarai.hf.space/caesarocr",showimage=False):

        cap = cv2.VideoCapture(0)
        
        _, image = cap.read()
        #uri = "http://0.0.0.0:7860/caesarobjectdetect"
        response = requests.post(uri,json={"frame":base64.b64encode(image).decode()})
        messageresp = response.json()
        if showimage == True:
            cv2.imshow('frame',image)
            cv2.waitKey(0)
            # closing all open windows
            cv2.destroyAllWindows()
        
        return messageresp
    @classmethod
    def send_image_recieve_image(self,uri ="https://palondomus-caesarai.hf.space/caesarfacesnap",showimage=False,saveimage=False):

        cap = cv2.VideoCapture(0)
        
        _, image = cap.read()
        #uri = "http://0.0.0.0:7860/caesarobjectdetect"
        
        response = requests.post(uri,json={"frame":base64.b64encode(image).decode(),"shape":[image.shape[0],image.shape[1]]})
        valresp = response.json()
        
        imagebase64 = np.array(valresp["frame"])
        
        image = np.frombuffer(base64.b64decode(imagebase64),dtype="uint8").reshape(valresp["shape"][0],valresp["shape"][1],3)
        if showimage == True:
            cv2.imshow('frame',image)
            cv2.waitKey(0)
            # closing all open windows
            cv2.destroyAllWindows()
        if saveimage == True:
            cv2.imwrite("CaesarFaceDetection/croppedimage.png", image)
   

        return image
if __name__ == "__main__":
    
    #yolo_uri = 'wss://palondomus-caesarai.hf.space/caesarobjectdetectws'
    #CaesarSendWeb.send_video_websocket(uri = yolo_uri)
    
    #video_uri = 'wss://palondomus-caesarai.hf.space/sendvideows'
    #CaesarSendWeb.send_video_websocket(uri = video_uri)
    
    #extraction_uri = "ws://0.0.0.0:7860/caesarocrextractionws"
    #CaesarSendWeb.send_video_websocket(uri = extraction_uri,jsondata={"target_words":["your","brain","power"]})

    #ocrws_uri = "ws://0.0.0.0:7860/caesarocrws"
    #CaesarSendWeb.send_video_websocket(uri = ocrws_uri)
    
    facedetect_uri = "ws://0.0.0.0:7860/caesarfacedetectws"
    CaesarSendWeb.send_video_websocket(uri = facedetect_uri)
    
    #ocr_uri = "http://0.0.0.0:7860/caesarfacesnap"
    #cropped_image = CaesarSendWeb.send_image_recieve_image(uri = ocr_uri,saveimage=True)
    #print(cropped_image)
    
    #ocr_uri = "http://0.0.0.0:7860/caesarocr"
    #message = CaesarSendWeb.send_image_recieve_text(uri = ocr_uri,showimage=True)
    #print(message)


    #https_uri = 'http://0.0.0.0:7860/caesarobjectdetect'
    #CaesarSendWeb.send_video_https(uri = https_uri)
