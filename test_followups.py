"""
Tests follow-up questions: a short question that depends on the one before
it ("paano kumuha ng clearance?" -> "magkano naman?").

Each row of followup_questions.csv has the previous question, the follow-up
and the topic it should get. The assistant is asked the follow-up alone and
with the previous question as context.

Run:  python test_followups.py
"""

import csv
import inspect
from pathlib import Path

from chatbot_engine import ChatbotEngine

BASE = Path(__file__).resolve().parent
NOT_ANSWERED = {"unknown", "out_of_scope", "language_switch"}


def outcome(result, expected):
    if result.intent == expected:
        return "right"
    if result.intent in NOT_ANSWERED:
        return "suggested" if expected in result.suggestions else "not answered"
    return "wrong answer"


def main():
    engine = ChatbotEngine()
    supports_context = "context" in inspect.signature(engine.get_response).parameters

    with (BASE / "followup_questions.csv").open(encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))

    totals = {"alone": {}, "with context": {}}
    for row in rows:
        alone = outcome(engine.get_response(row["question"]), row["expected"])
        totals["alone"][alone] = totals["alone"].get(alone, 0) + 1

        if supports_context:
            first = engine.get_response(row["previous"])
            result = engine.get_response(row["question"], previous=first.key, context=row["previous"])
            with_context = outcome(result, row["expected"])
            totals["with context"][with_context] = totals["with context"].get(with_context, 0) + 1
            if with_context != "right":
                print(f"  {with_context:12} {row['previous']} -> {row['question']}  (expected {row['expected']}, got {result.intent})")

    print(f"{len(rows)} follow-up questions")
    for name, counts in totals.items():
        if not counts:
            continue
        right = counts.get("right", 0)
        suggested = counts.get("suggested", 0)
        print(f"  {name:13} right {right / len(rows):.0%}   right or suggested {(right + suggested) / len(rows):.0%}   wrong {counts.get('wrong answer', 0)}")


if __name__ == "__main__":
    main()
