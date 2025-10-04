# JSON to AI Summary Tool

A Python tool that extracts content from JSON files, converts it to TXT format, and uses Google's Gemini API to generate concise summaries of the content (ideal for subtitle summarization or text aggregation tasks).


## Features
1. **JSON Content Extraction**: Automatically parses JSON files (requires JSON content to be a list) and extracts all `content` fields.
2. **TXT Conversion**: Saves extracted content as a TXT file with the same name as the input JSON (for easy backup and manual review).
3. **AI-Powered Summarization**: Uses Google Gemini 2.5 Flash API to generate concise summaries of the aggregated content.
4. **Robust Validation**: Includes strict file path validation (checks for empty paths, non-existent files, invalid file types, etc.) to avoid runtime errors.


## Prerequisites
Before using this tool, ensure you meet the following requirements:

### 1. Python Environment
- Install Python 3.8 or higher (recommended: Python 3.10+ for better compatibility with Gemini API).  
  Download from: [Python Official Website](https://www.python.org/downloads/)

### 2. Google Gemini API Access
- **Get an API Key**:  
  1. Go to [Google AI Studio](https://aistudio.google.com/).  
  2. Log in with your Google account.  
  3. Create a new project (or use an existing one) and generate an API key.  
- **API Key Configuration** (two options):  
  - **Option 1 (Recommended)**: Set the API key as an environment variable (avoids hardcoding sensitive information):  
    - Windows: Open Command Prompt and run `setx GEMINI_API_KEY "your-api-key-here"` (restart the terminal after setting).  
    - macOS/Linux: Open Terminal and run `export GEMINI_API_KEY="your-api-key-here"` (add to `~/.bashrc` or `~/.zshrc` for persistence).  
  - **Option 2**: Hardcode the API key directly in the code (for quick testing only, not recommended for production):  
    Modify the `aiSummary` function:  
    ```python
    client = genai.Client(api_key='your-api-key-here')  # Uncomment and replace with your key
    ```

### 3. Dependencies Installation
Install the required Python libraries via `pip`:
```bash
pip install google-generativeai
```


## File Structure
```
json-ai-summary-tool/
├── main.py               # Core script (contains all functions)
├── README.md             # Project documentation (this file)
└── example/              # Optional: Place test JSON files here (e.g., subtitles.json)
```


## Usage Guide
### 1. Prepare Input JSON File
The input JSON file **must follow this format** (content must be a `list` of `dict`s, each containing a `content` field):
```json
[
  {
    "content": "First segment of text (e.g., subtitle line 1)"
  },
  {
    "content": "Second segment of text (e.g., subtitle line 2)"
  },
  {
    "content": "Third segment of text (e.g., subtitle line 3)"
  }
]
```
- Example use case: Summarize video subtitles stored in JSON format.

### 2. Run the Tool
1. Open a terminal/command prompt and navigate to the project directory:
   ```bash
   cd path/to/json-ai-summary-tool
   ```
2. Execute the script:
   ```bash
   python main.py
   ```
3. Follow the on-screen prompt to enter the **full path** of your JSON file:
   - Windows example: `C:\subtitles\my-video-subtitles.json`  
   - macOS/Linux example: `/home/user/subtitles/my-video-subtitles.json`  
   - Note: If you accidentally wrap the path in quotes (e.g., `"C:\subtitles\file.json"`), the tool will automatically remove them.

### 3. View Results
- **TXT File**: A TXT file with the same name as the input JSON (e.g., `my-video-subtitles.txt`) will be generated in the same directory as the JSON file. It contains all extracted `content` fields joined by commas.  
- **AI Summary**: The summary will be printed directly in the terminal.


## Error Handling
The tool includes built-in error handling for common issues:
| Error Scenario | Tool Behavior |
|----------------|---------------|
| Empty file path input | Shows "JSON文件路径不能为空" and exits. |
| Non-existent file | Shows "JSON文件 'path' 不存在" and exits. |
| File is not a JSON (e.g., .txt, .docx) | Shows "文件 'path' 不是JSON格式" and exits. |
| JSON content is not a list (e.g., a single dict) | Shows "JSON文件内容不是一个列表" and exits. |
| No valid `content` fields in JSON | Shows "警告: 未找到任何有效的content字段" and exits. |
| Gemini API key invalid/missing | Shows an error from Google API (check key configuration). |
| Gemini API returns empty/invalid response | Shows "未返回有效结果" or "返回内容格式不正确". |


## Example Workflow
1. Create a test JSON file `subtitles.json` in the project directory:
   ```json
   [
     {"content": "The video starts with an introduction to AI basics."},
     {"content": "It explains how machine learning models are trained with data."},
     {"content": "The final part discusses future trends of AI in healthcare."}
   ]
   ```
2. Run `python main.py` and enter `./subtitles.json` when prompted.
3. The tool will:
   - Generate `subtitles.txt` with content: `The video starts with an introduction to AI basics., It explains how machine learning models are trained with data., The final part discusses future trends of AI in healthcare.`  
   - Print an AI summary like:  
     `以下为视频内容总结：`  
     `The video covers AI basics, explains the training process of machine learning models with data, and discusses future trends of AI applications in healthcare.`


## Notes
1. **API Quotas**: Google Gemini API has free usage quotas (check [Google AI Studio Pricing](https://ai.google.dev/pricing) for details). Avoid processing extremely large files to prevent exceeding quotas.
2. **File Size**: For JSON files larger than 10MB, the tool may process slowly (split large files into smaller chunks if needed).
3. **Sensitive Data**: Do not upload files with sensitive information to Gemini API (comply with Google's [Privacy Policy](https://policies.google.com/privacy)).
4. **Encoding**: Ensure input JSON files use UTF-8 encoding (common for subtitle files; avoid GBK or other encodings to prevent garbled text).


## Troubleshooting
- **"Gemini API key not found"**: Verify the environment variable `GEMINI_API_KEY` is set correctly (restart the terminal after setting).  
- **"JSONDecodeError"**: Check if the JSON file has valid syntax (use [JSON Validator](https://jsonlint.com/) to debug).  
- **"Permission denied"**: Ensure the tool has read access to the JSON file and write access to the directory (run the terminal as administrator on Windows if needed).


## License
This project is open-source for personal and non-commercial use. For commercial use, comply with Google Gemini API's [Terms of Service](https://ai.google.dev/terms) and Python library licenses.
