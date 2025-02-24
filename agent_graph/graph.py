from langgraph.graph import StateGraph, END
from states.state import AgentState
from agents.json_parser_agent import json_parser_agent
from agents.json_structurer_agent import json_structurer_agent
from agents.agents import humanConfirmLoop, text_to_structure, startAgent


def create_graph():
    builder = StateGraph(AgentState)

    #Defines starting point based on our state

    builder.set_entry_point("start")
    builder.add_node("start", startAgent)
    builder.add_node("json_parser", json_parser_agent)
    builder.add_node("json_structurer", json_structurer_agent)
    builder.add_node("human_confirm_looper", humanConfirmLoop)
    builder.add_node("text_to_structure", text_to_structure)

    
    
    # Main processing flow
    builder.add_conditional_edges(
        "start",
        lambda state: "json_parser" if state.get("start_point") == "json" else "text_to_structure",
        {
            "json_parser": "json_parser",
            "text_to_structure": "text_to_structure"
        }
    )
    builder.add_edge("json_parser", "json_structurer")
    builder.add_edge("json_structurer", "human_confirm_looper")
    builder.add_edge("text_to_structure", "human_confirm_looper")

    # Human confirmation conditional flow
    def confirmation_router(state):
        if state.get("human_confirm", "").lower() == "yes":
            return END
        elif state.get("start_point") == "text":
            return "text_to_structure"
        return "json_parser"  # Default to JSON path
    
    builder.add_conditional_edges(
        "human_confirm_looper",
        confirmation_router,
        {
            "json_parser": "json_parser",
            "text_to_structure": "text_to_structure",
            END: END
        }
    )

    return builder.compile()
