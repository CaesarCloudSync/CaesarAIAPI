import cv2 
import numpy as np
import requests
import base64
import time

def send_video():
    cap = cv2.VideoCapture(0)
    while True:
        _, image = cap.read()
        #print(image)
        #uri = "http://palondomus-caesarai.hf.space/caesarobjectdetect"
        uri = "http://0.0.0.0:7860/caesarobjectdetect"
        response = requests.post(uri,json={"frame":base64.b64encode(image).decode()})
        imagebase64 = np.array(response.json()["frame"])
        print(imagebase64)
        image = np.frombuffer(base64.b64decode(imagebase64),dtype="uint8").reshape(480,640,3)
        cv2.imshow("image", image)
        if ord("q") == cv2.waitKey(1):
            break

    cap.release()
    cv2.destroyAllWindows()

def send_websocket():
    import websockets
    import asyncio
    import cv2

    camera = cv2.VideoCapture(0)

    async def main():
        # Connect to the server
        #uri = 'wss://palondomus-caesarai.hf.space/caesarobjectdetectws'
        #uri = 'ws://0.0.0.0:7860/sendvideows'
        uri = 'ws://0.0.0.0:7860/sendvideows'
        uri = 'ws://0.0.0.0:7860/caesarobjectdetectws'
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
                    #print(arr)
                    
                    frameobj = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)
                    #print(message)
                    cv2.imshow('frame',frameobj)
                    cv2.waitKey(1)

    # Start the connection
    asyncio.run(main())
#send_websocket()
send_video()
