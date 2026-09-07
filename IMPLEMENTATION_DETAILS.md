# Implementation Details: OpenAI vs Gemini

## 1. Import and Initialization

### OpenAI Implementation
```python
from openai import OpenAI

class ResearchAgent:
    def __init__(self) -> None:
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is missing...")
        
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.search_tool = SearchTool()
```

### Gemini Implementation
```python
import google.generativeai as genai

class ResearchAgent:
    def __init__(self) -> None:
        if not settings.gemini_api_key:
            raise RuntimeError("GEMINI_API_KEY is missing...")
        
        genai.configure(api_key=settings.gemini_api_key)
        self.client = genai.GenerativeModel(model_name=settings.gemini_model)
        self.search_tool = SearchTool()
```

**Key Differences:**
- Gemini uses module-level configuration via `genai.configure()`
- Gemini client is created with `GenerativeModel()` instead of `OpenAI()` instance
- Model name is specified when creating the client

---

## 2. JSON Generation (Structured Output)

### OpenAI Implementation
```python
def _json_call(self, prompt: str) -> dict[str, Any]:
    response = self.client.responses.create(
        model=settings.openai_model,
        instructions=SYSTEM_PROMPT,
        input=prompt,
    )
    text = response.output_text.strip()
    
    # Handle markdown fences
    text = re.sub(r"^```json\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    
    return json.loads(text)
```

### Gemini Implementation
```python
def _json_call(self, prompt: str) -> dict[str, Any]:
    response = self.client.generate_content(
        contents=[
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ],
        generation_config=genai.types.GenerationConfig(
            temperature=0.7,
        ),
        system_instruction=SYSTEM_PROMPT,
    )
    text = response.text.strip()
    
    # Handle markdown fences
    text = re.sub(r"^```json\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    
    return json.loads(text)
```

**Key Differences:**
- `generate_content()` vs `responses.create()`
- Gemini requires structured `contents` with role and parts
- Gemini uses `system_instruction` parameter
- Response attribute is `.text` instead of `.output_text`
- Generation parameters use `GenerationConfig` object

---

## 3. Text Generation (Synthesis)

### OpenAI Implementation
```python
def synthesize(self, question: str, sources: list[dict]) -> str:
    prompt = f"{SYNTHESIS_PROMPT}\n\n..."
    
    response = self.client.responses.create(
        model=settings.openai_model,
        instructions=SYSTEM_PROMPT,
        input=prompt,
    )
    return response.output_text.strip()
```

### Gemini Implementation
```python
def synthesize(self, question: str, sources: list[dict]) -> str:
    prompt = f"{SYNTHESIS_PROMPT}\n\n..."
    
    response = self.client.generate_content(
        contents=[
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ],
        system_instruction=SYSTEM_PROMPT,
    )
    return response.text.strip()
```

**Key Differences:**
- Same as JSON call but without `generation_config`
- Default generation parameters are used for synthesis

---

## 4. Configuration Class

### OpenAI Configuration
```python
@dataclass(frozen=True)
class Settings:
    openai_api_key: str = get_secret("OPENAI_API_KEY")
    openai_model: str = get_secret(
        "OPENAI_MODEL",
        "gpt-5.6-luna"
    )
    # ... other settings
```

### Gemini Configuration
```python
@dataclass(frozen=True)
class Settings:
    gemini_api_key: str = get_secret("GEMINI_API_KEY")
    gemini_model: str = get_secret(
        "GEMINI_MODEL",
        "gemini-2.0-flash"
    )
    # ... other settings
```

---

## 5. Response Object Comparison

### OpenAI Response Structure
```
Response
├── output_text: str
├── usage: dict
│   ├── prompt_tokens
│   ├── completion_tokens
│   └── total_tokens
└── finish_reason: str
```

### Gemini Response Structure
```
GenerateContentResponse
├── text: str
├── candidates: list[Candidate]
│   └── content
│       └── parts: list[Part]
├── usage_metadata: dict
│   ├── prompt_token_count
│   ├── candidates_token_count
│   └── total_token_count
└── prompt_feedback: dict
```

---

## 6. Environment Variables

### OpenAI (.env)
```
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
OPENAI_MODEL=gpt-5.6-luna
```

### Gemini (.env)
```
GEMINI_API_KEY=AIzaSyxxxxxxxxxxxxx
GEMINI_MODEL=gemini-2.0-flash
```

**Note:** Gemini API keys typically start with `AIzaSy`

---

## 7. Generation Configuration Options

### Gemini GenerationConfig Parameters
```python
generation_config=genai.types.GenerationConfig(
    temperature=0.7,              # 0.0 to 2.0 (0.7 is default)
    top_p=0.95,                   # Nucleus sampling
    top_k=40,                      # Top-k sampling
    max_output_tokens=2048,        # Max response length
    stop_sequences=["END"],        # Stop at these sequences
    candidate_count=1,             # Number of responses
)
```

### Recommended Settings for Research
```python
# For planning (JSON) - more deterministic
GenerationConfig(temperature=0.5, top_p=0.9)

# For synthesis - more creative/varied
GenerationConfig(temperature=0.8, top_p=0.95)
```

---

## 8. Error Handling

### Gemini-Specific Exceptions
```python
try:
    response = self.client.generate_content(...)
except google.generativeai.types.StopCandidateException:
    # Content was blocked or stopped
    pass
except google.generativeai.types.HarmBlockedError:
    # Content safety filter triggered
    pass
```

---

## 9. Model Selection Guide

| Aspect | Gemini 2.0 Flash | Gemini 1.5 Pro | Gemini 1.5 Flash |
|--------|------------------|----------------|-----------------|
| Speed | Very Fast ⚡⚡⚡ | Fast ⚡⚡ | Very Fast ⚡⚡⚡ |
| Quality | Excellent ⭐⭐⭐⭐ | Outstanding ⭐⭐⭐⭐⭐ | Good ⭐⭐⭐ |
| Cost | Low 💰 | Medium 💰💰 | Low 💰 |
| Context | 1M tokens | 1M tokens | 1M tokens |
| Best For | Default choice | Accuracy-critical | Budget-conscious |

---

## 10. Testing Compatibility

**Good News:** The test suite requires no changes!

- Tests in `tests/` directory use mocks or don't depend on API specifics
- The `search_tool.py` uses Tavily API (unchanged)
- JSON validation logic remains identical

```bash
pytest tests/  # Works without modification
```

---

## Performance Characteristics

### Latency (Typical)
- **OpenAI GPT-4:** 2-4 seconds per request
- **Gemini 2.0 Flash:** 1-2 seconds per request
- **Gemini 1.5 Pro:** 1-3 seconds per request

### Token Usage (Example: Research Report)
- **Planning:** ~50-100 input, ~100-200 output tokens
- **Gap Analysis:** ~200-300 input, ~50-100 output tokens
- **Synthesis:** ~500-1000 input, ~500-1500 output tokens

### Cost per 1000 Requests (Approximate)
- **OpenAI GPT-4:** $10-20
- **Gemini 2.0 Flash:** $2-5
- **Gemini 1.5 Pro:** $5-10

---

## Debugging Tips

### Enable Debug Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Response Object
```python
response = self.client.generate_content(...)
print(f"Text: {response.text}")
print(f"Candidates: {response.candidates}")
print(f"Usage: {response.usage_metadata}")
```

### Validate API Key
```python
genai.configure(api_key="your_key")
genai.list_models()  # This will fail if key is invalid
```

---

## Additional Resources

- [Google AI Studio](https://aistudio.google.com/)
- [Gemini API Docs](https://ai.google.dev/docs)
- [Python SDK Reference](https://ai.google.dev/api/python/google/generativeai)
- [Model Comparison](https://ai.google.dev/models/gemini)
