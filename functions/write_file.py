import os

def write_file(working_directory, file_path, content):
    absolute_path = os.path.abspath(working_directory)
    target_file_path = os.path.join(absolute_path, file_path)
    
    if not target_file_path.startswith(absolute_path):
        return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory.'
    
    
    # if not os.path.isfile(target_file_path):
    #     return f'Error: File not found or is not a regular file: "{file_path}"'
    print(os.path.exists(target_file_path))
    if not os.path.exists(target_file_path):
        
        
        # os.makedirs(target_file_path, exist_ok=True)
        
        try:
            with open(target_file_path, "w") as f:
                f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
        except PermissionError as e1:
            return f'Error: {e1}, Insufficient permissions to write in this file.'
        except IsADirectoryError as e2:
            return f'Error {e2}, The file path {target_file_path} is a directory.'
        except FileNotFoundError as e3:
            return f'Error {e3}, The specified file was not found.'
        except TypeError as e4:
            return f'Error {e4}, The content to write is not in expected type.'
        except IOError or OSError as e5:
            return f'Error: {e5}, An operating system error occured during file access: {target_file_path}'


            
        

    else:
        try:
                with open(target_file_path, "w") as f:
                    f.write(content)
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
            
        except PermissionError as e1:
            return f'Error: {e1}, Insufficient permissions to write in this file.'
        except IsADirectoryError as e2:
            return f'Error {e2}, The file path {target_file_path} is a directory.'
        except FileNotFoundError as e3:
            return f'Error {e3}, The specified file was not found.'
        except TypeError as e4:
            return f'Error {e4}, The content to write is not in expected type.'
        except IOError or OSError as e5:
            return f'Error: {e5}, An operating system error occured during file access: {target_file_path}'

