from schemas import Agent_State

SUPPORTED_TYPES = ["image/jpeg", "image/png", "image/jpg", "image/webp"]

def load_image(state : Agent_State)-> Agent_State:
    assert state["image_bytes"], " Empty image received" 
    assert state["content_type"] in SUPPORTED_TYPES , (
        f"Unsupported content type : {state['content_type']}."
        f"Supported types are : {','.join(SUPPORTED_TYPES)}"
    )
    return state