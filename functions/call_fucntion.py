from google.genai import types

from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

## ====================================== ##
# available_functions = types.Tool(
#     function_declarations=[
#         schema_get_files_info, schema_write_file, schema_run_python_file, schema_get_file_content
#     ]
# )
## ====================================== ##
available_functions = {
    "get_file_content": get_file_content,
    "list_files": get_files_info,
    "run a file": run_python_file,
    "write in a file": write_file
}

def call_function(function_call_part, verbose=False):
    
    if verbose:
        print(f"Calling function: {function_call_part.get('name')}({function_call_part.get('args')})")    
    else:
        print(f" - Calling function: {function_call_part.get('name')}")
    
    working_directory = './calculator' # not controlled by llm
    function_result = None

    if function_call_part.get('name') == 'get_file_content':
        function_result = get_file_content(working_directory, function_call_part.get('args')['file_path'])
        
    elif function_call_part.get('name') == 'get_files_info':
        function_result = get_files_info(working_directory, function_call_part.get('args')['directory'])
        
    elif function_call_part.get('name') == 'run_python_file':
        if 'args' in function_call_part.args:
            function_result = run_python_file(working_directory, function_call_part.get('args')['file_path'], function_call_part.args['args'])
        else:
            function_result = run_python_file(working_directory, function_call_part.get('args')['file_path'])
        
    elif function_call_part.get('name') == 'write_file':
        function_result = write_file(working_directory, function_call_part.get('args')['file_path'], function_call_part.get('args')['content'])
       
    else:
        
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.get('name')}"},
                )
            ],
        )
    
    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_call_part.name,
            response={"result": function_result},
        )
    ],
)
    
    