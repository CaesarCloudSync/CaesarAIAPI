from resemble import Resemble
#https://www.resemble.ai/python/
#https://www.resemble.ai/cloned/
response = Resemble.v2.voices.create('AI Scott')
print(response)
#with open("resembledata/resemb.wav", 'rb') as file:
#    response = Resemble.v2.recordings.create(
#        response['item']['uuid'])
        
        #,
        #file,
        #'audio.wav',
        #'This is the transcript')
#Resemble.v2.voices.build(response['item']['uuid'])