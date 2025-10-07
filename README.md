# AI Agent Instructions for py_agent

## Project Overview
This is a Python-based AI coding assistant that supports "gemini-2.0-flash-001" for code analysis and interaction. The project implements a function-calling architecture that allows AI model to safely interact with the filesystem and execute Python code.

```python
                                             | |  
        _ __  _   _     __ _  __ _  ___ _ __ | |_ 
        | '_ \| | | |   / _` |/ _` |/ _ \ '_ \| __|
        | |_) | |_| |  | (_| | (_| |  __/ | | | |_ 
        | .__/ \__, |   \__,_|\__, |\___|_| |_|\__|
        | |     __/ |_____     __/ |               
        |_|    |___/______|   |___/                
    
```

## Core Components
- `/main.py`: Entry point.
- `/functions/`: Contains core function implementations for file operations:
  - `get_files_info.py`: Directory listing with file metadata
  - `get_file_content.py`: Safe file reading with path validation
  - `write_file.py`: Safe file writing with path validation
  - `run_python_file.py`: Sandboxed Python file execution
  - `call_function.py`: Function routing and execution

## Key Patterns and Conventions
1. **Path Safety**:
   - All file operations are constrained to the working directory (here set as `/calculator`)
   - Path validation using `os.path.abspath()` and `.startswith()` checks
   - Example: See `get_file_content.py` implementation

2. **Error Handling**:
   - Comprehensive error handling with specific error messages
   - Graceful degradation with informative error responses
   - Example: See error handling in `write_file.py`

3. **Function Call Protocol**:
   - Functions are declared with schemas (see `types.FunctionDeclaration`)
   - Arguments validated against schema definitions
   - Standard response format: `{"function_response": {"name": name, "response": str(result)}}`

4. **Calculator Example**:
   - `/calculator/`: Reference implementation showing proper project structure
   - Demonstrates package organization (`pkg/`), testing, and modular design

## Environment Setup
- Python 3.10+ required (see `.python-version`)
- Dependencies managed via `pyproject.toml`
- Requires either:
  - Google Gemini API key (in `.env`)
  - To get access to Gemini API follow the link[!https://aistudio.google.com/app/api-keys?project=gen-lang-client-0272858766]
- After successfully securing the API key, run the follwing command in terminal
``` bash
   cd py_agent
   echo "GEMINI_API_KEY=Your_api_key" >> .env
```

## Common Operations
1. **Running the Assistant**:
   ```bash
   uv run main.py "your prompt here" [--verbose]
   ```

## Integration Points
1. Model Integration:
   - System prompts defined in `prompts.py`
   - Model function calling protocol in `generate_content()` function

2. Function Registration:
   - New functions must be registered in `call_function.py`
   - Must include schema declaration and implementation

## Best Practices
1. Always validate file paths against working directory
2. Provide specific error messages for failure cases
3. Follow existing error handling patterns
4. Include tests for new functionality
5. Document function schemas using `types.FunctionDeclaration`
