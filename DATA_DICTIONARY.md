# Data dictionary

All CSVs use UTF-8, comma separators, and a header row. Numeric strings retain their source precision. Scores and rates are fractions on a 0--1 scale, not percentages.

## Shared fields

| Field | Meaning |
| --- | --- |
| `method` | Method or variant label used in the manuscript |
| `seed` | Scenario random seed: 42, 43, or 44 |
| `attack_mode` | Controlled attack mode; `low_noise` corresponds to low-noise in the text |
| `mask_rate` | Scenario missing-observation fraction: 0.1, 0.2, 0.3, 0.4, or 0.5 |
| `malicious_ratio` | Designated malicious-worker ratio, 0.1 |
| `mae` / `MAE` | Mean absolute numerical error, in PM2.5 concentration units (micrograms per cubic meter) |
| `rmse` / `RMSE` | Root mean squared numerical error, in the same units |
| `malicious_precision` | Worker-level malicious-user precision in one scenario |
| `malicious_recall` | Worker-level malicious-user recall in one scenario |
| `malicious_f1` | Worker-level malicious-user F1 in one scenario; already averaged in the Beijing summary |

The key for a scenario-result row is `(method, seed, attack_mode, mask_rate)`. Capitalization of MAE/RMSE in the Beijing summary is retained from its source.

## Visible-only overcorrection fields

| Field | Meaning |
| --- | --- |
| `scenario_id` | Readable scenario identifier, e.g. `seed42_bias_mask0.1` |
| `visible_numerator` | Visible rows whose enhanced absolute error exceeds the original absolute error |
| `visible_denominator` | Number of visible submissions used in the rate |
| `visible_overcorr` | `visible_numerator / visible_denominator` |
| `total_rows` | Number of rows in the full-output evaluation universe |
| `masked_rows` | Rows without an original visible submission |
| `visible_rows` | Visible rows; equal to `visible_denominator` and to `total_rows - masked_rows` |

These counts support the visible-only comparison; masked rows are excluded from both the overcorrection numerator and denominator.

## Ablation labels

| Label | Removed component |
| --- | --- |
| DTC-O | Full method |
| DTC-O-NE | Event guard |
| DTC-O-NI | Implication propagation |
| DTC-O-NC | Quality-aware correction |
