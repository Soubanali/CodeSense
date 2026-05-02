# 🧠 CodeSense — AI-Powered Python Code Analyzer

> Paste your Python code. Get instant explanation, debugging, optimization, or a kid-friendly breakdown — powered by Google Gemini.

---

## What is CodeSense?

CodeSense is a full-stack web application that analyzes Python code through **three layers of understanding**:

1. **AST Parsing** — your code's structure is extracted using Python's `ast` module
2. **Live Execution** — the code is actually run and output/errors are captured
3. **AI Analysis** — all context is sent to Google Gemini for intelligent feedback

This triple-context approach gives the AI far more to work with than just raw source code, resulting in more accurate and useful responses.

The project is split into two parts: a **Flask REST API** (backend) and a **standalone HTML/CSS/JS interface** (frontend).

---

## Features

- 4 analysis modes selectable from the UI
- Python AST traversal for structural context (never shown to the user)
- Real runtime output captured before AI analysis
- Structured JSON responses validated with Pydantic schemas
- Cyberpunk-themed frontend with typewriter output animation
- Copy-to-clipboard output support
- Keyboard shortcut: `Ctrl + Enter` to run analysis

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
codesense/
├── frontend/
│   └── index.html       # Single-file UI — all HTML, CSS, and JS included
│
└── backend/
    ├── main.py          # Flask app — defines all API routes
    ├── gem_api.py       # Gemini API integration — builds prompts, calls model
    ├── parser.py        # AST builder — traverses code into a JSON tree
    ├── exec.py          # Executes user code, captures stdout/stderr
    └── data_model.py    # Pydantic schemas for structured AI responses
```

---

## How It Works

Every analysis request goes through the same pipeline:

```
User Code (entered in browser)
    │
    └──► Flask Backend (localhost:5000)
              │
              ├──► parser.py   →  AST JSON tree (structure)
              ├──► exec.py     →  stdout + runtime errors (behavior)
              └──► gem_api.py  →  combines all context → Gemini → JSON response
                                                                        │
                                                              Frontend renders result
```

The AST is used internally to enrich the prompt — it's never mentioned or exposed to the user.

---

## Frontend

The frontend is a single self-contained `index.html` file. No build step, no dependencies to install.

### Features

- **Mode selector** — switch between Explain, ELI5, Debug, and Optimize with one click
- **Code editor panel** — syntax-highlighted textarea styled as a terminal window
- **Live status indicator** — dot changes color to reflect idle / loading / success / error states
- **Typewriter animation** — AI output streams character by character for a polished feel
- **Copy button** — copies the current output to clipboard instantly
- **Responsive layout** — adapts to mobile screens (mode buttons collapse to 2-column grid)

### Running the Frontend

Just open `index.html` in your browser. No server needed for the frontend itself — it communicates directly with the Flask backend via `fetch`.

> **Note:** The frontend points to `http://127.0.0.1:5000` by default. If you change the backend port or host, update the `BASE` constant at the top of the `<script>` block in `index.html`.

### Keyboard Shortcut

Press `Ctrl + Enter` inside the code editor to trigger analysis without reaching for the mouse.

---

## Backend

### API Reference

#### Request Format

All endpoints accept a JSON body:

```json
{ "code": "<your python code here>" }
```

If no code is provided, a default bubble sort example is used.

#### Endpoints

##### `POST /explain`
Returns a plain-language summary of what the code does.
```json
{ "Explanation": "..." }
```

##### `POST /eli5`
Explains the code using simple, beginner-friendly analogies.
```json
{ "Eli5_Explanation": "..." }
```

##### `POST /debug`
Identifies bugs and runtime errors with detailed fix suggestions.
```json
{ "bugs_explanation": "..." }
```

##### `POST /optimize`
Highlights inefficiencies and returns an improved version of the code.
```json
{ "Optimized_code": "..." }
```

---

## Setup & Installation

### Prerequisites
- Python 3.8+
- A [Google Gemini API key](https://aistudio.google.com/app/apikey)
- A modern browser (Chrome, Firefox, Edge, Safari)

### 1. Install backend dependencies

```bash
pip install flask pydantic google-genai requests
```

### 2. Configure your Gemini API key

In `backend/gem_api.py`, replace the placeholder with your key:

```python
client_explain = genai.Client(api_key="YOUR_API_KEY_HERE")
```

### 3. Start the backend server

```bash
cd backend
python main.py
```

Server starts at `http://127.0.0.1:5000`

### 4. Open the frontend

Open `frontend/index.html` directly in your browser. That's it — no additional setup required.

---

## Example

**Via the UI:** Select a mode, paste your code, click `▶ ANALYZE` (or press `Ctrl + Enter`).

**Via curl:**
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

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | HTML / CSS / JavaScript | UI, user input, result rendering |
| Backend | Python + Flask | API routing and orchestration |
| AI | Google Gemini API (`gemini-2-flash-preview`) | Code analysis and explanation |
| Validation | Pydantic | Structured response schemas |
| Static Analysis | `ast` (stdlib) | AST traversal for code structure |
| Execution | `io` / `sys` / `traceback` (stdlib) | Runtime output and error capture |

---

## Notes

- The `exec()` sandbox captures stdout/stderr but does **not** provide OS-level isolation. Avoid running untrusted code in production without additional sandboxing.
- Each analysis mode uses its own Gemini client instance, making it easy to assign separate API keys or rate limits per mode later.
- CORS must be enabled on the Flask backend if the frontend is served from a different origin. For local development (opening `index.html` as a file), most browsers allow `localhost` fetches without CORS issues.

---

## Author

**Souban Ali** — [github.com/Soubanali](https://github.com/Soubanali)
