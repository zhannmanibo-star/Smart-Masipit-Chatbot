import json
import joblib
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_predict, cross_val_score, StratifiedKFold
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay

SKIP_TAGS = {"autocorrect_typo_handling"}   # hindi ito intent

# 1. Basahin ang JSON at gawing table
with open("intents.json", encoding="utf-8") as f:
    data = json.load(f)

rows, responses = [], {}
for intent in data["intents"]:
    tag = intent["tag"]
    if tag in SKIP_TAGS:
        continue
    responses[tag] = intent["responses"]
    for pattern in intent["patterns"]:
        rows.append((pattern.lower().strip(), tag))

df = pd.DataFrame(rows, columns=["text", "label"])
print(f"Kabuuang patterns: {len(df)} | Intents: {df['label'].nunique()}")
print(df["label"].value_counts().to_string(), "\n")

# 2. Model
model = make_pipeline(
    TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4)),
    LogisticRegression(C=10, max_iter=2000),
)

# 3. Evaluation gamit ang cross-validation (mas patas kapag maliit ang data)
cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
scores = cross_val_score(model, df["text"], df["label"], cv=cv)
print(f"CV accuracy: {scores.mean():.2f} +/- {scores.std():.2f}\n")

y_pred = cross_val_predict(model, df["text"], df["label"], cv=cv)
print(classification_report(df["label"], y_pred, zero_division=0))

labels = sorted(df["label"].unique())
cm = confusion_matrix(df["label"], y_pred, labels=labels)
fig, ax = plt.subplots(figsize=(14, 12))
ConfusionMatrixDisplay(cm, display_labels=labels).plot(ax=ax, xticks_rotation=90, colorbar=False)
plt.tight_layout()
plt.savefig("confusion_matrix.png", dpi=120)

# 4. I-train sa BUONG data para sa final model
model.fit(df["text"], df["label"])
joblib.dump(model, "intent_model.joblib")
with open("responses.json", "w", encoding="utf-8") as f:
    json.dump(responses, f, ensure_ascii=False, indent=2)

print("\nSaved: intent_model.joblib, responses.json, confusion_matrix.png")