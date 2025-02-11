import json
import re
from models.openai_models import get_open_ai_json

def json_structurer_agent(state):
    llm = get_open_ai_json()

    unstructured_json = state.get("input_json", "{}")
    schema = state.get("json_schema", {})
    human_append = state.get("human_append", "")

    prompt = (
        "Analyze the following unstructured JSON data and its inferred JSON Schema. "
        "Transform the data into a structured format that follows the schema while ensuring consistency. "
        "Apply these universal rules:\n"
        "- Detect and standardize field names (e.g., 'yearsOld' → 'age', 'mail' → 'email').\n"
        "- Convert age values to integers if they are stored as strings.\n"
        "- Flatten nested objects where possible, keeping meaningful relationships.\n"
        "- Ensure all email-related fields use the standard name 'email'.\n"
        "- Do not assume any specific field names; adjust dynamically based on context.\n\n"
        "- This last rule takes precedence over others: " + human_append + "\n\n"
        f"Schema:\n{json.dumps(schema, indent=4)}\n\n"
        f"Unstructured Data:\n{unstructured_json}\n\n"
        "Return only valid JSON output without any additional text or explanation."
    )


    # Call OpenAI API
    response = llm(prompt)  

    # Debugging - Print raw response
    response_text = response.choices[0].message.content.strip()
    print("\n🔹 OpenAI API Response (Raw):")
    print(response_text)

    # Try extracting JSON from Markdown code block (```json ... ```)
    match = re.search(r'```json\n(.*?)\n```', response_text, re.DOTALL)
    if match:
        cleaned_json = match.group(1)
    else:
        # Try extracting the first valid JSON object in response
        json_match = re.search(r'({.*})', response_text, re.DOTALL)
        if json_match:
            cleaned_json = json_match.group(1)
        else:
            print("❌ ERROR: OpenAI did not return JSON in a recognizable format.")
            return {"error": "No valid JSON detected in OpenAI response"}

    # Debugging - Print cleaned JSON
    print("\n🔹 Extracted JSON (Cleaned):")
    print(cleaned_json)

    # Convert cleaned string to JSON
    try:
        structured_output = json.loads(cleaned_json)
        # Store structured data in state
        state["structured_data"] = structured_output  
        return structured_output
    except json.JSONDecodeError:
        print("❌ ERROR: Failed to parse structured data response.")
        return {"error": "Failed to parse structured data response"}
