import json
import ast
from langchain_core.runnables import RunnableLambda
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
from langchain_core.messages import HumanMessage
from models.openai_models import get_open_ai_json
from langgraph.checkpoint import MemorySaver

from agents.agents import feedback_verification_agent
from prompts.prompts import feedback_verification_prompt_template, feedback_verification_guided_json

from states.state import AgentGraphState, get_agent_graph_state

def create_graph(server=None, model=None, stop=None, model_endpoint=None, profile_file=None):
    graph = StateGraph(AgentGraphState)

    # ✅ Prevent infinite looping by stopping execution at the graph level
    def feedback_verification_node(state):
        if state.get("feedback_verified"):
            print("🚫 Feedback already verified. Stopping execution at graph level.")
            return state  # ✅ Stop execution immediately without scheduling another node
        
        state["feedback_verified"] = True  # ✅ Mark feedback as verified
        
        # Call the feedback agent
        try:
            updated_state = feedback_verification_agent(
                state=state,
                model=model,
                server=server,
                guided_json=feedback_verification_guided_json,
                stop=stop,
                model_endpoint=model_endpoint
            )
            return updated_state  # ✅ Return the new state to stop further execution
        except Exception as e:
            print(f"❌ Error in feedback_verification_agent: {e}")
            state["feedback"] = {"error": str(e), "status": "failed"}
            state["error_reported"] = True  # ✅ Prevent repeated error execution
            return state  # ✅ Stop execution on error as well

    # ✅ Add feedback verification agent node with loop prevention
    graph.add_node("feedback_verification", feedback_verification_node)

    # ✅ Add an explicit exit node
    def end_node(state):
        print("✅ Execution completed. Stopping workflow.")
        return state  # ✅ This ensures the workflow stops

    graph.add_node("end", end_node)

    # ✅ Set entry and finish points (prevents '__start__' error)
    graph.set_entry_point("feedback_verification")
    graph.set_finish_point("end")

    # ✅ Connect feedback verification to the end node
    graph.add_edge("feedback_verification", "end")  # ✅ Ensures execution stops

    return graph

def compile_workflow(graph):
    workflow = graph.compile()
    return workflow
