from agent.agent import run_agent

def main():
    print("=" * 50)
    print("  AI Knowledge Agent powered by Endee")
    print("=" * 50)
    print("Type 'quit' to exit.\n")

    while True:
        question = input("You: ").strip()
        if question.lower() in ("quit", "exit", "q"):
            break
        if not question:
            continue
        answer = run_agent(question)
        print(f"\nAgent: {answer}\n")
        print("-" * 50)

if __name__ == "__main__":
    main()
