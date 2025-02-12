import json
import re

class TextToStructuredAgent:
    def __init__(self, schema):
        """
        Initialize the agent with a schema.
        :param schema: A dictionary defining the structure of the expected output.
        """
        self.schema = schema

    def process_text(self, text):
        """
        Convert unstructured text into structured data based on the schema.
        :param text: Raw text input.
        :return: A structured dictionary.
        """
        structured_data = {}
        
        for key, pattern in self.schema.items():
            match = re.search(pattern, text)
            structured_data[key] = match.group(1) if match else None
        
        return structured_data

    def process_file(self, file_path):
        """
        Read a text file and convert it to structured data.
        :param file_path: Path to the text file.
        :return: Structured data dictionary.
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        
        return self.process_text(text)

if __name__ == "__main__":
    # Example schema defining expected fields and their regex patterns
    schema = {
        "name": r"Name:\s*([\w\s]+)",
        "email": r"Email:\s*([\w.-]+@[\w.-]+\.\w+)",
        "phone": r"Phone:\s*(\d{3}-\d{3}-\d{4})",
        "address": r"Address:\s*([\w\s,]+)",
        "dob": r"Date of Birth:\s*([\d-]+)",
        "occupation": r"Occupation:\s*(.+)",
        "company": r"Company:\s*(.+)",
        "linkedin": r"LinkedIn:\s*(https?://[\w./-]+)",
        "github": r"GitHub:\s*(https?://[\w./-]+)",

        # Multi-line Fields
        "experience": r"Experience:\s*([\s\S]+?)\n\n",  
        "education": r"Education:\s*([\s\S]+?)\n\n",
        "projects": r"Projects:\s*([\s\S]+?)\n\n",
        "skills": r"Skills:\s*([\s\S]+?)\n\n",
        "references": r"References:\s*([\s\S]+)"
    }


    
    agent = TextToStructuredAgent(schema)
    structured_output = agent.process_file("sample.txt")
    
    print(json.dumps(structured_output, indent=4))
