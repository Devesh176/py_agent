import os
from google.genai import types

def get_files_info(working_directory: str, directory: str =".") -> str:
    """
    Get the information of the files in the specified directory.
    
    Args:
        working_directory (str): The base working directory.
        directory (str): The target directory relative to the working directory.
        
    Output:
        String containing files information.
    """
    
    absolute_path = os.path.abspath(working_directory)
    target_directory = os.path.join(absolute_path, directory)
    
    if not target_directory.startswith(absolute_path):
        return f"Error: The directory '{directory}' is outside the permitted working directory.\n"
    
    if not os.path.exists(target_directory) or not os.path.isdir(target_directory):
        return f'Error: "{directory}" is not a directory.\n'
    
    files_info = ""
    files = os.listdir(target_directory)
    
    for file_name in files:
        file_path = os.path.join(target_directory, file_name)
        
        # Initialize size and is_dir flag
        is_dir = False
        file_size = 0
        
        if os.path.isfile(file_path):
            is_dir = False
            file_size = os.path.getsize(file_path)
        elif os.path.isdir(file_path):
            is_dir = True
            # Calculate the total size for directories using os.walk
            for path, dirs, files in os.walk(file_path):
                for f in files:
                    file_size += os.path.getsize(os.path.join(path, f))
        
        # Append information for this file/directory
        files_info += f"- {file_name}: file_size={file_size} bytes, is_dir={is_dir}\n"
 
    return files_info


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
