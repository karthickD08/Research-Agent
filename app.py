import streamlit as st

from agent import ResearchAgent

st.set_page_config(
    page_title="ResearchPilot",
    page_icon="🔎",
    layout="wide",
)

st.title("🔎 ResearchPilot")
st.caption("A tool-using research agent that searches the web, evaluates evidence, and cites sources.")

with st.sidebar:
    st.header("Agent")
    st.write("**Search tool:** Tavily")
    st.write("**LLM:** OpenAI Responses API")
    st.write("**Output:** Evidence-backed report with verified source IDs")
    st.divider()
    st.info(
        "API keys are read from Streamlit Secrets in deployment or a local .env file during development."
    )

question = st.text_area(
    "Research question",
    placeholder="Example: What are the latest developments in quantum computing and how could they affect AI?",
    height=120,
)

research_button = st.button("🔍 Research", type="primary", use_container_width=True)

if research_button:
    if not question.strip():
        st.warning("Enter a research question first.")
        st.stop()

    with st.status("ResearchPilot is working...", expanded=True) as status:
        try:
            st.write("Planning research queries...")
            agent = ResearchAgent()

            result = agent.research(question)

            st.write("Web search completed.")
            st.write(f"Collected {len(result['sources'])} unique sources.")
            st.write("Synthesizing evidence and validating citations...")

            status.update(label="Research completed", state="complete")

        except Exception as exc:
            status.update(label="Research failed", state="error")
            st.error(str(exc))
            st.stop()

    st.markdown(result["report"])

    st.divider()
    st.subheader("Sources")

    for source in result["sources"]:
        st.markdown(
            f"**[{source['id']}] {source['title']}**  \n"
            f"{source['url']}  \n"
            f"Relevance: `{source.get('score', 0):.2f}` · "
            f"Quality estimate: `{source.get('quality', 0):.2f}`"
        )

    with st.expander("Agent tool-use trace"):
        for item in result["trace"]:
            st.write(
                f"Round {item['round']} — `{item['query']}` — "
                f"{item['results']} results"
            )

    with st.expander("Research plan"):
        st.write(result["research_goal"])
        for area in result["focus_areas"]:
            st.write(f"- {area}")
