from pydantic import BaseModel
from typing import Union,List

class CaesarHotelBookingsModel(BaseModel):
    city:str
    checkin_date: str
    checkout_date: str
    purpose: str
    num_of_adults:int
    num_of_rooms: int
    num_of_children:int
    price_range : float
    num_of_pages : int
    exclude_whole : Union[str,None]

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

class CaesarLangTranslateModel(BaseModel):
    caesartranslate : str
    response: str
    language: str
    triggerword: Union[str,None]

class CaesarStockInfoModel(BaseModel):
    stock: str
    start_date: str
    end_date: str


class CaesarVoiceModel(BaseModel):
    filename: Union[str,None]
    language: Union[str,None]
    text: str
class CaesarOCRRequestModel(BaseModel):
    ocr_data:str

class CaesarSummarizeModel(BaseModel):
    text: str

class CaesarCreateAPIModel(BaseModel):
    caesarapis : List[dict] = []

class CaesarObjectDetectModel(BaseModel):
    frame: str
class CaesarOCRHTTPModel(BaseModel):
    frame: str

class TriggerAPIModel(BaseModel):
    user_trigger : str

