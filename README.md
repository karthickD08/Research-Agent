# 🔎 ResearchPilot — Tool-Using Research Agent

ResearchPilot is an AI research agent that answers research questions by **planning searches, calling a real web-search tool, collecting evidence, checking for evidence gaps, and producing a cited research report**.

This project is designed as a portfolio/internship demonstration of practical agentic AI.

## Why this is an agent

The system is not a simple chatbot.

It follows an agent loop:

```text
User Question
     ↓
Research Planner (LLM)
     ↓
Search Tool → Tavily Web Search
     ↓
Source Deduplication + Quality Scoring
     ↓
Evidence Gap Analysis (LLM)
     ↓
Optional Follow-up Search
     ↓
Evidence-grounded Synthesis (LLM)
     ↓
Citation Validation
     ↓
Research Report + Sources
```

The search capability is implemented as a separate tool in `search_tool.py`, and the agent explicitly invokes that tool during its research loop.

## Features

- LLM-generated research plan
- Real-time web search through Tavily
- Multiple search queries per research task
- Evidence collection and deduplication
- Basic source-quality scoring
- Second research round when evidence gaps are detected
- Evidence-grounded synthesis
- Inline source citations such as `[S1]`
- Citation validation against the actual retrieved source set
- Tool-use trace for transparency
- Streamlit UI
- CLI mode
- Unit tests
- Secrets excluded from Git

## Project Structure

```text
researchpilot-agent/
│
├── app.py
├── main.py
├── agent.py
├── search_tool.py
├── source_manager.py
├── prompts.py
├── config.py
│
├── requirements.txt
├── .env.example
├── .gitignore
│
├── .streamlit/
│   └── config.toml
│
├── tests/
│   ├── test_source_manager.py
│   └── test_citations.py
│
└── screenshots/
```

## Prerequisites

- Python 3.10+
- An OpenAI API key
- A Tavily API key

Tavily provides a free tier for development; check the current Tavily pricing/usage limits before deploying publicly.

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/researchpilot-agent.git
cd researchpilot-agent
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env`.

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Then edit `.env`:

```env
OPENAI_API_KEY=your_key
TAVILY_API_KEY=your_key
OPENAI_MODEL=gpt-5.6-luna
```

Never commit `.env`.

### 5. Run the Streamlit app

```bash
streamlit run app.py
```

Open the local URL shown by Streamlit.

## CLI Usage

You can also run the agent without Streamlit:

```bash
python main.py
```

Then enter a research question.

## Example Questions

```text
What are the latest developments in quantum computing and how could they affect AI?

What are the environmental impacts of generative AI data centers?

How is AI changing software engineering productivity?

What are the current approaches to detecting AI-generated misinformation?
```

## How citations work

The search tool returns source metadata including:

- title
- URL
- search relevance score
- content snippet

The agent assigns IDs such as:

```text
[S1]
[S2]
[S3]
```

The synthesizer is instructed to cite only those IDs.

A final validation step removes citation IDs that do not exist in the retrieved source set.

The application then displays the actual source URLs below the report.

## Source-quality scoring

The project uses a lightweight heuristic:

- Government domains: high
- Academic/university domains: high
- Major scientific publishers: high
- Reputable news organizations: medium-high
- Other domains: general

This is a ranking aid, not a claim that a domain is automatically authoritative.

## Limitations

- Search quality depends on the Tavily search index.
- LLM-generated plans and summaries can still contain errors.
- Source-quality scoring is heuristic.
- Citation validation checks whether a cited source exists, not whether every individual claim is perfectly supported.
- Public deployment can consume API credits quickly.

## Testing

Run:

```bash
pytest
```

## Streamlit Cloud Deployment

1. Push this repository to GitHub.
2. Open Streamlit Community Cloud.
3. Create a new app.
4. Select this GitHub repository.
5. Set the main file to:

```text
app.py
```

6. Add secrets in the Streamlit app settings:

```toml
OPENAI_API_KEY = "your-openai-key"
TAVILY_API_KEY = "your-tavily-key"
OPENAI_MODEL = "gpt-5.6-luna"
MAX_SEARCH_RESULTS = "5"
MAX_QUERIES_PER_ROUND = "4"
MAX_RESEARCH_ROUNDS = "2"
```

Do not put API keys inside GitHub.

## Security

The repository intentionally contains no API keys.

The following are ignored by Git:

```text
.env
.streamlit/secrets.toml
```

If a secret is accidentally committed, revoke/rotate it immediately.

## Future Improvements

- Add source-domain allowlists for academic research
- Add URL content extraction for deeper evidence
- Add claim-to-source entailment checking
- Add persistent research sessions
- Add PDF research export
- Add source clustering by topic
- Add confidence estimation
- Add evaluation benchmark with citation precision/recall
- Add parallel search execution
- Add support for additional search providers

## License

MIT License.
