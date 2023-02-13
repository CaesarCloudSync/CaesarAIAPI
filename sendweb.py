import cv2 
import numpy as np
import requests
import base64
import time
import websockets
import asyncio
import cv2
class CaesarSendWeb:
    @classmethod
    def send_video_https(self,uri = "https://palondomus-caesarai.hf.space/caesarobjectdetect"):
        cap = cv2.VideoCapture(0)
        while True:
            _, image = cap.read()
            #uri = "http://0.0.0.0:7860/caesarobjectdetect"
            response = requests.post(uri,json={"frame":base64.b64encode(image).decode()})
            valresp = response.json()["frame"]
            imagebase64 = np.array(valresp)
            
            image = np.frombuffer(base64.b64decode(imagebase64),dtype="uint8").reshape(480,640,3)
            cv2.imshow("image", image)
            if ord("q") == cv2.waitKey(1):
                break

        cap.release()
        cv2.destroyAllWindows()
    @classmethod
    def send_video_websocket(self,uri = 'wss://palondomus-caesarai.hf.space/caesarobjectdetectws'):

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
                        contents = await ws.recv()
                        arr = np.frombuffer(contents, np.uint8)
                        
                        
                        frameobj = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)
                        #print(message)
                        cv2.imshow('frame',frameobj)
                        cv2.waitKey(1)

        # Start the connection
        asyncio.run(main())
if __name__ == "__main__":
    #yolo_uri = 'wss://palondomus-caesarai.hf.space/caesarobjectdetectws'
    #CaesarSendWeb.send_video_websocket(uri = yolo_uri)
    
    video_uri = 'wss://palondomus-caesarai.hf.space/sendvideows'
    CaesarSendWeb.send_video_websocket(uri = video_uri)

    #https_uri = 'https://palondomus-caesarai.hf.space/caesarobjectdetect'
    #CaesarSendWeb.send_video_https(uri = https_uri)