# Claude AI — Function Calling (Tool Use) in Python

A clean & multi-tool demonstration of Claude's **tool use (function calling)** capability using the Anthropic Python SDK.

---

## What This Does

Sends user prompts to Claude. If Claude decides a tool is needed, the app:
1. Receives the tool call request from Claude
2. Runs the corresponding Python function locally
3. Returns the result back to Claude
4. Gets a natural-language final response

Supports multiple tool calls in a single turn.

---

## Included Tools

| Tool | Description |
|---|---|
| `score_checker` | Pass/Fail based on a 0.0–1.0 score |
| `calculator` | Evaluates math expressions safely |
| `get_weather` | Returns weather for a city (mock data — swap in a real API) |

---

## Setup
```bash
# 1. Clone the repo
git clone https://github.com/AdarshZolekar/Claude-Function-Calling
cd Claude-Function-Calling

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your API key
echo "ANTHROPIC_API_KEY=your_key_here" > .env

# 4. Run the demo
python Main.py
```

---

## Adding a New Tool

1. Add the JSON schema to the `TOOLS` list in `tools.py`
2. Implement the Python function
3. Register it in `_REGISTRY`

No changes needed in `main.py`.

---

## Project Structure
```
├── main.py           # Conversation loop with tool-use handling
├── tools.py          # Tool schemas + implementations + dispatcher
├── requirements.txt
└── example.env       # Your ANTHROPIC_API_KEY (not committed)
```

---

## References

- [Anthropic Tool Use Docs](https://docs.anthropic.com/en/docs/tool-use)
- [Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python)

---

## License

This project is open-source under the MIT License.

---

## Contributions

Contributions are welcome!

- Open an issue for bugs or feature requests

- Submit a pull request for improvements.


<p align="center">
  <a href="#top">
    <img src="https://img.shields.io/badge/%E2%AC%86-Back%20to%20Top-blue?style=for-the-badge" alt="Back to Top"/>
  </a>
</p>

