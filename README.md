# DTC-O paper: selected experimental result data

This repository accompanies **DTC-O: Dynamic Trust Calibration for Full-Output Sensor Data Enhancement in Mobile Crowdsensing**.

This initial release contains selected existing result data from the manuscript, rather than the original sensor observations or a complete experiment-reproduction package. The data were exported on 2026-10-15 by selecting rows and columns from the archived result files. No experiments were rerun, no parameters were selected, and no result values were changed for this release.

## Included files

| File | Rows | Connection to the manuscript |
| --- | ---: | --- |
| `data/standard_numerical_results.csv` | 525 | MAE and RMSE for the seven methods in Table II; 75 scenarios per method |
| `data/standard_detection_results.csv` | 450 | Precision, recall, and F1 for the six defined detectors in Table II; 75 scenarios per method |
| `data/ablation_results.csv` | 300 | F1, MAE, and RMSE for DTC-O and three ablations in Table VII; 75 scenarios per variant |
| `data/visible_overcorrection.csv` | 150 | Visible-only overcorrection for DTC-O and PRBTD-O; 75 scenarios per method, with counts |
| `data/beijing_four_site_summary.csv` | 2 | Existing F1, MAE, and RMSE aggregates for the two methods in Table V |

The standard grid crosses five attack modes (`gaussian`, `bias`, `low_noise`, `burst`, `collusion`), five mask rates (0.1--0.5), and three seeds (42, 43, 44). The malicious-worker ratio is 0.1. Each row in the standard files is a scenario-level aggregate, not an individual sensor reading. The ablation file includes the unchanged DTC-O rows again to make the Table VII comparison self-contained.

## Reading the results

- Compute an unweighted mean over the 75 scenario rows for each method to obtain the standard and ablation table metrics. F1 is the mean of scenario F1 scores, not F1 recomputed from the mean precision and recall.
- RAW does not define a malicious-user detector. It appears only in the numerical file; source diagnostic detector values for RAW are not released as paper detection results.
- MAE and RMSE use the full-output evaluation universe. The overcorrection file uses **visible submissions only**: `visible_overcorr = visible_numerator / visible_denominator`. Average the scenario rates, rather than pooling their counts, to recover the reported comparison. Legacy all-row overcorrection columns from the source files are excluded.
- The released visible-only counts cover DTC-O and PRBTD-O. Overcorrection and output-coverage values for the other methods are not included in this subset.
- The Table VII F1 loss for DTC-O-NI is **6.617063869... percentage points**, which rounds to **6.62**. The four-decimal values printed in the manuscript do not preserve this difference exactly.
- The Beijing file contains already-aggregated results for Aotizhongxin, Changping, Dingling, and Dongsi. It does not contain external per-scenario observations or overcorrection denominators.

The 75 controlled scenarios reuse reference series; these rows are not 75 independent field deployments. This deposit does not include stress-test data, original third-party PM2.5 observations, row-level predictions, training/validation records, or implementation code.

## Validate this deposit

Use Python 3.8 or later; only the Python standard library is required:

```sh
python validate_data.py
```

The check verifies file hashes, row counts, scenario keys, visible-only denominators, the released rounded table values, and the unrounded ablation difference. It runs in seconds on an ordinary computer and does not execute any model or experiment.

See [DATA_DICTIONARY.md](DATA_DICTIONARY.md) for fields and [PROVENANCE.json](PROVENANCE.json) for original source-file hashes and exact export selections. `MANIFEST.sha256` records the SHA-256 of every release file except the manifest itself.

## Attribution and reuse

Please cite the associated DTC-O manuscript when using these result data. Bibliographic details will be updated when a publication record is available. This deposit assigns no new reuse license; contact the repository owner for reuse permission. Original third-party sensor records are not redistributed here.
