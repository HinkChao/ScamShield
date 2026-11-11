
# ScamShield AI - Dataset Protocol

## 1. Purpose

This document defines the dataset standards and evaluation
protocol used by ScamShield AI.

The purpose is to ensure that model evaluation is
reproducible, fair, and based on reliable evidence.

## 2. Classification Labels

The dataset uses three primary labels.

| Label | Definition |
|---|---|
| phishing | Messages that attempt to deceive users into revealing credentials or sensitive information. |
| spam | Unsolicited promotional or bulk messages without clear phishing intent. |
| legitimate | Normal messages without identified phishing or spam characteristics. |

### Ambiguous Cases

Messages that cannot be reliably classified should be
marked for manual review.

They should not be forced into one of the three primary
classes for the main evaluation.

## 3. Dataset Provenance

Every dataset must record:

- Dataset name
- Original source
- Source URL
- License and usage permissions
- Collection date
- Language
- Number of samples
- Known limitations

Data without clear provenance or usage permissions
must not be treated as approved evaluation data.

## 4. Data Schema

Each processed record should contain:

| Field | Description |
|---|---|
| id | Unique sample identifier |
| text | Message content after approved anonymization |
| label | phishing, spam, or legitimate |
| language | Message language |
| source | Dataset source |
| license | Applicable license |
| group_id | Duplicate or template group identifier |
| split | train, validation, or test |
| is_synthetic | Whether the sample is synthetic |
| review_status | pending, reviewed, or ambiguous |

## 5. Privacy and Anonymization

- Remove personal identifiers where possible.
- Do not include real passwords, authentication tokens,
  or private account information.
- Avoid collecting unnecessary personal information.
- Keep sensitive examples out of public demonstrations.
- Follow the original dataset's license and usage restrictions.

## 6. Data Partitioning

The dataset will be divided into:

- Training set: used to train the model.
- Validation set: used for model selection and threshold tuning.
- Test set: reserved for final evaluation.

A provisional split is:

- 70% Training
- 15% Validation
- 15% Testing

The final split must account for dataset size,
class balance, language distribution, and duplicate groups.

Samples with identical or highly similar templates
must not leak across different partitions.

The test set must not be reused for threshold tuning.

## 7. Language Slices

Evaluation should report results separately
for each available language.

At minimum, record:

- English
- Traditional Chinese

Language-specific metrics must include sample counts.

If a language has insufficient data, report that
the evaluation is unavailable or limited.

## 8. Synthetic Data Policy

Synthetic samples must be explicitly identified.

Synthetic data may be used for development and
functional testing.

Synthetic data must not be presented as independent
real-world evaluation evidence.

## 9. Evaluation Metrics

The evaluation will report:

- Precision
- Recall
- F1-score
- Confusion Matrix
- Sample counts
- Label distribution
- False positives
- False negatives

## 10. Error Analysis

Representative cases should include:

- False positives
- False negatives
- Ambiguous messages
- Difficult multilingual examples

Each case should include an explanation of
why the prediction may have failed.

## 11. Reproducibility

Evaluation runs should record:

- Dataset version
- Model version
- Evaluation date
- Random seed
- Dataset partition
- Evaluation configuration

If evaluation data or a model is unavailable,
the evaluation script must report this explicitly.

## 12. Limitations

Evaluation results only describe performance
on the available dataset.

They do not guarantee that a message is safe
or fraudulent in every real-world situation.