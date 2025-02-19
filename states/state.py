from typing import TypedDict, Annotated, Optional
from langgraph.graph.message import add_messages

class AgentGraphState(TypedDict):
    research_question: str
    planner_response: Annotated[list, add_messages]
    researcher_response: Annotated[list, add_messages]
    reporter_response: Annotated[list, add_messages]
    reviewer_response: Annotated[list, add_messages]
    serper_response: Annotated[list, add_messages]
    scraper_response: Annotated[list, add_messages]
    final_reports: Annotated[list, add_messages]
    end_chain: Annotated[list, add_messages]
    checker_response: Annotated[list, add_messages]
    industry_creator_response: Annotated[list, add_messages]
    uncertain_questions: Annotated[list, add_messages]
    internet_questions: Annotated[list, add_messages]
    categorized_questions: Annotated[list, add_messages]
    report_outlines: Annotated[list, add_messages]
    current_category_index: Optional[int]
    experiments: Annotated[list, add_messages]
    main_focus: Optional[str]
    scored_experiments: Annotated[list, add_messages]

    # ✅ Ensuring Structured Data and Input Data Exist
    structured_data: dict
    input_data: str
    feedback_verified: bool
    error_reported: bool
    feedback: dict  # ✅ Ensure feedback exists

# ✅ Ensure `get_agent_graph_state` function is correctly defined
def get_agent_graph_state(state: AgentGraphState, state_key: str):
    """
    Retrieves the specified state key safely, ensuring missing values don't cause errors.
    """

    state_mapping = {
        "planner": "planner_response",
        "researcher": "researcher_response",
        "reporter": "reporter_response",
        "reviewer": "reviewer_response",
        "serper": "serper_response",
        "scraper": "scraper_response",
        "checker": "checker_response",
        "industry_creator": "industry_creator_response",
        "uncertain": "uncertain_questions",
        "internet": "internet_questions",
        "categorized": "categorized_questions",
        "reports": "report_outlines",
        "experiments": "experiments",
        "scored_experiments": "scored_experiments",
    }

    if state_key.endswith("_all"):
        key = state_key.replace("_all", "")
        return state.get(state_mapping.get(key, ""), [])

    if state_key.endswith("_latest"):
        key = state_key.replace("_latest", "")
        response_list = state.get(state_mapping.get(key, ""), [])
        return response_list[-1] if response_list else []

    return state.get(state_key, None)

# ✅ Ensure Initial State Exists
state: AgentGraphState = {
    "research_question": "",
    "planner_response": [],
    "researcher_response": [],
    "reporter_response": [],
    "reviewer_response": [],
    "serper_response": [],
    "scraper_response": [],
    "final_reports": [],
    "end_chain": [],
    "checker_response": [],
    "industry_creator_response": [],
    "uncertain_questions": [],
    "internet_questions": [],
    "categorized_questions": [],
    "report_outlines": [],
    "current_category_index": 0,
    "experiments": [],
    "main_focus": None,
    "scored_experiments": [],

    # ✅ Fix: Make sure structured data and input data are NEVER None
    "structured_data": {
        "event": "Product Launch",
        "date": "2025-03-15",
        "time": "10:00 AM"
    },  # ✅ Dummy structured data

    "input_data": "The product launch is scheduled for March 15, 2025, at 10:00 AM.",  # ✅ Dummy input data

    # ✅ Fix: Ensure feedback and verification flags work correctly
    "feedback_verified": False,
    "error_reported": False,
    "feedback": {}  
}
