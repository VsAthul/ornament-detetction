from pydantic import BaseModel
from typing import List, TypedDict

class Ornament_Item(BaseModel):
    item_type : str
    quantity : int

class Detection_Result(BaseModel):
    items : List[Ornament_Item]

class Agent_State(TypedDict):
    image_bytes : bytes
    filename : str
    items : List[Ornament_Item]