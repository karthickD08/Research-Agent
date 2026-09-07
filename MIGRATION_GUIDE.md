# Migration Guide: OpenAI to Gemini API

This document outlines the changes made to convert the ResearchPilot Agent from using OpenAI API to Google Generative AI (Gemini) API.

## Changes Summary

### 1. **dependencies (requirements.txt)**
   - **Removed:** `openai>=1.100.0`
   - **Added:** `google-generativeai>=0.3.0`

### 2. **Configuration (config.py)**
   - Changed `openai_api_key` → `gemini_api_key`
   - Changed `openai_model` → `gemini_model`
   - Updated default model from `gpt-5.6-luna` to `gemini-2.0-flash`
   - Environment variable: `OPENAI_API_KEY` → `GEMINI_API_KEY`
   - Environment variable: `OPENAI_MODEL` → `GEMINI_MODEL`

### 3. **Agent Implementation (agent.py)**

#### Import Changes
```python
# Old
from openai import OpenAI

# New
import google.generativeai as genai
```

#### Client Initialization
```python
# Old
self.client = OpenAI(api_key=settings.openai_api_key)

# New
genai.configure(api_key=settings.gemini_api_key)
self.client = genai.GenerativeModel(model_name=settings.gemini_model)
```

#### API Call Changes

**Old (OpenAI):**
```python
response = self.client.responses.create(
    model=settings.openai_model,
    instructions=SYSTEM_PROMPT,
    input=prompt,
)
text = response.output_text.strip()
```

**New (Gemini):**
```python
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
```

### 4. **Environment File (.env.example)**
```
# Old
OPENAI_API_KEY=sk-proj-...
OPENAI_MODEL=gpt-5.6-luna

# New
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.0-flash
```

## Setup Instructions

### 1. Get a Gemini API Key
- Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
- Click "Create API Key" or "Get API Key"
- Copy your API key

### 2. Update Environment Variables
- Copy `.env.example` to `.env`
- Replace `your_gemini_api_key_here` with your actual Gemini API key
- Keep `TAVILY_API_KEY` as is

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
# For Streamlit app
streamlit run app.py

# For command-line usage
python main.py
```

## Available Gemini Models

Recommended models (with trade-offs):

| Model | Speed | Cost | Quality | Use Case |
|-------|-------|------|---------|----------|
| `gemini-2.0-flash` | ⚡⚡⚡ | 💰 | ⭐⭐⭐⭐ | Fast research, default choice |
| `gemini-1.5-pro` | ⚡⚡ | 💰💰 | ⭐⭐⭐⭐⭐ | High-quality synthesis |
| `gemini-1.5-flash` | ⚡⚡⚡ | 💰 | ⭐⭐⭐ | Budget-friendly option |

Update `GEMINI_MODEL` in `.env` to change the model.

## API Differences

### Temperature and Generation Config
Gemini uses `GenerationConfig` for controlling output behavior:

```python
generation_config=genai.types.GenerationConfig(
    temperature=0.7,
    top_p=0.95,
    top_k=40,
    max_output_tokens=2048,
)
```

### System Instructions
Gemini supports `system_instruction` parameter, which maps directly to the system prompt used before.

### Error Handling
Gemini may raise different exceptions:
- `google.generativeai.types.StopCandidateException`
- `google.generativeai.types.HarmBlockedError`

## Testing

Run the test suite:
```bash
pytest tests/
```

Note: Tests should work without modification as they don't depend on the API implementation.

## Common Issues

### Issue: "GEMINI_API_KEY is missing"
**Solution:** 
- Ensure your `.env` file contains `GEMINI_API_KEY=your_key_here`
- Or set the environment variable: `export GEMINI_API_KEY=your_key_here`

### Issue: "Could not parse API response"
**Solution:**
- Ensure `google-generativeai>=0.3.0` is installed
- Run: `pip install --upgrade google-generativeai`

### Issue: API Rate Limiting
**Solution:**
- Gemini has different rate limits than OpenAI
- Check [rate limit documentation](https://ai.google.dev/pricing)
- Consider adding delays between requests in production

## Rollback

If you need to revert to OpenAI:
1. Copy the original files from your backup
2. Or reinstall from the original repository
3. No database migrations needed

## Performance Notes

- **Latency:** Gemini 2.0 Flash is typically faster than GPT-4 variants
- **Cost:** Generally more cost-effective for high-volume usage
- **Quality:** Comparable to GPT-3.5/GPT-4 for research synthesis

## Additional Resources

- [Google AI Python SDK Docs](https://ai.google.dev/tutorials/python_quickstart)
- [Gemini API Reference](https://ai.google.dev/api/python/google/generativeai)
- [Pricing Calculator](https://ai.google.dev/pricing)

## Support

For issues with the Gemini API:
- Check [Google AI Support](https://issuetracker.google.com/issues?q=componentid:409819)
- Review [API Documentation](https://ai.google.dev/docs)

For issues with ResearchPilot itself:
- Check the main project repository
