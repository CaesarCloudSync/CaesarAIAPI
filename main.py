import asyncio
import base64
import itertools
import json
import os
import time

import cv2
import numpy as np
import pandas_datareader as pdr
import pytesseract
import speech_recognition as sr
import uvicorn
from CaesarDetectEntity import CaesarDetectEntity
from CaesarHotelBooking.caesarhotelbooking import CaesarHotelBooking
from CaesarObjectDetection.CaesarYolo import CaesarYolo
from CaesarTranslate import CaesarLangTranslate
from CaesarVoice import CaesarVoice
from csv_to_db import ImportCSV
from fastapi import FastAPI, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from RequestModels import *
from tqdm import tqdm
from transformers import pipeline
from CaesarFaceDetection.caesarfd import CaesarFaceDetection
importcsv  = ImportCSV("CaesarAI")
caesaryolo = CaesarYolo()
caesarfacedetectmodel = CaesarFaceDetection()
app = FastAPI()
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
@app.get("/")
def caesaraihome():
    return "Welcome to CaesarAI's API's and CaesarAINL."

@app.websocket("/caesarobjectdetectws")
async def caesarobjectdetectws(websocket: WebSocket):
    # listen for connections
    await websocket.accept()

    try:
        while True:
            contents = await websocket.receive_bytes()
            arr = np.frombuffer(contents, np.uint8) # turns the image byte data into numpy array

            frame = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED) # turns numpy array into the original image shape and state
            
            image =  caesaryolo.caesar_object_detect(frame) # Does object detection and returns a numpy array
            ret, buffer = cv2.imencode('.png', image) # turns numpy array into buffer

            await websocket.send_bytes(buffer.tobytes()) # sends the buffer as bytes


    except WebSocketDisconnect:
        print("Client disconnected")

@app.websocket("/caesarfacedetectws")
async def caesarfacedetect(websocket: WebSocket):
    # listen for connections
    await websocket.accept()

    try:
        while True:
            contents = await websocket.receive_bytes()
            arr = np.frombuffer(contents, np.uint8) # turns the image byte data into numpy array

            frame = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED) # turns numpy array into the original image shape and state
            
            image =  caesarfacedetectmodel.detect_face(frame) # Does object detection and returns a numpy array
            ret, buffer = cv2.imencode('.png', image) # turns numpy array into buffer

            await websocket.send_bytes(buffer.tobytes()) # sends the buffer as bytes


    except WebSocketDisconnect:
        print("Client disconnected")

@app.post("/caesarfacesnap")
def caesarfacesnap(frames: CaesarOCRHTTPModel):
    try:
        frames = dict(frames)
        image = np.frombuffer(base64.b64decode(frames["frame"]),dtype="uint8").reshape(frames["shape"][0],frames["shape"][1],3)
        image = caesarfacedetectmodel.detect_face(image,snapcropface=True)
        if image == [] or image is None:
            return {"frame":"no face was detected."}
        elif image != [] or image is None:
            x=np.ascontiguousarray(image)
            return {'frame': base64.b64encode(x).decode(),"shape":[image.shape[0],image.shape[1]]}
    except Exception as ex:
        return {"error":f"{type(ex)},{ex}"}

@app.websocket("/caesarocrextractionws")
async def caesarocrextractionws(websocket: WebSocket):
    # listen for connections
    await websocket.accept()

    try:
        while True:
            contents = await websocket.receive_bytes()
            target_words = await websocket.receive_json()
            
            target_words = dict(target_words)["target_words"]


            arr = np.frombuffer(contents, np.uint8) # turns the image byte data into numpy array

            frame = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED) # turns numpy array into the original image shape and state
            
            data = pytesseract.image_to_data(frame, output_type=pytesseract.Output.DICT)
            image_copy = frame.copy()

            # get all data from the image
            data = pytesseract.image_to_data(frame, output_type=pytesseract.Output.DICT)

            # print the data
            #print(data["text"])

            # get all occurences of the that word
            word_occurences = [ i for i, word in enumerate(data["text"]) for target in target_words if word.lower() == target]

            for occ in word_occurences:
                # extract the width, height, top and left position for that detected word
                w = data["width"][occ]
                h = data["height"][occ]
                l = data["left"][occ]
                t = data["top"][occ]
                # define all the surrounding box points
                p1 = (l, t)
                p2 = (l + w, t)
                p3 = (l + w, t + h)
                p4 = (l, t + h)
                # draw the 4 lines (rectangular)
                image_copy = cv2.line(image_copy, p1, p2, color=(255, 0, 0), thickness=2)
                image_copy = cv2.line(image_copy, p2, p3, color=(255, 0, 0), thickness=2)
                image_copy = cv2.line(image_copy, p3, p4, color=(255, 0, 0), thickness=2)
                image_copy = cv2.line(image_copy, p4, p1, color=(255, 0, 0), thickness=2)

            ret, buffer = cv2.imencode('.png', image_copy) # turns numpy array into buffer

            await websocket.send_bytes(buffer.tobytes()) # sends the buffer as bytes


    except WebSocketDisconnect:
        print("Client disconnected")

@app.websocket("/caesarocrws")
async def caesarocrws(websocket: WebSocket):
    # listen for connections
    await websocket.accept()

    try:
        while True:
            contents = await websocket.receive_bytes()

            arr = np.frombuffer(contents, np.uint8) # turns the image byte data into numpy array

            frame = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED) # turns numpy array into the original image shape and state
            # get the string
            string = pytesseract.image_to_string(frame)
            # print it
            #print(string)

            

            message = json.dumps({"message":string})
            ret, buffer = cv2.imencode('.png', frame) # turns numpy array into buffer

            await websocket.send_json(message) # sends the buffer as bytes
            await websocket.send_bytes(buffer.tobytes()) # sends the buffer as bytes



    except WebSocketDisconnect:
        print("Client disconnected")
@app.post("/caesarocr")
def caesarocr(frames: CaesarOCRHTTPModel):
    # listen for connections
    try:
        frames = dict(frames)
        image = np.frombuffer(base64.b64decode(frames["frame"]),dtype="uint8").reshape(frames["shape"][0],frames["shape"][1],3)
        string = pytesseract.image_to_string(image)
        return {'message': string}
    except Exception as ex:
        return {"error":f"{type(ex)},{ex}"}
        
@app.websocket("/sendvideows")
async def sendvideows(websocket: WebSocket):
    # listen for connections
    await websocket.accept()

    try:
        while True:
            contents = await websocket.receive_bytes()
            arr = np.frombuffer(contents, np.uint8)
            #print(arr)
            
            frame = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)
            #print(frame.shape)
            #image =  caesaryolo.caesar_object_detect(frame)
            ret, buffer = cv2.imencode('.png', frame)
            #print(buffer)
            await websocket.send_bytes(buffer.tobytes())


    except WebSocketDisconnect:
        print("Client disconnected")
# Done
@app.post("/caesarobjectdetect")
def caesarobjectdetect(frames: CaesarObjectDetectModel):
    frames = dict(frames)
    image = caesaryolo.caesar_object_detect(np.frombuffer(base64.b64decode(frames["frame"]),dtype="uint8").reshape(frames["shape"][0],frames["shape"][1],3))#base64.b64decode(frames["frame"]))
    return {'frame': base64.b64encode(image).decode(),"shape":[image.shape[0],image.shape[1]]}


# Done
@app.post("/createcaesaraipi")
def createcaesaraipi(caesar_api_post : CaesarCreateAPIModel):
    caesar_api_post = dict(caesar_api_post)
    caesarapi_db_exists = list(importcsv.db.caesarapis.find( { "caesarapis" : { "$exists" : "true" } } ))
    #print(caesarapi_db)
    if len(caesarapi_db_exists) == 0:
        importcsv.db.caesarapis.insert_one(caesar_api_post)
        return {"message":"caesarapi created."}
    elif len(caesarapi_db_exists) > 0:
        caesarapi_db = caesarapi_db_exists[0]
        #print(caesarapi_db)
        for apis in caesar_api_post["caesarapis"]:
            if apis not in caesarapi_db["caesarapis"]:
                caesarapi_db["caesarapis"].append(apis)
            elif apis in caesarapi_db["caesarapis"]:
                continue
        importcsv.db.caesarapis.replace_one({ "caesarapis" : { "$exists" : "true" } },caesarapi_db)
        return {"message":"caesarapi stored."}
# Done
@app.get("/getcaesaraipi")
def getcaesaraipi():
    try:
        caesarapi_db_exists = list(importcsv.db.caesarapis.find( { "caesarapis" : { "$exists" : "true" } } ))[0]
        del caesarapi_db_exists["_id"]
        return caesarapi_db_exists
    except KeyError as kex:
        return {"error":f"Api doesn't exist"}
# Done
@app.post("/triggerapi")
def triggerapi(user_trigger : TriggerAPIModel):
    user_trigger = dict(user_trigger)["user_trigger"]
    try:
        caesarapi_db_exists = list(importcsv.db.caesarapis.find( { "caesarapis" : { "$exists" : "true" } } ))[0]
    except KeyError as kex:
        return {"error":"Api doesn't exist"}
    try:
        triggered_apis = [i for i in caesarapi_db_exists["caesarapis"] if i["triggerwords"] in user_trigger]
        triggered_api = triggered_apis[0]
        return triggered_api
    except (IndexError,KeyError) as kex:
        return {"message":"sorry couldn't understand what api you want."}
# Done
@app.post("/caesaraihotelbookings")
def caesaraihotelbookings(hotelbookings_json: CaesarHotelBookingsModel):
    """
    params = {
    "city":city,
    "checkin_date":"2023-8-01",
    "checkout_date":"2023-8-08",
    "purpose":"work",
    "num_of_adults":10,
    "num_of_rooms":5,
    "num_of_children":0,
    "page_num":i
    }
    """
    def get_price_range(bookings_json,city,range,):
        def condition(dic):
            ''' Define your own condition here'''
            try:
                price = dic['assumed_final_price']
                return price <= range
            except KeyError as kex:
                return False
        #print(bookings_json)
        bookings = bookings_json[f"{city.lower()}_bookings"]
        filtered = [d for d in bookings if condition(d)]
        return filtered
        
    
    try:
        overall_booking_info = []
        hotelbookings_json = dict(hotelbookings_json)
        try:
            exclude_whole = hotelbookings_json["exclude_whole"]
        except KeyError as kex:
            exclude_whole = None
        city = hotelbookings_json["city"]
        price_range = hotelbookings_json["price_range"]
        print(f"Extracting flight data for {city}...")
        for i in tqdm(range(1,hotelbookings_json["num_of_pages"]+1)):
            params = {
            "city":city,
            "checkin_date":hotelbookings_json["checkin_date"],
            "checkout_date":hotelbookings_json["checkout_date"],
            "purpose":hotelbookings_json["purpose"],
            "num_of_adults":hotelbookings_json["num_of_adults"],
            "num_of_rooms":hotelbookings_json["num_of_rooms"],
            "num_of_children":hotelbookings_json["num_of_children"],
            "page_num":i
            }
            url = CaesarHotelBooking.create_url(**params)
            bookinginfo = CaesarHotelBooking.caesar_get_hotel_info(url)
            overall_booking_info.append(bookinginfo)
        full_bookings = list(itertools.chain(*overall_booking_info))
        price_range_bookings = get_price_range({f"{city.lower()}_bookings":full_bookings},city,price_range)
        if exclude_whole == "true":
            return {"caesaroutput":{"caesarbookings":price_range_bookings}}
            #return {f"{city.lower()}_bookings_lower_than_{price_range}":price_range_bookings}
        return {"caesaroutput":{"caesarbookings":full_bookings}}
        #return {"caesaroutput":full_bookings}
        #return {f"{city.lower()}_bookings":full_bookings,f"{city.lower()}_bookings_lower_than_{price_range}":price_range_bookings}
    except Exception as ex:
        return {"error":f"{type(ex)}{ex}"}

@app.post("/caesarlangtranslate")
def caesarlangtranslate(translate_json: CaesarLangTranslateModel):
    try:# hello
        translate_json = dict(translate_json)
        text = translate_json["caesartranslate"]

        language = "en"
        try:
            responsejson = translate_json["response"]
            language =  translate_json["language"]
            try:
                triggerword  = translate_json["triggerword"]
                caesarlang = CaesarDetectEntity()
                text,language = caesarlang.run(triggerword,text,caesarlang.main_entities[triggerword])
            except KeyError as kex:
                pass
            if responsejson == "true":
                response = True
            elif responsejson == "false":
                response = False
            else:
                response = False
        except KeyError as kex:
            response = False
        caesarlangtranslate = CaesarLangTranslate()
        original,translation,original_language,destination_language = caesarlangtranslate.translate(text,lang=language,response=response)


        return {"caesaroutput":translation,"caesartranslation":{"original":original,"translation":translation,"original_language":original_language,"destination_language":destination_language}}

    except Exception as ex:
        return {"error":f"{type(ex)}-{ex}"}




@app.get("/caesarlangtranslate")
def caesarlangtranslateget(text:str,triggerword:str,responsejson:str):
    try:# hello 
        caesarlang = CaesarDetectEntity()
        try:
            text,language = caesarlang.run(triggerword,text,caesarlang.main_entities[triggerword])
            if responsejson == "true":
                response = True
            elif responsejson == "false":
                response = False
            else:
                response = False
        except KeyError as kex:
            response = False
        caesarlangtranslate = CaesarLangTranslate()
        original,translation,original_language,destination_language = caesarlangtranslate.translate(text,lang=language,response=response)


        return {"caesaroutput":translation,"caesartranslation":{"original":original,"translation":translation,"original_language":original_language,"destination_language":destination_language}}

    except Exception as ex:
        return {"error":f"{type(ex)}-{ex}"}


"""
@app.post("/caesarsr")
def caesarsr(audio_data: Union[UploadFile,str]):

    transcript = ""
    try:
        #print("FORM DATA RECEIVED")
        file = request.files.get("audio_data")
        print(file)

        if file:
            recognizer = sr.Recognizer()
            audioFile = sr.AudioFile(file)
            with audioFile as source:
                data = recognizer.record(source)
            transcript = recognizer.recognize_google(data, key=None)
            return {"message":transcript}
        elif not file:
            # TODO Make it show that the .3pg extension is adaptable
            audiobase64json = request.get_json()
            decode_bytes = base64.b64decode(audiobase64json["audio_data"].replace("data:video/3gpp;base64,",""))
            with open("temp.3pg", "wb") as wav_file:
                wav_file.write(decode_bytes)
            
            os.system('ffmpeg -y -i temp.3pg temp.wav')
            recognizer = sr.Recognizer()
            audioFile = sr.AudioFile("temp.wav")
            with audioFile as source:
                data = recognizer.record(source)
            transcript = recognizer.recognize_google(data, key=None)
            return {"message":transcript}

    except Exception as ex:
        return {"error":f"{type(ex)}-{ex}"}
"""

@app.post("/caesarvoice")
def caesarvoice(voice_input : CaesarVoiceModel):
    try:
        voice_input = dict(voice_input)
        try:
            filename = voice_input["filename"]
            lang = voice_input["language"]
        except KeyError as kex:
            filename = "temp.wav"
            lang = "en"

        CaesarVoice.synthesise(voice_input["text"],filename,lang=lang)
        #if request.method == "POST":
        #    return {"message":transcript}
        return {"message":"voice syntheized"}# send_file(filename,"audio/x-wav")
    except Exception as ex:
        return {"error":f"{type(ex)}-{ex}"}

@app.post("/caesarsummarize")
def caesarsummarize(json_input : CaesarSummarizeModel):
    try:
        json_input = dict(json_input)
        original_text = json_input["text"]
        summarization = pipeline("summarization")
        summary_text = summarization(original_text)[0]['summary_text']
        return {"caesaroutput":summary_text}# send_file(filename,"audio/x-wav")
    except Exception as ex:
        return {"error":f"{type(ex)}-{ex}"}

@app.post("/caesarstockinfo")
def caesarstockinfo(json_input: CaesarStockInfoModel):
    try:
        json_input = dict(json_input)
        # import AAPL stock price
        stock_tick = json_input["stock"]
        start_date = json_input["start_date"]
        end_date =  json_input["end_date"]
        df = pdr.get_data_yahoo(stock_tick, start=start_date,end=end_date)
        print(df)
        return {"caesaroutput":str(df.to_csv(index=False))}# send_file(filename,"audio/x-wav")
    except Exception as ex:
        return {"error":f"{type(ex)}-{ex}"}




@app.get("/caesarvoiceget")
def caesarvoiceget():
    try:
        filename = "temp.wav"
        return FileResponse(filename,media_type="audio/x-wav")
    except Exception as ex:
        return {"error":f"{type(ex)}-{ex}"}
async def main():
    config = uvicorn.Config("main:app", port=7860, log_level="info",host="0.0.0.0",reload=True)
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
