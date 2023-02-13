import cv2 
import numpy as np
import requests
import base64
import time
#sio = socketio.Client()

#sio.connect('http://localhost:5000')

#sio.emit('man', {'from': 'client'})

#@sio.on("capture")
#def capture():

        
        #cv2.imshow("image", image)
        #if ord("q") == cv2.waitKey(1):
        #    break

    #cap.release()
    #cv2.destroyAllWindows()


#@sio.on('response')
#def response(data):
#    print(data)  # {'from': 'server'}

#   sio.disconnect()
#    exit(0)

cap = cv2.VideoCapture(0)
while True:
    _, image = cap.read()
    response = requests.post("http://0.0.0.0:7860/caesarobjectdetect",json={"frame":base64.b64encode(image).decode()})
    imagebase64 = np.array(response.json()["frame"])
    
    image = np.frombuffer(base64.b64decode(imagebase64),dtype="uint8").reshape(480,640,3)
    cv2.imshow("image", image)
    if ord("q") == cv2.waitKey(1):
        break

cap.release()
cv2.destroyAllWindows()
   # @sio.on('caesarobjectresponse')
    #def caesarobjectresponse(image):
    #    #print(image)
    #    cv2.imshow("image",  {'frame':np.array(image["frame"])})
    #sio.emit("caesarobjectdetect",{'frame':str(image)})
        