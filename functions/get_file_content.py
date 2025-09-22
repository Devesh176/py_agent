import os

def get_file_content(working_directory, file_path):
    absolute_path = os.path.abspath(working_directory)
    target_file_path = os.path.join(absolute_path, file_path)
    
    if not target_file_path.startswith(absolute_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    
    if not os.path.isfile(target_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    MAX_CHARS = 10000 # user choice
   
    try:
        with open(file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)

        file_content_string += f'File "{file_path}" truncated at 1000 characters'
        return file_content_string

    except FileNotFoundError as e1: 
        return f'Error: {e1}, The specified file was not found.'
    except PermissionError as e2:
        return f'Error: {e2}. Insufficient permissions to read this file.'
    except IsADirectoryError as e3:
        return f'Error: {e3}, Cannot open a directory as a file.'
    except UnicodeDecodeError as e4:
        return f'Error: {e4}, Failed to decode the file content. Check Encoding.'
    except IOError or OSError as e5:
        return f'Error: {e5}, An operating system error occured during file access: {file_path}'
    except EOFError as e6:
        return f'Error: {e6}, End of input reached unexpectedly. No input was provided.'

