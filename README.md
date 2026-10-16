# DTC-O paper:result data

This repository accompanies **DTC-O: Dynamic Trust Calibration for Full-Output Sensor Data Enhancement in Mobile Crowdsensing**.


## Included files

| File | Rows | Connection to the manuscript |
| --- | ---: | --- |
| `data/standard_numerical_results.csv` | 525 | MAE and RMSE for the seven methods in Table II; 75 scenarios per method |
| `data/standard_detection_results.csv` | 450 | Precision, recall, and F1 for the six defined detectors in Table II; 75 scenarios per method |
| `data/ablation_results.csv` | 300 | F1, MAE, and RMSE for DTC-O and three ablations in Table VII; 75 scenarios per variant |
| `data/visible_overcorrection.csv` | 150 | Visible-only overcorrection for DTC-O and PRBTD-O; 75 scenarios per method, with counts |
| `data/beijing_four_site_summary.csv` | 2 | Existing F1, MAE, and RMSE aggregates for the two methods in Table V |

The standard grid crosses five attack modes (`gaussian`, `bias`, `low_noise`, `burst`, `collusion`), five mask rates (0.1--0.5), and three seeds (42, 43, 44). The malicious-worker ratio is 0.1. Each row in the standard files is a scenario-level aggregate, not an individual sensor reading. The ablation file includes the unchanged DTC-O rows again to make the Table VII comparison self-contained.


## Validate this deposit

Use Python 3.8 or later; only the Python standard library is required:

```sh
python validate_data.py
```

The check verifies file hashes, row counts, scenario keys, visible-only denominators, the released rounded table values, and the unrounded ablation difference. It runs in seconds on an ordinary computer and does not execute any model or experiment.

See [DATA_DICTIONARY.md](DATA_DICTIONARY.md) for fields and [PROVENANCE.json](PROVENANCE.json) for original source-file hashes and exact export selections. `MANIFEST.sha256` records the SHA-256 of every release file except the manifest itself.

## Attribution and reuse

Please cite the associated DTC-O manuscript when using these result data. Bibliographic details will be updated when a publication record is available. This deposit assigns no new reuse license; contact the repository owner for reuse permission. Original third-party sensor records are not redistributed here.
