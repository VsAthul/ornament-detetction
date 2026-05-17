import base64
import json
import os
from groq import Groq
from schemas import Ornament_Item, Detection_Result, Agent_State
from dotenv import load_dotenv

load_dotenv()
def detect_items(state: Agent_State) -> Agent_State:

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    b64 = base64.standard_b64encode(state["image_bytes"]).decode()
    mime = state["content_type"]

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime};base64,{b64}",
                        },
                    },
                    {
                        "type": "text",
                        "text": (
                            "You are a gold ornament expert. "
                            "Identify every gold ornament visible in this image. "
                            "Return a JSON object with a key called 'items' which is a list of objects. "
                            "Each object must have exactly two keys: "
                            "'item_type' (string: ring, bangle, chain, necklace, earring, bracelet, anklet, or other) "
                            "and 'quantity' (integer: count of that ornament type visible). "
                            "If no gold ornaments are visible, return {\"items\": []}."
                        ),
                    },
                ],
            }
        ],
        max_tokens=600,
        temperature=0,
        response_format={
            "type": "json_object",
            "schema": Detection_Result.model_json_schema(),
        },
    )

    raw = response.choices[0].message.content.strip()
    print(f"\n--- Structured output ---\n{raw}\n-------------------------\n")

    parsed = json.loads(raw)

    # Safety: remap 'count' to 'quantity' if model still uses wrong key
    items = []
    for item in parsed.get("items", []):
        if "count" in item and "quantity" not in item:
            item["quantity"] = item.pop("count")
        items.append(Ornament_Item(**item))

    return {**state, "items": items}