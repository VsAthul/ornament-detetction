from pydantic import BaseModel, Field
from typing import List, TypedDict, Optional

class Ornament_Item(BaseModel):
    item_type: str = Field(description="Type of ornament: ring, bangle, chain, necklace, earring, bracelet, anklet, or other")
    quantity: int = Field(description="Number of this ornament type visible in the image")

class Detection_Result(BaseModel):
    items: List[Ornament_Item] = Field(description="List of detected gold ornaments")

class Agent_State(TypedDict):
    image_bytes: bytes
    filename: str
    content_type: str
    items: List[Ornament_Item]
    error: Optional[Exception]