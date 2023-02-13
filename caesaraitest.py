import json
import unittest
import requests
import os 
import socket

class CaesarAIHotelBookingTest(unittest.TestCase):
    def hotel_bookings_test(self):
        if "Bookings" not in os.listdir():
            os.mkdir("Bookings")
        city = "Alicante"
        price_range = 2000
        booking_json= {
        "city":city,
        "checkin_date":"2023-8-15",
        "checkout_date":"2023-8-22",
        "purpose":"work",
        "num_of_adults":8,
        "num_of_rooms":5,
        "num_of_children":0,
        "price_range":price_range,
        "num_of_pages":10,
        "exclude_whole":"true"
        }
        #full_bookings = requests.post("https://caesaraiapi.onrender.com/caesaraihotelbookings",json=booking_json).json()
        #print(full_bookings)
        with open(f"Bookings/{city.lower()}_bookings.json","r") as f:
            full_bookings = json.load(f)
        #.json()
        print(full_bookings)
        with open(f"Bookings/{city.lower()}_bookings_lower_than_{price_range}.txt","w+") as f:
            for booking in full_bookings[f"{city.lower()}_bookings_lower_than_{price_range}"]:
                for key,value in booking.items():
                    try:
                        if key == "address":
                            key = key.capitalize()
                        f.write(f"{key} - {value}\n")
                        
                    except KeyError as kex:
                        continue
                f.write("\n")
    #def web_socket_test(self):
    #    import json
    #    from websocket import create_connection
    #    ws = create_connection("ws://caesaraiapi.onrender.com/echo")
    #    ws.send(json.dumps({"op":"addr_sub", "addr":"dogecoin_address"}))
    #    result =  ws.recv()
    #    print (result)
    #    ws.close()


if __name__ == "__main__":
    unittest.main()