"""
Tests the whole assistant (rules + model + suggestion buttons + English
replies) on real_questions.csv: everyday questions written separately from
intents.json, in Tagalog, English and Taglish, with typos.

Unlike train.py and evaluate_assistant.py, none of these questions are
training examples, so this shows how the chatbot does on new questions.

Run:  python test_real_questions.py
Writes real_questions_results.csv (one row per question) and
real_questions_metrics.json.
"""

import csv
import json
from collections import Counter
from pathlib import Path

from chatbot_engine import ChatbotEngine

BASE = Path(__file__).resolve().parent
NOT_ANSWERED = {"unknown", "out_of_scope"}


def main():
    engine = ChatbotEngine()
    known = set(map(str, engine.model.classes_))

    with (BASE / "real_questions.csv").open(encoding="utf-8-sig", newline="") as file:
        questions = list(csv.DictReader(file))

    rows = []
    for item in questions:
        question, expected = item["question"], item["expected"]
        result = engine.get_response(question)
        answered = result.intent not in NOT_ANSWERED

        if expected == "out_of_scope":
            outcome = "wrong answer" if answered else "right (not answered)"
        elif result.intent == expected:
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
            "topic_known_to_model": expected in known or expected == "out_of_scope",
        })

    in_scope = [r for r in rows if r["expected"] != "out_of_scope"]
    out_scope = [r for r in rows if r["expected"] == "out_of_scope"]
    count = Counter(r["outcome"] for r in in_scope)

    metrics = {
        "questions": len(rows),
        "in_scope": len(in_scope),
        "answered_right": count["right"] / len(in_scope),
        "right_or_suggested": (count["right"] + count["suggested"]) / len(in_scope),
        "not_answered": count["not answered"] / len(in_scope),
        "wrong_answers": sum(r["outcome"] == "wrong answer" for r in rows),
        "out_of_scope_refused": sum(r["outcome"] == "right (not answered)" for r in out_scope) / max(1, len(out_scope)),
    }

    print(f"{len(rows)} questions ({len(in_scope)} in scope, {len(out_scope)} out of scope)")
    print(f"  Answered right:              {metrics['answered_right']:.1%}")
    print(f"  ...or right topic suggested: {metrics['right_or_suggested']:.1%}")
    print(f"  Not answered:                {metrics['not_answered']:.1%}")
    print(f"  Wrong answers:               {metrics['wrong_answers']}")
    print(f"  Out-of-scope refused:        {metrics['out_of_scope_refused']:.1%}")

    with (BASE / "real_questions_results.csv").open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    (BASE / "real_questions_metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print("\nSaved: real_questions_results.csv, real_questions_metrics.json")


if __name__ == "__main__":
    main()
