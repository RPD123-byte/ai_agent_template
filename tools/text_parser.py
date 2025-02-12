from agents.text_to_structured_agent import TextToStructuredAgent

def parse_text_file(file_path):
    schema = {
        "name": r"Name:\s*(\w+\s\w+)",
        "email": r"Email:\s*([\w.-]+@[\w.-]+\.\w+)",
        "phone": r"Phone:\s*(\d{3}-\d{3}-\d{4})"
    }
    
    agent = TextToStructuredAgent(schema)
    return agent.process_file(file_path)
