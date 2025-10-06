import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

from prompts import system_prompt
from functions.call_function import call_function, available_functions


def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages, verbose)


def generate_content(client, messages, verbose):
    verbose = True
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting.")


if __name__ == "__main__":
    main()

# import os 
# import sys
# import json
# from dotenv import load_dotenv
# from transformers import AutoTokenizer, AutoModelForCausalLM
# import torch
# from prompts import system_prompt
# from functions.call_fucntion import available_functions, call_function
# from huggingface_token import token
# from huggingface_hub import login

# # Paste your token here
# # It's better to load this from a secret manager or environment variable


# # ... the rest of your main function

# # def get_file_content(path: str) -> str:
# #     """Reads the content of a file at the given path."""
# #     try:
# #         with open(path, 'r') as f:
# #             return f.read()
# #     except Exception as e:
# #         return f"Error reading file: {e}"

# # def list_files(path: str = ".") -> list[str]:
# #     """Lists all files and directories in the given path."""
# #     try:
# #         return os.listdir(path)
# #     except Exception as e:
# #         return [f"Error listing files: {e}"]

# # --- Map function names to the actual functions ---
# # This is used to execute the function call returned by the model


# # --- Modified System Prompt for Hugging Face ---
# # This is the crucial part. We describe the functions and the desired JSON output format.



# # def call_function(function_call_part, verbose=False):
# #     """
# #     Executes a function call based on the model's output.
# #     Note: The input `function_call_part` is now a dictionary, not a Google API object.
# #     """
# #     function_name = function_call_part.get("name")
# #     function_args = function_call_part.get("args", {})

# #     if function_name not in available_functions:
# #         raise ValueError(f"Function '{function_name}' is not available.")

# #     function_to_call = available_functions[function_name]
    
# #     if verbose:
# #         print(f"Executing: {function_name}({function_args})")
        
# #     result = function_to_call(**function_args)
# #     return {"function_response": {"name": function_name, "response": str(result)}}


# def generate_content(model, tokenizer, messages, verbose):
#     """
#     Generates content using a Hugging Face model and handles function calls.
#     """
#     # Apply the chat template for the specific model (e.g., Mistral)
#     # This correctly formats the input with roles like 'user', 'assistant'
#     prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    
#     if verbose:
#         print("--- Formatted Prompt for Model ---")
#         print(prompt)
#         print("---------------------------------")
        
#     # Tokenize the input and move it to the GPU if available
#     inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
#     # Generate the response
#     outputs = model.generate(
#         **inputs,
#         max_new_tokens=512,  # Limit the length of the response
#         pad_token_id=tokenizer.eos_token_id # Avoid warnings
#     )
    
#     # Decode the generated tokens, skipping the prompt part
#     response_text = tokenizer.decode(outputs[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True)

#     if verbose:
#         print("\n--- Model Raw Output ---")
#         print(response_text)
#         print("----------------------\n")

    
#     try:
#         # The model might output markdown ```json ... ```, so we clean it
#         if "```json" in response_text:
#             json_str = response_text.split("```json")[1].split("```")[0].strip()
#         else:
#             json_str = response_text
        
#         response_json = json.loads(json_str)
        
#         if "function_call" in response_json:
#             function_call_part = response_json["function_call"]
#             print(f"Calling function: {function_call_part.get('name')}({function_call_part.get('args')})")
            
#             # This is a dictionary, not a special object anymore
#             function_call_result = call_function(function_call_part, verbose=verbose)
#             if not function_call_result.parts[0]:
#                 raise ValueError("The function call result has no part[0]")
#             print(f"-> {function_call_result.parts[0].function_response.response}")   
#             # print(f"-> {function_call_result['function_response']['response']}")
            
#             return # Or implement a loop to continue the conversation
            
#     except json.JSONDecodeError:
#         # If it's not valid JSON, it's a regular text response
#         print(response_text)
#         return response_text


# # def main():
# #     load_dotenv()
# #     HF_TOKEN = token ## add your token here
# #     login(token=HF_TOKEN)
# #     verbose = "--verbose" in sys.argv
# #     args = []
# #     for arg in sys.argv[1:]:
# #         if not arg.startswith("--"):
# #             args.append(arg)

# #     if not args:
# #         print("AI Code Assistant (Hugging Face)")
# #         print('\nUsage: python main.py "your prompt here" [--verbose]')
# #         sys.exit(1)

# #     # --- Hugging Face Model Loading ---
# #     model_name = "mistralai/Mistral-7B-Instruct-v0.2"
# #     print(f"Loading model: {model_name}...")
    
# #     # Use bfloat16 for less memory usage
# #     tokenizer = AutoTokenizer.from_pretrained(model_name)
# #     model = AutoModelForCausalLM.from_pretrained(
# #         model_name,
# #         torch_dtype=torch.bfloat16,
# #         device_map="auto" # Automatically use GPU if available
# #     )
# #     print("Model loaded successfully. You can now start chatting.")
# #     print("Type 'exit' or 'quit' to end the session.")
    
# #     while True:
# #         user_prompt = " ".join(args)

# #         if user_prompt.lower() in ["exit", "quit"]:
# #             print("Goodbye!")
# #             break
        
# #         if verbose:
# #             print(f"User prompt: {user_prompt}\n")

# #         # The 'messages' format is a standard that chat models understand
# #         # We add our system prompt first to provide instructions.
# #         messages = [
# #             {"role": "user", "content": system_prompt + "\n" + user_prompt}
# #         ]

# #         generate_content(model, tokenizer, messages, verbose)


# def main():
#     # ... (keep your existing setup code like load_dotenv, verbose check, etc.)

#     # --- CHOOSE YOUR LIGHTWEIGHT MODEL HERE ---

#     # My top recommendation for the best balance of performance and size
#     HF_TOKEN = token ## add your token here
#     login(token=HF_TOKEN)
#     verbose = "--verbose" in sys.argv
#     model_name = "microsoft/Phi-3-mini-4k-instruct"
    
#     # Uncomment the one you want to use:
#     # model_name = "google/gemma-2b-it" # Requires you to accept license on its HF page
#     # model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0" # The smallest and fastest option

#     # IMPORTANT: Phi-3 requires an extra tokenizer argument
#     # If you use Phi-3, the tokenizer MUST have `trust_remote_code=True`
#     # For other models, this is not needed.
#     tokenizer_kwargs = {}
#     if "Phi-3" in model_name:
#         tokenizer_kwargs['trust_remote_code'] = True


#     print(f"Loading model onto CPU: {model_name}... (This will be much faster now)")
    
#     tokenizer = AutoTokenizer.from_pretrained(model_name, **tokenizer_kwargs)
#     model = AutoModelForCausalLM.from_pretrained(
#         model_name,
#         device_map="cpu",
#         trust_remote_code=True # This is also needed for Phi-3
#     )
    
#     print("Model loaded successfully. You can now start chatting.")
#     print("Type 'exit' or 'quit' to end the session.")

#     # --- Start an interactive loop ---
#     while True:
#         user_prompt = input("\nYou: ")
        
#         if user_prompt.lower() in ["exit", "quit"]:
#             print("Goodbye!")
#             break
            
#         # The prompt formatting needs to be applied by the tokenizer
#         # We can create the messages list and let the tokenizer handle the template
#         messages = [
#             # For these smaller models, a complex system prompt isn't as necessary
#             # unless you are doing function calling. Let's simplify for chat.
#             {"role": "user", "content": user_prompt}
#         ]
        
#         # We will handle prompt formatting inside generate_content

#         generate_content(model, tokenizer, messages, verbose)

# # You may need to adjust the generate_content function slightly for chat templates

# if __name__ == "__main__":
#     main()
