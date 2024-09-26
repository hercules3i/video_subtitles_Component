from pydantic import BaseModel


class Item(BaseModel):
    url: str
    dest:str
