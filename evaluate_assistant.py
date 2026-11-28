"""
Evaluates the assistant as users experience it: rules + model + suggestions.

train.py measures the model alone. This script adds what happens when the
model is unsure: the greeting/thanks rule and the "Ito ba ang ibig mong
sabihin?" buttons (the two closest topics). It uses the same three-fold
cross-validation, repeated on five different splits so the result is not
luck of one split.

Run:  python evaluate_assistant.py
Writes assistant_metrics.json.
"""

import json
import platform
from pathlib import Path

import numpy as np
import sklearn
from sklearn.base import clone
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import make_pipeline

from chatbot_engine import (
    MAX_SUGGESTIONS,
    MIN_SUGGESTION_PROBABILITY,
    THRESHOLD,
    build_vocabulary,
    is_meaningful,
    smalltalk_response,
)
from train import load_dataset

BASE = Path(__file__).resolve().parent
SEEDS = range(5)


def model():
    # Same model as train.py.
    return make_pipeline(
        TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4)),
        LogisticRegression(C=10, max_iter=2000, random_state=42),
    )


def evaluate(texts, targets, seed):
    out_of_scope = targets == "out_of_scope"
    direct_right = np.zeros(len(targets), bool)
    direct_wrong = np.zeros(len(targets), bool)
    suggested_right = np.zeros(len(targets), bool)
    model_only_right = np.zeros(len(targets), bool)

    folds = StratifiedKFold(n_splits=3, shuffle=True, random_state=seed)

    for train_ids, test_ids in folds.split(texts, targets):
        fitted = clone(model()).fit(texts[train_ids], targets[train_ids])
        # Same check as the engine: no suggestions for messages without a
        # single known word (from this fold's training questions only).
        vocabulary = build_vocabulary(
            texts[i] for i in train_ids if targets[i] != "out_of_scope"
        )
        probabilities = fitted.predict_proba(texts[test_ids])
        labels = fitted.classes_

        for row, index in enumerate(test_ids):
            p = probabilities[row]
            best = int(p.argmax())
            predicted = labels[best]
            answered = p[best] >= THRESHOLD and predicted != "out_of_scope"
            model_only_right[index] = answered and predicted == targets[index]

            rule = smalltalk_response(texts[index])
            if rule is not None:
                direct_right[index] = rule.intent == targets[index]
                direct_wrong[index] = rule.intent != targets[index]
                continue

            if answered:
                direct_right[index] = predicted == targets[index]
                direct_wrong[index] = predicted != targets[index]
                continue

            picks = [
                labels[j] for j in p.argsort()[::-1]
                if labels[j] != "out_of_scope" and p[j] >= MIN_SUGGESTION_PROBABILITY
            ][:MAX_SUGGESTIONS] if is_meaningful(texts[index], vocabulary) else []
            suggested_right[index] = targets[index] in picks

    in_scope = ~out_of_scope
    return {
        "model_only_answered_right": model_only_right[in_scope].mean(),
        "answered_right_directly": direct_right[in_scope].mean(),
        "answered_right_or_suggested": (direct_right | suggested_right)[in_scope].mean(),
        "wrong_direct_answers": int(direct_wrong.sum()),
        "out_of_scope_answered": direct_wrong[out_of_scope].mean(),
    }


def main():
    frame, _ = load_dataset()
    texts = frame["text"].to_numpy()
    targets = frame["label"].to_numpy()

    runs = [evaluate(texts, targets, seed) for seed in SEEDS]
    summary = {key: float(np.mean([run[key] for run in runs])) for key in runs[0]}

    print(f"In-scope questions, averaged over {len(runs)} splits:")
    print(f"  Model alone, answered right:          {summary['model_only_answered_right']:.1%}")
    print(f"  With greeting rule, answered right:   {summary['answered_right_directly']:.1%}")
    print(f"  ...or right topic offered as a button: {summary['answered_right_or_suggested']:.1%}")
    print(f"Wrong direct answers: {summary['wrong_direct_answers']:.0f}")
    print(f"Out-of-scope questions answered:        {summary['out_of_scope_answered']:.1%}")

    metrics = {
        "evaluation": "three-fold cross-validation, repeated on five splits",
        "threshold": THRESHOLD,
        "max_suggestions": MAX_SUGGESTIONS,
        "min_suggestion_probability": MIN_SUGGESTION_PROBABILITY,
        **summary,
        "python_version": platform.python_version(),
        "sklearn_version": sklearn.__version__,
    }

    with (BASE / "assistant_metrics.json").open("w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=2)

    print("\nSaved: assistant_metrics.json")


if __name__ == "__main__":
    main()
