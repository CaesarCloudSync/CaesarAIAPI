from flask import Flask,request
from flask_cors import cross_origin
from flask_socketio import SocketIO,send,emit
from CaesarYolo import CaesarYolo
import numpy as np
import base64
caesaryolo = CaesarYolo()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route("/",methods=["GET"])
@cross_origin()
def caesaraihome():
    return "Welcome to CaesarAI's API's and CaesarAINL."
@app.route("/caesarobjectdetect",methods=["POST"])
def caesarobjectdetect():
    frames = request.get_json()
    #print(frames)
    
    image = caesaryolo.caesar_object_detect(np.frombuffer(base64.b64decode(frames["frame"]),dtype="uint8").reshape(480,640,3))#base64.b64decode(frames["frame"]))
    return {'frame': base64.b64encode(image).decode()}

@socketio.on('message')
def message(data):
    print(data)  # {'from': 'client'}
    emit('response', {'from': 'server'})

@socketio.on('man')
def message(data):
    print(data)  # {'from': 'client'}
    emit('response', {'from': 'server man'})
@socketio.on('caesarobjectdetect')
def caesarobjectdetect(image):
    image = caesaryolo.caesar_object_detect(np.array(image["frame"]))
    emit('caesarobjectresponse',  {'frame': str(image)})

if __name__ == "__main__":
    #port = int(os.environ.get('PORT', 5000)) # 80
    app.run(debug=True,host="0.0.0.0",port=5000) 
    #socketio.run(app,debug=True,host="0.0.0.0",port=5000) 
