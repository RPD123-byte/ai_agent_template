import openai
import yaml

# Load API key
with open("config/config.yml", "r") as file:
    config = yaml.safe_load(file)

def get_open_ai_json(temperature=0, model="gpt-4-turbo"):
    client = openai.OpenAI(api_key=config["OPENAI_API_KEY"])

    def llm_call(prompt):
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a JSON formatter. Always return valid JSON with no additional text."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            # Force JSON-only output
            response_format={"type": "json_object"}  
        )
        return response

    return llm_call
