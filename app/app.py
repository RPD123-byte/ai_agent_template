import json
from agent_graph.graph import GraphExecutor

if __name__ == "__main__":
    executor = GraphExecutor()

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
    # Load unstructured JSON file
    with open("unstructured_data.json", "r") as file:
        input_json = json.load(file)

    with open("sample.txt", 'r') as file:
            text = file.read()

    #Set standard to none
    executor.state['input_json'] = None
    executor.state["input_text_file"] = None
    executor.state["schema"] = None

    # Store input JSON or text in state.. can test with different options
    #executor.state["input_json"] = json.dumps(input_json)
    executor.state["input_text_file"] = text
    executor.state["schema"] = schema

    # Run AI Agent
    executor.execute()

    # Debugging - Print stored schema & structured data
    print("\n🔹 Generated JSON Schema:")
    print(json.dumps(executor.state.get("json_schema", {}), indent=4))

    print("\n🔹 Structured JSON Data:")
    structured_data = executor.state.get("structured_data")

    if structured_data:
        # Save the structured JSON to a file
        with open("structured_output.json", "w") as f:
            json.dump(structured_data, f, indent=4)

        print("\n✅ Structured JSON saved to `structured_output.json`")
        # Print for verification
        print(json.dumps(structured_data, indent=4))  
    else:
        print("❌ ERROR: No structured data generated.")
