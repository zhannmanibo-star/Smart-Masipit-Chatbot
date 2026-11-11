from chatbot_engine import ChatbotEngine


def main():
    engine = ChatbotEngine()

    print(
        "SMART MASIPIT Virtual Assistant. "
        "Type 'exit' para tumigil.\n"
    )

    while True:
        try:
            message = input("Ikaw: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nPaalam!")
            break

        if not message:
            continue

        if message.lower() == "exit":
            break

        try:
            result = engine.get_response(message)
        except ValueError as exception:
            print(f"Bot: {exception}\n")
            continue

        print(f"Bot: {result.reply}")

        if result.confidence is None:
            score = "N/A — rule-based"
        else:
            score = f"{result.confidence:.2f}"

        print(
            f"     [debug: {result.intent}, "
            f"{score}, {result.source}]\n"
        )


if __name__ == "__main__":
    main()