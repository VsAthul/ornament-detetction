from schemas import Agent_State

SUPPORTED_TYPES = ["image/jpeg", "image/png", "image/jpg", "image/webp"]


def load_image(state: Agent_State) -> Agent_State:
    """
    Validates the incoming image payload.

    On failure the node returns the existing state augmented with an
    'error' key so the graph can route to an error-handling node instead
    of letting a raw exception bubble up.
    """

    if not state.get("image_bytes"):
        return {
            **state,
            "error": ValueError("Empty image received."),
        }

    if state.get("content_type") not in SUPPORTED_TYPES:
        supported = ", ".join(SUPPORTED_TYPES)
        return {
            **state,
            "error": ValueError(
                f"Unsupported content type: '{state.get('content_type')}'. "
                f"Supported types are: {supported}."
            ),
        }

    # Clear any stale error from a previous run through this node
    return {**state, "error": None}