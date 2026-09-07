# Conversion Summary: OpenAI → Gemini

## Quick Reference: What Changed

### Files Modified
1. ✅ **agent.py** - API calls updated to Gemini
2. ✅ **config.py** - Configuration keys changed
3. ✅ **requirements.txt** - Dependencies updated
4. ✅ **.env.example** - Environment variables updated

### Files Unchanged
- prompts.py
- search_tool.py
- source_manager.py
- app.py
- main.py
- tests/

## Before and After

### Import Statement
```diff
- from openai import OpenAI
+ import google.generativeai as genai
```

### Client Setup
```diff
- self.client = OpenAI(api_key=settings.openai_api_key)
+ genai.configure(api_key=settings.gemini_api_key)
+ self.client = genai.GenerativeModel(model_name=settings.gemini_model)
```

### API Calls
```diff
- response = self.client.responses.create(
-     model=settings.openai_model,
-     instructions=SYSTEM_PROMPT,
-     input=prompt,
- )
- text = response.output_text.strip()

+ response = self.client.generate_content(
+     contents=[{"role": "user", "parts": [{"text": prompt}]}],
+     generation_config=genai.types.GenerationConfig(temperature=0.7),
+     system_instruction=SYSTEM_PROMPT,
+ )
+ text = response.text.strip()
```

### Configuration
```diff
- openai_api_key: str = get_secret("OPENAI_API_KEY")
- openai_model: str = get_secret("OPENAI_MODEL", "gpt-5.6-luna")

+ gemini_api_key: str = get_secret("GEMINI_API_KEY")
+ gemini_model: str = get_secret("GEMINI_MODEL", "gemini-2.0-flash")
```

### Dependencies
```diff
- openai>=1.100.0
+ google-generativeai>=0.3.0
```

## Quick Start
1. Install dependencies: `pip install -r requirements.txt`
2. Get API key: https://aistudio.google.com/app/apikey
3. Update `.env`: Replace `GEMINI_API_KEY` with your key
4. Run: `streamlit run app.py`

## Model Recommendations
- **Default:** `gemini-2.0-flash` (fast & cost-effective)
- **Best Quality:** `gemini-1.5-pro` (slower, higher cost)
- **Budget:** `gemini-1.5-flash` (faster, lower cost)

See MIGRATION_GUIDE.md for detailed documentation.
