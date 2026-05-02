# 🧠 CodeSense — AI-Powered Python Code Analyzer

> Paste your Python code. Get instant explanation, debugging, optimization, or a kid-friendly breakdown — powered by Google Gemini.

---

## What is CodeSense?

CodeSense is a Flask REST API that analyzes Python code through **three layers of understanding**:

1. **AST Parsing** — your code's structure is extracted using Python's `ast` module
2. **Live Execution** — the code is actually run and output/errors are captured
3. **AI Analysis** — all context is sent to Google Gemini for intelligent feedback

This triple-context approach gives the AI far more to work with than just raw source code, resulting in more accurate and useful responses.

---

## Features

- 4 analysis modes via simple POST endpoints
- Python AST traversal for structural context (never shown to the user)
- Real runtime output captured before AI analysis
- Structured JSON responses validated with Pydantic schemas
- Lightweight Flask backend, easy to extend

---

## Analysis Modes

| Mode | Endpoint | Description |
|------|----------|-------------|
| **Explain** | `POST /explain` | Clear, concise summary of what the code does |
| **ELI5** | `POST /eli5` | Explains the code using simple analogies for beginners |
| **Debug** | `POST /debug` | Identifies all errors in detail and suggests fixes |
| **Optimize** | `POST /optimize` | Highlights inefficiencies and returns improved code |

---

## Project Structure

```
backend/
├── main.py          # Flask app — defines all API routes
├── gem_api.py       # Gemini API integration — builds prompts, calls model
├── parser.py        # AST builder — traverses code into a JSON tree
├── exec.py          # Executes user code, captures stdout/stderr
└── data_model.py    # Pydantic schemas for structured AI responses
```

---

## How It Works

Every request goes through the same pipeline:

```
User Code
    │
    ├──► parser.py   →  AST JSON tree (structure)
    ├──► exec.py     →  stdout + runtime errors (behavior)
    └──► gem_api.py  →  combines all context → Gemini → JSON response
```

The AST is used internally to enrich the prompt — it's never mentioned or exposed in the response to the user.

---

## API Reference

### Request Format

All endpoints accept a JSON body:

```json
{ "code": "<your python code here>" }
```

If no code is provided, a default bubble sort example is used.

### Endpoints

#### `POST /explain`
Returns a plain-language summary of what the code does.
```json
{ "Explanation": "..." }
```

#### `POST /eli5`
Explains the code using simple, beginner-friendly analogies.
```json
{ "Eli5_Explanation": "..." }
```

#### `POST /debug`
Identifies bugs and runtime errors with detailed fix suggestions.
```json
{ "bugs_explanation": "..." }
```

#### `POST /optimize`
Highlights inefficiencies and returns an improved version of the code.
```json
{ "Optimized_code": "..." }
```

---

## Setup & Installation

### Prerequisites
- Python 3.8+
- A [Google Gemini API key](https://aistudio.google.com/app/apikey)

### Install dependencies

```bash
pip install flask pydantic google-genai requests
```

### Configure your API key

In `gem_api.py`, replace the placeholder with your Gemini API key:

```python
client_explain = genai.Client(api_key="YOUR_API_KEY_HERE")
```

### Run the server

```bash
python main.py
```

Server starts at `http://127.0.0.1:5000`

---

## Example

```bash
curl -X POST http://127.0.0.1:5000/explain \
     -H "Content-Type: application/json" \
     -d '{"code": "print(sum(range(10)))"}'
```

```json
{
  "Explanation": "This code calculates the sum of all integers from 0 to 9 using Python's built-in range and sum functions, then prints the result (45) to the console."
}
```

---

## Tech Stack

- **Python** — Core language
- **Flask** — Web framework & API layer
- **Google Gemini API** — AI model (`gemini-2-flash-preview`)
- **Pydantic** — Response schema validation
- **`ast`** (stdlib) — Static code analysis & AST traversal
- **`io` / `sys` / `traceback`** (stdlib) — Code execution & error capture

---

## Notes

- The `exec()` sandbox captures stdout/stderr but does **not** provide OS-level isolation. Avoid running untrusted code in production without additional sandboxing.
- Each analysis mode uses its own Gemini client instance, making it easy to assign separate API keys or rate limits per mode later.

---

## Author

**Souban Ali** — [github.com/Soubanali](https://github.com/Soubanali)
