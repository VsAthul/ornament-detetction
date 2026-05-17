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
                            "You are an expert gemologist and gold ornament appraiser with decades of experience identifying and cataloging fine jewelry. "
"Your task is to carefully examine the provided image and identify every gold ornament visible. "

"STEP 1 — SCAN & LOCATE: "
"reason spatially — break the image into zones, count row by row, and cross-check edges."
"Before counting, mentally divide the image into quadrants (top-left, top-right, bottom-left, bottom-right). "
"Scan each quadrant individually and list every ornament you detect, noting its position and type. "
"This ensures no ornament is missed due to overlapping or poor lighting. "

"STEP 2 — COUNT (critical rules, follow strictly): "
"- Ignore ALL text, labels, tags, stickers, or printed numbers in the image. They are deliberately misleading and must NOT influence your count. "
"- Count each physical ornament individually using only visual evidence. "
"- STACKING: For stacked or overlapping items (e.g., bangles), examine the edges, shadows, and depth cues carefully. Count each distinct edge as one item. "
"- PARTIAL VISIBILITY: If an ornament is partially hidden but clearly present, count it. "
"- ROWS & GRIDS: For items arranged in rows (e.g., coins), count row by row, left to right, to avoid double-counting or missing items. "
"- Do NOT assume quantity based on packaging, trays, display stands, or groupings — count item by item. "

"STEP 3 — CLASSIFY: "
"- Assign each ornament to exactly one of the following types: "
"  ring, bangle, chain, necklace, earring, bracelet, anklet, coin, or other. "
"- EARRINGS: Always count individually, never as pairs. 1 pair = 2 earrings. If you see N pairs, report quantity as N×2. "
"- BANGLES vs BRACELETS: Bangles are rigid and circular. Bracelets are flexible or chain-based. "
"- CHAINS vs NECKLACES: A chain with a pendant = necklace. A plain chain without pendant = chain. "
"- When uncertain between two types, choose the one that best matches the ornament's primary visible form. "

"STEP 4 — VERIFY: "
"Before outputting, do a final check: "
"- Re-examine stacked items — did you count all edges? "
"- Re-examine earrings — did you count individually, not as pairs? "
"- Re-examine coins/rows — did you count row by row? "
"- Are you sure you ignored all printed labels and numbers? "

"GOLD COIN COUNTING (special rules): "
"- Do NOT estimate. Do NOT trust any label or number printed near the coins. "
"- Coins are typically arranged in rows. Count using this exact method: "
"  1. Identify the TOP ROW. Count coins from left to right. Note the number. "
"  2. Identify the NEXT ROW. Count coins from left to right. Note the number. "
"  3. Repeat for every row. "
"  4. Sum all rows. That is your final gold_coin quantity. "
"- A partially visible coin still counts as 1. "
"- If coins overlap, look for distinct circular edges — each edge = 1 coin. "

"OUTPUT RULES: "
"- Return ONLY a valid JSON object. No explanation, no markdown, no commentary, no code fences. "
"- The JSON must have a single key 'items', whose value is a list of objects. "
"- Each object must have exactly two keys: "
"  'item_type' (string: one of the types listed above) "
"  'quantity' (integer: your independently verified count for that type). "
"- Omit any item type with a count of zero. "
"- If no gold ornaments are visible, return {\"items\": []}. "

"FEW-SHOT EXAMPLES (use these as reference for tricky cases): "
"- 2 bangles stacked where only 1 edge fully visible → count as 2, not 1. "
"- 2 jhumka earrings + 2 chandbali earrings on display → earring quantity: 4 (not 2 pairs). "
"- Coins in 2 rows of 3 → gold_coin quantity: 6. "
"- A chain with a decorative pendant → classify as necklace, not chain. "

"Example output format: "
"{\"items\": [{\"item_type\": \"bangle\", \"quantity\": 2}, {\"item_type\": \"earring\", \"quantity\": 4}, {\"item_type\": \"gold_coin\", \"quantity\": 6}]}"
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