import base64
import os
from schemas import Agent_State, Detection_Result, Ornament_Item
from groq import Groq
import json
from dotenv import load_dotenv

load_dotenv()

def detect_items(state : Agent_State)-> Agent_State:
    client = Groq(
        api_key=os.getenv("GROQ_API_KEY")
    )

    b64 = base64.standard_b64encode(state["image_bytes"]).decode()
    image_type = state["content_type"]
    response = client.chat.completions.create(
        model = "qwen2-vl-7b-instruct",
        messages=[
            {
                "role" : "user",
                "content" : [
                    {
                        "type" : "image_url",
                        "image_url" : {
                            "url" : f"data:{image_type};base64,{b64}", 
                        },
                    },
                    {
                        "type" : "text",
                        "text" : (
                            "You are a gold ornament expert. "
                            "Identify every gold ornament visible in this image. "
                            "For each distinct type, return the item_type "
                            "(ring/bangle/chain/necklace/earring/bracelet/anklet/other) "
                            "and the count of how many are visible. "
                            "Respond ONLY with a valid JSON object in this exact format, "
                            "no extra text:\n"
                            '{"items": [{"item_type": "chain", "quantity": number in integer format}]}'
                    
                        ),
                    },
                ],
            }
        ],
        max_tokens = 600,
        temperature = 0,        
    )
    raw = response.choices[0].message.content.strip()

    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    parsed = json.loads(raw)
    items = [Ornament_Item(**item) for item in parsed["items"]]
    return {**state, "items" : items}
