from database import get_db_connection
from schemas import Agent_State

def save_to_db(state: Agent_State)-> Agent_State:

    with get_db_connection() as conn:
        for item in state["items"]:
            conn.execute(
                "insert into detections (filename, item_type, quantity) values (?, ?, ?)",
                (state["filename"], item.item_type, item.quantity),
            )
        conn.commit()
    return state
