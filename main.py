from agent import ResearchAgent


def main() -> None:
    question = input("Research question: ").strip()

    if not question:
        print("Please enter a research question.")
        return

    agent = ResearchAgent()
    result = agent.research(question)

    print("\n" + result["report"])
    print("\n## Sources")
    for source in result["sources"]:
        print(f"[{source['id']}] {source['title']}")
        print(source["url"])
        print()


if __name__ == "__main__":
    main()
