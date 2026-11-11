import csv
from datetime import datetime
from pathlib import Path

from chatbot_engine import ChatbotEngine


BASE_DIR = Path(__file__).resolve().parent

FIELDS = [
    "tested_at",
    "question",
    "reply",
    "predicted_intent",
    "confidence",
    "source",
    "rating",
    "expected_behavior",
]


def main():
    engine = ChatbotEngine()

    filename = (
        "user_test_"
        + datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        + ".csv"
    )
    output_path = BASE_DIR / filename

    counts = {
        "correct": 0,
        "incorrect": 0,
        "unnecessary_fallback": 0,
        "needs_review": 0,
    }

    ratings = {
        "1": "correct",
        "2": "incorrect",
        "3": "unnecessary_fallback",
        "4": "needs_review",
    }

    print("\nSMART MASIPIT — User Testing")
    print("Gumamit ng bagong tanong sa sariling pananalita.")
    print("Huwag magsama ng personal o patient information.")
    print("Type 'exit' para matapos.\n")

    try:
        with output_path.open(
            "x",
            newline="",
            encoding="utf-8-sig",
        ) as file:
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            writer.writeheader()
            file.flush()

            while True:
                question = input("Tanong: ").strip()

                if question.lower() == "exit":
                    break

                if not question:
                    continue

                try:
                    result = engine.get_response(question)
                except ValueError as exception:
                    print(f"\n{exception}\n")
                    continue

                print(f"\nBot: {result.reply}\n")

                print("I-rate ang sagot:")
                print(
                    "1 = Tama at angkop "
                    "(kasama ang tamang pagtanggi/clarification)"
                )
                print("2 = Mali o hindi tumutugon sa tanong")
                print(
                    "3 = Unnecessary fallback "
                    "(malinaw at supported ang tanong)"
                )
                print("4 = Hindi matiyak; kailangan ng review")

                choice = input("Rating [1–4]: ").strip()

                while choice not in ratings:
                    choice = input(
                        "Pumili lamang ng 1, 2, 3, o 4: "
                    ).strip()

                rating = ratings[choice]

                expected_behavior = input(
                    "Ano ang dapat na sagot/handling? "
                    "(Enter kung walang note): "
                ).strip()

                writer.writerow({
                    "tested_at": datetime.now()
                    .astimezone()
                    .isoformat(timespec="seconds"),
                    "question": question,
                    "reply": result.reply,
                    "predicted_intent": result.intent,
                    "confidence": (
                        ""
                        if result.confidence is None
                        else f"{result.confidence:.6f}"
                    ),
                    "source": result.source,
                    "rating": rating,
                    "expected_behavior": expected_behavior,
                })
                file.flush()
                counts[rating] += 1

                confidence = (
                    "N/A — rule-based"
                    if result.confidence is None
                    else f"{result.confidence:.4f}"
                )

                print(
                    f"\nSaved. Debug: {result.intent} | "
                    f"{confidence} | {result.source}\n"
                )

    except (KeyboardInterrupt, EOFError):
        print("\nTesting stopped. Completed ratings are saved.")

    total = sum(counts.values())

    print("\nRESULTS")
    print(f"Total rated questions: {total}")
    print(f"Tama at angkop: {counts['correct']}")
    print(f"Mali: {counts['incorrect']}")
    print(
        "Unnecessary fallback: "
        f"{counts['unnecessary_fallback']}"
    )
    print(f"Needs review: {counts['needs_review']}")

    if total:
        rate = counts["correct"] / total * 100
        print(
            f"Rated correct / all rated questions: {rate:.1f}%"
        )

    print(
        "\nHuman-rated test results ito, "
        "hindi training/CV accuracy."
    )
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()