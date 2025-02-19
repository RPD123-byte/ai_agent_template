feedback_verification_prompt_template = """
You are a precise AI validator responsible for ensuring accurate conversion of unstructured data to structured data. 
Your task is to meticulously compare the structured data with the input data and provide detailed feedback.

ONLY return JSON, following this format:
{{
    "correctly_converted": [
        "List of elements that were accurately converted, with specific details"
    ],
    "incorrectly_converted": [
        "List of elements that were converted incorrectly, including what was expected vs what was received"
    ],
    "missing_information": [
        "List of elements from the input that are missing in the structured output"
    ],
    "schema_compliance": {{
        "is_compliant": boolean,
        "issues": ["List of any schema violations or structural issues"]
    }},
    "data_quality": {{
        "completeness": 0-100,
        "accuracy": 0-100,
        "consistency": 0-100
    }},
    "overall_feedback": "Detailed summary of conversion quality and specific recommendations for improvement"
}}

Input Data: {input_data}

Structured Data: {structured_data}

Validation Requirements:
1. Verify all input data elements are present in the structured output
2. Ensure data types are preserved correctly
3. Check for any unrelated or spurious data in the output
4. Validate nested structure integrity
5. Verify array/list conversions maintain order and completeness
6. Check for proper handling of null/empty values

Do NOT include any explanatory text outside the JSON response.
"""

feedback_verification_guided_json = {
    "type": "object",
    "properties": {
        "correctly_converted": {
            "type": "array",
            "items": {"type": "string"}
        },
        "incorrectly_converted": {
            "type": "array",
            "items": {"type": "string"}
        },
        "missing_information": {
            "type": "array",
            "items": {"type": "string"}
        },
        "schema_compliance": {
            "type": "object",
            "properties": {
                "is_compliant": {"type": "boolean"},
                "issues": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            }
        },
        "data_quality": {
            "type": "object",
            "properties": {
                "completeness": {"type": "number"},
                "accuracy": {"type": "number"},
                "consistency": {"type": "number"}
            }
        },
        "overall_feedback": {"type": "string"}
    }
}
