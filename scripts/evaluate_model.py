
import argparse
from pathlib import Path

import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)

# ----------------------------------
# Configuration
# ----------------------------------

LABELS = ["phishing", "spam", "legitimate"]

REQUIRED_COLUMNS = [
    "id",
    "y_true",
    "y_pred",
    "language",
]

DEFAULT_DATASET = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "processed"
    / "evaluation_results.csv"
)


# ----------------------------------
# Load Dataset
# ----------------------------------

def load_dataset(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"DATA_UNAVAILABLE: Dataset not found: {path}"
        )

    df = pd.read_csv(path)

    if df.empty:
        raise ValueError(
            "DATA_UNAVAILABLE: Dataset contains no samples."
        )

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"DATA_INVALID: Missing columns: {missing_columns}"
        )

    return df


# ----------------------------------
# Validate Dataset
# ----------------------------------

def validate_dataset(df: pd.DataFrame) -> None:
    if df[REQUIRED_COLUMNS].isnull().any().any():
        raise ValueError(
            "DATA_INVALID: Required fields contain missing values."
        )

    invalid_true = set(df["y_true"]) - set(LABELS)
    invalid_pred = set(df["y_pred"]) - set(LABELS)

    if invalid_true or invalid_pred:
        raise ValueError(
            "DATA_INVALID: Unknown labels found. "
            f"y_true={invalid_true}, y_pred={invalid_pred}"
        )

    if df["id"].duplicated().any():
        raise ValueError(
            "DATA_INVALID: Duplicate sample IDs found."
        )


# ----------------------------------
# Evaluate Predictions
# ----------------------------------

def evaluate_predictions(df: pd.DataFrame) -> dict:
    y_true = df["y_true"]
    y_pred = df["y_pred"]

    report = classification_report(
        y_true,
        y_pred,
        labels=LABELS,
        output_dict=True,
        zero_division=0,
    )

    matrix = confusion_matrix(
        y_true,
        y_pred,
        labels=LABELS,
    )

    return {
        "sample_count": len(df),
        "accuracy": accuracy_score(y_true, y_pred),
        "classification_report": report,
        "confusion_matrix": matrix.tolist(),
        "labels": LABELS,
    }


# ----------------------------------
# Language-specific Evaluation
# ----------------------------------

def evaluate_by_language(df: pd.DataFrame) -> dict:
    results = {}

    for language in sorted(df["language"].unique()):
        language_df = df[df["language"] == language]

        results[language] = evaluate_predictions(language_df)

    return results


# ----------------------------------
# Main
# ----------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Evaluate ScamShield AI predictions."
    )

    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_DATASET,
        help="Path to evaluation CSV file.",
    )

    args = parser.parse_args()

    try:
        df = load_dataset(args.input)
        validate_dataset(df)

        overall = evaluate_predictions(df)
        language_results = evaluate_by_language(df)

        print("\n=== ScamShield AI Evaluation ===")
        print(f"Samples: {overall['sample_count']}")
        print(f"Accuracy: {overall['accuracy']:.4f}")

        print("\n=== Overall Classification Report ===")
        print(
            classification_report(
                df["y_true"],
                df["y_pred"],
                labels=LABELS,
                zero_division=0,
            )
        )

        print("\n=== Confusion Matrix ===")
        print("Label order:", LABELS)
        print(overall["confusion_matrix"])

        print("\n=== Language-specific Results ===")

        for language, result in language_results.items():
            print(f"\nLanguage: {language}")
            print(f"Samples: {result['sample_count']}")

            print(
                classification_report(
                    df[df["language"] == language]["y_true"],
                    df[df["language"] == language]["y_pred"],
                    labels=LABELS,
                    zero_division=0,
                )
            )

    except (FileNotFoundError, ValueError) as error:
        print(f"\n{error}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
