import json
from langgraph.graph import StateGraph
from agent_graph.graph import create_graph  # Import the LangGraph builder

if __name__ == "__main__":
    # Initialize LangGraph instead of GraphExecutor
    graph = create_graph()

    # Your existing schema and data loading
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
    
    with open("unstructured_data.json", "r") as file:
        input_json = json.load(file)
    
    with open("sample.txt", 'r') as file:
        text = file.read()

    # Create initial state matching your TypedDict structure
    initial_state = {
        "input_json": None,          # Set to json.dumps(input_json) if using JSON
        "input_text_file": text,     # Using text input in this example
        "schema": schema,
        "start_point": None,       # Explicit starting point
        "human_confirm": None,
        "json_parser_response": None,
        "json_structurer_response": None,
        "text_to_structure_response": None,
        "structured_data": None,
        "human_append": "",
        "json_schema": None
    }

    # Execute the graph

    final_state = graph.invoke(initial_state)




    # Output results (same as before)
    print("\n🔹 Generated JSON Schema:")
    print(json.dumps(final_state.get("json_schema", {}), indent=4))

    print("\n🔹 Structured JSON Data:")
    structured_data = final_state.get("structured_data")

    if structured_data:
        with open("structured_output.json", "w") as f:
            json.dump(structured_data, f, indent=4)
        print("\n✅ Structured JSON saved to `structured_output.json`")
        print(json.dumps(structured_data, indent=4))
    else:
        print("❌ ERROR: No structured data generated.")



