import json
from models.openai_models import get_open_ai_json

def json_parser_agent(state):
    llm = get_open_ai_json()

    unstructured_json = state.get("input_json", "{}")

    prompt = (
        "Given the following unstructured JSON data, generate a valid JSON Schema "
        "that explicitly defines the data structure, including types for each field. "
        "Ensure that the schema includes a detailed format for each nested field and does not return an empty object `{}`.\n\n"
        f"Data:\n{unstructured_json}\n\n"
        "Output only the JSON Schema, formatted as a valid JSON object, without any additional text or explanation."
    )

    # Call OpenAI API
    response = llm(prompt)  

    try:
        # Fix response extraction
        schema_output = json.loads(response.choices[0].message.content)  
        # Store in state
        state["json_schema"] = schema_output  
        return schema_output
    except json.JSONDecodeError:
        print("❌ ERROR: Failed to parse schema response.")
        return {"error": "Failed to parse schema response"}


    # Convert cleaned string to JSON
    try:
        structured_output = json.loads(cleaned_json)
        # Store structured data in state
        state["structured_data"] = structured_output  
        return structured_output
    except json.JSONDecodeError:
        print("❌ ERROR: Failed to parse structured data response.")
        return {"error": "Failed to parse structured data response"}