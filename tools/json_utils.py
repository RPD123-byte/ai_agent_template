'''
import json

def validate_json(input_json, schema_path="schema.json"):
    try:
        with open(schema_path, "r") as schema_file:
            schema = json.load(schema_file)

        for key, expected_type in schema.items():
            if key not in input_json:
                return {"error": f"Missing field: {key}"}
            
            if isinstance(expected_type, list) and not isinstance(input_json[key], list):
                return {"error": f"Field {key} should be a list."}
            if isinstance(expected_type, str) and not isinstance(input_json[key], str):
                return {"error": f"Field {key} should be a string."}

        return {"status": "Valid JSON"}
    
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format"}
'''