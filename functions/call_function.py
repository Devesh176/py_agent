# from google.genai import types

# from functions.get_files_info import schema_get_files_info, get_files_info
# from functions.get_file_content import schema_get_file_content, get_file_content
# from functions.run_python_file import schema_run_python_file, run_python_file
# from functions.write_file import schema_write_file, write_file

# available_functions = types.Tool(
#     function_declarations=[
#         schema_get_files_info, schema_write_file, schema_run_python_file, schema_get_file_content
#     ]
# )

# def call_function(function_call_part, verbose=False):
    
#     if verbose:
#         print(f"Calling function: {function_call_part.name}({function_call_part.args})")    
#     else:
#         print(f" - Calling function: {function_call_part.name}")
    
#     working_directory = './calculator' # not controlled by llm
#     function_result = None

#     if function_call_part.name == 'get_file_content':
#         function_result = get_file_content(working_directory, function_call_part.args['file_path'])
        
#     elif function_call_part.name == 'get_files_info':
#         function_result = get_files_info(working_directory, function_call_part.args['directory'])
        
#     elif function_call_part.name == 'run_python_file':
#         if 'args' in function_call_part.args:
#             function_result = run_python_file(working_directory, function_call_part.args['file_path'], function_call_part.args['args'])
#         else:
#             function_result = run_python_file(working_directory, function_call_part.args['file_path'])
        
#     elif function_call_part.name == 'write_file':
#         function_result = write_file(working_directory, function_call_part.args['file_path'], function_call_part.args['content'])
       
#     else:
        
#         return types.Content(
#             role="tool",
#             parts=[
#                 types.Part.from_function_response(
#                     name=function_call_part.name,
#                     response={"error": f"Unknown function: {function_call_part.name}"},
#                 )
#             ],
#         )
    
#     return types.Content(
#     role="tool",
#     parts=[
#         types.Part.from_function_response(
#             name=function_call_part.name,
#             response={"result": function_result},
#         )
#     ],
# )

from google.genai import types

from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file
# from config import WORKING_DIR
WORKING_DIR = './calculator'  # not controlled by llm

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)


def call_function(function_call_part, verbose=False):
    if verbose:
        print(
            f" - Calling function: {function_call_part.name}({function_call_part.args})"
        )
    else:
        print(f" - Calling function: {function_call_part.name}")
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }
    function_name = function_call_part.name
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    args = dict(function_call_part.args)
    # print("argsd ", args)
    args["working_directory"] = WORKING_DIR
    function_result = function_map[function_name](**args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
