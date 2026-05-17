from langgraph.graph import StateGraph, END
from schemas import Agent_State
from nodes import load_image, detect_items, save_to_db

def build_graph():

    graph = StateGraph(Agent_State)

    graph.add_node("load_image", load_image)
    graph.add_node("detection", detect_items)
    graph.add_node("store_to_db", save_to_db)

    graph.set_entry_point("load_image")
    graph.add_edge("load_image", "detection")
    graph.add_edge("detection", "store_to_db")
    graph.add_edge("store_to_db", END)

    compiled_graph = graph.compile()
    # graph_image = compiled_graph.get_graph().draw_mermaid_png()
    # with open("graph.png", "wb") as f :
    #     f.write(graph_image)
    return compiled_graph

detection_graph = build_graph()