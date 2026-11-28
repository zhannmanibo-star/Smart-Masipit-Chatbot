"""
Tests the assistant on staff_questions.csv: questions barangay staff ask
about their own work (scanning QR codes, approving requests, posting
announcements, recording ayuda), written separately from intents.json.

The questions are asked as a staff user who works in every area, so the
staff answers from staff_responses.py are used.

Run:  python test_staff_questions.py
Writes staff_questions_results.csv and staff_questions_metrics.json.
"""

import csv
import json
from collections import Counter
from pathlib import Path

from chatbot_engine import ChatbotEngine
from staff_responses import KNOWN_AREAS

BASE = Path(__file__).resolve().parent
NOT_ANSWERED = {"unknown", "out_of_scope"}


def main():
    engine = ChatbotEngine()
    areas = sorted(KNOWN_AREAS)

    with (BASE / "staff_questions.csv").open(encoding="utf-8-sig", newline="") as file:
        questions = list(csv.DictReader(file))

    rows = []
    for item in questions:
        question, expected = item["question"], item["expected"]
        result = engine.get_response(question, staff_areas=areas)
        answered = result.intent not in NOT_ANSWERED

        if result.intent == expected:
            outcome = "right"
        elif not answered and expected in result.suggestions:
            outcome = "suggested"
        elif not answered:
            outcome = "not answered"
        else:
            outcome = "wrong answer"

        rows.append({
            "question": question,
            "expected": expected,
            "got": result.intent,
            "confidence": "" if result.confidence is None else f"{result.confidence:.2f}",
            "suggestions": " | ".join(result.suggestions),
            "outcome": outcome,
        })

    count = Counter(r["outcome"] for r in rows)
    metrics = {
        "questions": len(rows),
        "answered_right": count["right"] / len(rows),
        "right_or_suggested": (count["right"] + count["suggested"]) / len(rows),
        "not_answered": count["not answered"] / len(rows),
        "wrong_answers": count["wrong answer"],
    }

    print(f"{len(rows)} staff questions")
    print(f"  Answered right:              {metrics['answered_right']:.1%}")
    print(f"  ...or right topic suggested: {metrics['right_or_suggested']:.1%}")
    print(f"  Not answered:                {metrics['not_answered']:.1%}")
    print(f"  Wrong answers:               {metrics['wrong_answers']}")

    for row in rows:
        if row["outcome"] != "right":
            print(f"  [{row['outcome']}] {row['question']} -> {row['got']} ({row['suggestions']})")

    with (BASE / "staff_questions_results.csv").open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    (BASE / "staff_questions_metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print("\nSaved: staff_questions_results.csv, staff_questions_metrics.json")


if __name__ == "__main__":
    main()
