import json
import re


def __init__(self, schema):
        """
        Initialize the agent with a schema.
        :param schema: A dictionary defining the structure of the expected output.
        """
        self.schema = schema

def process_text(text, schema):
        prompt = (
        "Analyze the following unstructured text data and its set schema"
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
        
        return None

def process_file(file_path):
        """
        Read a text file and convert it to structured data.
        :param file_path: Path to the text file.
        :return: Structured data dictionary.
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        
        return process_text(text)

