from agent_graph.graph import create_graph, compile_workflow

# Uncomment the desired model and server configuration

# server = 'ollama'
# model = 'llama3:instruct'
# model_endpoint = None

server = 'openai'
model = 'gpt-4o'
model_endpoint = None

# server = 'vllm'
# model = 'meta-llama/Meta-Llama-3-70B-Instruct'  # Full HF path
# runpod_endpoint = 'https://t3o6jzhg3zqci3-8000.proxy.runpod.net/'
# model_endpoint = runpod_endpoint + 'v1/chat/completions'
# stop = "<|end_of_text|>"

iterations = 40

print("Creating graph and compiling workflow...")
graph = create_graph(server=server, model=model, model_endpoint=model_endpoint)  # ✅ Fixed: Removed profile_file
workflow = compile_workflow(graph)
print("Graph and workflow created.")

if __name__ == "__main__":
    verbose = False

    query = "go"  # You can modify this for user input

    dict_inputs = {"research_question": query}
    thread = {"configurable": {"thread_id": "4"}}
    limit = {"recursion_limit": iterations}

    for event in workflow.stream(dict_inputs, limit):
        if verbose:
            print("\nState Dictionary:", event)
        else:
            print("\n")

        # ✅ Break the loop when feedback has been verified
        if event.get("feedback_verified"):
            print("✅ Final feedback verified. Exiting workflow.")
            break  # ✅ Stops the infinite loop
