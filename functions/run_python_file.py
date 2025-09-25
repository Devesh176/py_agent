import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    absolute_path = os.path.abspath(working_directory)
    target_file_path = os.path.join(absolute_path, file_path)
    
    if not target_file_path.startswith(absolute_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory.'
    
    if not os.path.exists(target_file_path):
        return f'Error: File "{target_file_path}" not found.'

    if target_file_path[len(target_file_path)-3:] != '.py':
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        if args:
            inp = ''
            for a in args:
                inp += a + " " 
            result = subprocess.run(['python3', target_file_path, inp], timeout=30, cwd= working_directory,  capture_output=True, text=True, check=True) # Pass additional args if provided
        else:
            result = subprocess.run(['python3', target_file_path], timeout=30, cwd= working_directory,  capture_output=True, text=True, check=True)
        if not result.stdout:
            return f'No output produced.'

        res = f'STDOUT: {result.stdout}'

        if result.stderr:
            res += f'STDERR: {result.stderr}'

        if result.check_returncode():
            res += ' Process exited with code X.'

        print("res", res)
        return res
    
    except ValueError as e1:
        return f"ValueError: executing Python file: {e1}"

    except OSError as e2:
        return f"OSError: executing Python file: {e2}"
    except ChildProcessError as e3:
        return f"ChildProcessError: executing Python file: {e3}"
    except TimeoutError as e4:
        return f"TimeoutError: executing Python file: {e4}"
    except subprocess.CalledProcessError as e5:
        return f"CalledProcessError: executing Python file: {e5}"

    

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the python file and returns the output.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The current working directory.",
            ),
            "file_path": types.Schema( # Corrected: snake_case
                type=types.Type.STRING,
                description="The actual path of the python file relative to the working directory, to be executed."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="The arguments which need to be passed while executing the python file.",
                items=types.Schema(type=types.Type.STRING) # Corrected: Added items definition
            ),
        },
        required=["directory", "file_path"]
    ),
)
