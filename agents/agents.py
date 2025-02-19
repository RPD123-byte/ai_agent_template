import json
import logging
from termcolor import colored
from typing import Dict, List, Any
from models.openai_models import get_open_ai_json
from models.ollama_models import OllamaJSONModel
from models.vllm_models import VllmJSONModel
from states.state import AgentGraphState
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from prompts.prompts import feedback_verification_prompt_template  # ✅ Ensure this is correctly imported

# Configure logging
logging.basicConfig(level=logging.INFO)

# ✅ Custom Exception for Rate Limit Errors
class RateLimitError(Exception):
    """Custom exception for handling API rate limits."""
    pass

# ✅ Retry Logic: Stops after 3 attempts, waits with exponential backoff
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=2, min=5, max=30),
    retry=retry_if_exception_type(RateLimitError),
    reraise=True
)
def call_llm_with_retry(llm, messages):
    """Wrapper for LLM calls with retry logic."""
    try:
        return llm.invoke(messages)
    except Exception as e:
        if "Rate limit exceeded" in str(e) or "Too Many Requests" in str(e):
            logging.warning("⚠️ Rate limit exceeded. Retrying with exponential backoff...")
            raise RateLimitError("Rate limit exceeded - backing off")
        raise e  # Re-raise any other errors

def feedback_verification_agent(state: AgentGraphState, model=None, server=None, guided_json=None, stop=None, model_endpoint=None):
    """
    Enhanced agent with robust error handling and retry mechanism for rate limits.
    """

    print("\n🔍 DEBUG: Checking state before verification")
    print(json.dumps(state, indent=4))

    # ✅ Ensure `structured_data` and `input_data` are properly initialized
    if not state.get("structured_data") or not state.get("input_data"):
        print("⚠️ Warning: `structured_data` or `input_data` was missing. Resetting to default values.")
        state["structured_data"] = {
            "event": "Product Launch",
            "date": "2025-03-15",
            "time": "10:00 AM"
        }
        state["input_data"] = "The product launch is scheduled for March 15, 2025, at 10:00 AM."

    # ✅ Reset feedback verification if already verified
    if state.get("feedback_verified"):
        print("🚫 Feedback already verified. Resetting verification.")
        state["feedback_verified"] = False  # Reset verification flag
        state["feedback"] = {}  # Clear previous feedback

    # ✅ Ensure input data is always in string format
    try:
        structured_data = json.dumps(state["structured_data"], ensure_ascii=False)  # ✅ Prevents formatting issues
        input_data = json.dumps(state["input_data"], ensure_ascii=False)  # ✅ Prevents formatting issues

    except Exception as e:
        print(colored(f"❌ Error: Failed to process input data - {e}", 'red'))
        state["feedback"] = {"error": f"Input data processing failed: {e}", "status": "failed"}
        return state

    # ✅ Debug print before formatting prompt
    print("\n🛠 DEBUG: Attempting to format prompt with:")
    print(f"🔹 input_data: {input_data}")
    print(f"🔹 structured_data: {structured_data}")

    # ✅ Fixing prompt formatting issue
    try:
        formatted_prompt = feedback_verification_prompt_template.format(
            input_data=input_data,
            structured_data=structured_data
        )
        print("✅ Successfully formatted prompt.")

    except Exception as e:
        print(colored(f"❌ Error: Could not format prompt - {e}", 'red'))
        state["feedback"] = {"error": f"Prompt formatting failed: {e}", "status": "failed"}
        return state

    # ✅ Prepare messages for LLM
    messages = [
        {
            "role": "system",
            "content": formatted_prompt
        },
        {
            "role": "user",
            "content": "Verify the quality of structured data conversion."
        }
    ]

    # ✅ Select model based on the server
    try:
        if server == 'openai':
            llm = get_open_ai_json(model=model)
        elif server == 'ollama':
            llm = OllamaJSONModel(model=model)
        elif server == 'vllm':
            llm = VllmJSONModel(
                model=model,
                guided_json=guided_json,
                stop=stop,
                model_endpoint=model_endpoint
            )
        else:
            raise ValueError(f"Unsupported server type: {server}")

        # ✅ Attempt LLM call with retry logic
        ai_msg = call_llm_with_retry(llm, messages)

        # ✅ Ensure response is valid JSON
        try:
            ai_feedback = json.loads(ai_msg.content)
        except json.JSONDecodeError:
            state["feedback"] = {
                "error": "Invalid JSON received from LLM",
                "status": "failed"
            }
            print(colored(f"❌ Error: Invalid JSON received from LLM", 'red'))
            return state

        # ✅ Update state with feedback
        state["feedback"] = {"ai_feedback": ai_feedback, "status": "success"}
        state["feedback_verified"] = True  # ✅ Mark feedback as verified
        print(colored("✓ Feedback generated successfully", 'green'))

    except RateLimitError:
        print(colored(f"⚠️ Rate limit reached. Stopping execution after max retries.", 'yellow'))
        state["feedback"] = {"error": "Rate limit exceeded", "status": "failed"}
        return state
        
    except Exception as e:
        print(colored(f"❌ Error during model execution: {str(e)}", 'red'))
        state["feedback"] = {"error": str(e), "status": "failed"}
        return state

    return state
