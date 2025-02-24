from typing import TypedDict
class AgentState(TypedDict):
    input_json: str | None
    input_text_file: str
    schema: dict
    start_point: str | None
    human_confirm: str | None
    human_append: str | None
    structured_data: dict | None  # Must exist in state
    json_schema: dict | None      # Must exist in state