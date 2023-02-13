import pymongo
import json
import certifi
import gridfs
# Mongo client Debugging: 
# Tsl error :https://stackoverflow.com/questions/54484890/ssl-handshake-issue-with-pymongo-on-python3
# Ip address whilisting mongo atlas..
class ImportCSV:
    def __init__(self,database,gridfsbase="caesaraifiles") -> None:
        ca = certifi.where()
        # This tells python to specifically send a tls certificate for the connection.
        client = pymongo.MongoClient(f"mongodb+srv://palondrome:kya63amari@caesaraicluster0.k8894gg.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=ca)
        self.db = client[database]
        self.gridfs = client[gridfsbase]

    def load_data(self,collection_name,init_data):
        # Initialises collection 
        db_cm = self.db[collection_name]
        def load_n_insert(data):
            # Input is Dataframe
            data_json = json.loads(data.to_json(orient='records'))
            db_cm.insert_many(data_json)
        load_n_insert(init_data)

if __name__ == "__main__":
    filename = "HusseyCoin.txt.torrent"
    importcsv = ImportCSV("CaesarCoinDB")
    with open("CaesarTorrents"+"/"+filename,"rb") as f:
        data = f.read()
    fs = gridfs.GridFS(importcsv.gridfs)
    fs.put(data,filename=filename)
    print("Upload completed.")

    filedata = importcsv.gridfs.fs.files.find_one({"filename":filename})
    my_id = filedata["_id"]
    output_Data = fs.get(my_id).read()
    output = open("hello.txt.torrent","wb")
    output.write(output_Data)
    output.close()
    print("download completed")
    #outputdata = fs.get()