import json
import platform
from pathlib import Path

import joblib
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn

from sklearn.base import clone
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
    f1_score,
)
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import make_pipeline

from chatbot_engine import normalize_text


BASE = Path(__file__).resolve().parent
SKIP_TAGS = {"autocorrect_typo_handling"}

THRESHOLD = 0.4
RANDOM_STATE = 42


def duplicate_key(text):
    return " ".join(text.lower().split()).strip(" ?!.,")


def load_dataset():
    with (BASE / "intents.json").open(
        encoding="utf-8-sig"
    ) as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError("intents.json must contain an object.")

    intents = data.get("intents")

    if not isinstance(intents, list) or not intents:
        raise ValueError("Missing or empty intents list.")

    rows = []
    responses = {}
    seen_tags = set()
    seen_questions = {}

    for intent in intents:
        tag = intent.get("tag")

        if not isinstance(tag, str) or not tag.strip():
            raise ValueError("Invalid intent tag.")

        if tag in seen_tags:
            raise ValueError(f"Duplicate tag: {tag}")

        seen_tags.add(tag)

        if tag in SKIP_TAGS:
            continue

        patterns = intent.get("patterns")
        answers = intent.get("responses")

        if not isinstance(patterns, list) or not patterns:
            raise ValueError(f"Missing patterns for {tag}")

        if (
            not isinstance(answers, list)
            or not answers
            or any(
                not isinstance(answer, str) or not answer.strip()
                for answer in answers
            )
        ):
            raise ValueError(f"Invalid responses for {tag}")

        responses[tag] = answers

        for pattern in patterns:
            if not isinstance(pattern, str) or not pattern.strip():
                raise ValueError(f"Invalid pattern in {tag}")

            key = duplicate_key(pattern)

            if key in seen_questions:
                previous_tag = seen_questions[key]

                if previous_tag != tag:
                    raise ValueError(
                        f"Conflicting labels: {previous_tag} / {tag}\n"
                        f"Question: {pattern}"
                    )

                # Identical examples should not inflate evaluation.
                continue

            seen_questions[key] = tag

            # Same preprocessing as the chatbot (lowercase and shortcuts).
            rows.append((normalize_text(pattern), tag))

    frame = pd.DataFrame(rows, columns=["text", "label"])

    if frame.empty or frame["label"].nunique() < 2:
        raise ValueError("At least two non-empty intents are required.")

    counts = frame["label"].value_counts()

    if counts.min() < 3:
        raise ValueError(
            "Every intent needs at least three distinct examples "
            "for three-fold cross-validation."
        )

    return frame, responses


def main():
    frame, responses = load_dataset()

    print(
        f"Kabuuang patterns: {len(frame)} "
        f"| Intents: {frame['label'].nunique()}"
    )
    print(frame["label"].value_counts().to_string())
    print()

    model = make_pipeline(
        TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(2, 4),
        ),
        LogisticRegression(
            C=10,
            max_iter=2000,
            random_state=RANDOM_STATE,
        ),
    )

    texts = frame["text"].to_numpy()
    targets = frame["label"].to_numpy()

    predictions = np.empty(len(frame), dtype=object)
    confidence = np.zeros(len(frame), dtype=float)

    folds = StratifiedKFold(
        n_splits=3,
        shuffle=True,
        random_state=RANDOM_STATE,
    )

    fold_accuracy = []
    fold_macro_f1 = []

    for fold_number, (train_ids, test_ids) in enumerate(
        folds.split(texts, targets),
        start=1,
    ):
        fold_model = clone(model)

        fold_model.fit(
            texts[train_ids],
            targets[train_ids],
        )

        probabilities = fold_model.predict_proba(texts[test_ids])
        best_indices = probabilities.argmax(axis=1)
        predicted_labels = fold_model.classes_[best_indices]

        predictions[test_ids] = predicted_labels
        confidence[test_ids] = probabilities.max(axis=1)

        accuracy = accuracy_score(
            targets[test_ids],
            predicted_labels,
        )

        macro_f1 = f1_score(
            targets[test_ids],
            predicted_labels,
            average="macro",
            zero_division=0,
        )

        fold_accuracy.append(accuracy)
        fold_macro_f1.append(macro_f1)

        print(
            f"Fold {fold_number}: "
            f"accuracy={accuracy:.3f}, macro F1={macro_f1:.3f}"
        )

    print(
        "\nMean CV accuracy: "
        f"{np.mean(fold_accuracy):.3f} "
        f"+/- {np.std(fold_accuracy):.3f}"
    )

    print(
        "Mean CV macro F1: "
        f"{np.mean(fold_macro_f1):.3f}"
    )

    print("\nCombined out-of-fold classification report:")
    print(
        classification_report(
            targets,
            predictions,
            zero_division=0,
        )
    )

    # Simulate the current API's answer/fallback rule.
    answered = (
        (confidence >= THRESHOLD)
        & (predictions != "out_of_scope")
    )

    correct = predictions == targets
    out_of_scope = targets == "out_of_scope"

    answer_count = int(answered.sum())
    coverage = float(answered.mean())

    print(f"\nThreshold: {THRESHOLD:.2f}")
    print(f"Answer coverage: {coverage:.1%}")
    print(f"Fallback rate: {1 - coverage:.1%}")

    if answer_count:
        accepted_accuracy = float(correct[answered].mean())

        print(
            "Correct intent among answered questions: "
            f"{accepted_accuracy:.1%}"
        )
    else:
        accepted_accuracy = None
        print("No questions passed the answer threshold.")

    if out_of_scope.any():
        oos_false_answer_rate = float(answered[out_of_scope].mean())

        print(
            "Out-of-scope questions incorrectly answered: "
            f"{oos_false_answer_rate:.1%}"
        )
    else:
        oos_false_answer_rate = None

    # Include both wrong predictions and questions sent to fallback.
    review = pd.DataFrame({
        "question": texts,
        "expected_intent": targets,
        "predicted_intent": predictions,
        "confidence": confidence,
        "api_action": np.where(answered, "answer", "fallback"),
        "intent_correct": correct,
    })

    review.to_csv(
        BASE / "cv_predictions.csv",
        index=False,
        encoding="utf-8-sig",
    )

    review.loc[~correct].sort_values(
        "confidence",
        ascending=False,
    ).to_csv(
        BASE / "cv_errors.csv",
        index=False,
        encoding="utf-8-sig",
    )

    confusion_pairs = (
        review.loc[~correct]
        .groupby(["expected_intent", "predicted_intent"])
        .size()
        .sort_values(ascending=False)
        .head(15)
    )

    print("\nMost common intent confusions:")
    print(confusion_pairs.to_string())

    labels = sorted(responses)

    matrix = confusion_matrix(
        targets,
        predictions,
        labels=labels,
    )

    fig, ax = plt.subplots(figsize=(19, 17))

    ConfusionMatrixDisplay(
        confusion_matrix=matrix,
        display_labels=labels,
    ).plot(
        ax=ax,
        xticks_rotation=90,
        colorbar=False,
        values_format="d",
    )

    ax.tick_params(axis="both", labelsize=7)
    fig.tight_layout()
    fig.savefig(BASE / "confusion_matrix.png", dpi=140)
    plt.close(fig)

    metrics = {
        "evaluation": "three-fold development cross-validation",
        "patterns": len(frame),
        "intents": len(responses),
        "threshold": THRESHOLD,
        "fold_accuracy": fold_accuracy,
        "fold_macro_f1": fold_macro_f1,
        "mean_accuracy": float(np.mean(fold_accuracy)),
        "mean_macro_f1": float(np.mean(fold_macro_f1)),
        "answer_coverage": coverage,
        "accepted_intent_accuracy": accepted_accuracy,
        "out_of_scope_false_answer_rate": oos_false_answer_rate,
        "python_version": platform.python_version(),
        "sklearn_version": sklearn.__version__,
        "numpy_version": np.__version__,
        "joblib_version": joblib.__version__,
    }

    (BASE / "training_metrics.json").write_text(
        json.dumps(metrics, indent=2) + "\n",
        encoding="utf-8",
    )

    # Train the deliverable only after evaluation.
    model.fit(texts, targets)

    joblib.dump(
        model,
        BASE / "intent_model.joblib",
    )

    (BASE / "responses.json").write_text(
        json.dumps(
            responses,
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )

    print("\nSaved:")
    print("  intent_model.joblib")
    print("  responses.json")
    print("  confusion_matrix.png")
    print("  cv_predictions.csv")
    print("  cv_errors.csv")
    print("  training_metrics.json")

    print(
        "\nThese are development results, not a final "
        "real-user accuracy estimate."
    )


if __name__ == "__main__":
    main()