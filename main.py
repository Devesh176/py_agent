import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info

def main():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)

    if len(sys.argv) < 2:
        print("I need a prompt!")
        sys.exit(1)
    prompt = sys.argv[1]

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]


    system_prompt = """
            You are a helpful AI coding agent.

            When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

            - List files and directories

            All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
            """
    

    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages,
        config = types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt)
    )

    if response is None or response.usage_metadata is None:
        print("No usage metadata available.")
        return
    
    print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    print(response.text)
    
    print(f"Prompt Tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response Tokens: {response.usage_metadata.candidates_token_count}")

main()