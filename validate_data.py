"""Validate the selected result-data release without running experiments."""
import csv
import hashlib
import itertools
import json
import math
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parent

def read(name):
    with (ROOT / 'data' / name).open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))

def average(rows, method, field):
    return mean(float(r[field]) for r in rows if r['method'] == method)

def check_grid(rows, methods):
    expected = set(itertools.product(methods, ['42', '43', '44'],
                   ['gaussian', 'bias', 'low_noise', 'burst', 'collusion'],
                   ['0.1', '0.2', '0.3', '0.4', '0.5']))
    actual = [(r['method'], r['seed'], r['attack_mode'], r['mask_rate']) for r in rows]
    assert len(actual) == len(set(actual))
    assert set(actual) == expected

def main():
    manifest = (ROOT / 'MANIFEST.sha256').read_text(encoding='utf-8').splitlines()
    for line in manifest:
        digest, name = line.split('  ', 1)
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, name
    provenance = json.loads((ROOT / 'PROVENANCE.json').read_text(encoding='utf-8'))
    for export in provenance['exports']:
        with (ROOT / export['file']).open(encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            assert reader.fieldnames == export['columns']
        assert len(rows) == export['rows']

    numerical = read('standard_numerical_results.csv')
    detection = read('standard_detection_results.csv')
    ablation = read('ablation_results.csv')
    visible = read('visible_overcorrection.csv')
    beijing = read('beijing_four_site_summary.csv')
    methods = ['RAW', 'WEI', 'TD', 'ST', 'PRBTD-O', 'DTC', 'DTC-O']
    check_grid(numerical, methods)
    check_grid(detection, methods[1:])
    check_grid(ablation, ['DTC-O', 'DTC-O-NE', 'DTC-O-NI', 'DTC-O-NC'])
    check_grid(visible, ['PRBTD-O', 'DTC-O'])
    assert all(r['malicious_ratio'] == '0.1' for r in numerical + detection + ablation)
    for rows, fields in [(numerical, ['mae', 'rmse']),
                         (detection, ['malicious_precision', 'malicious_recall', 'malicious_f1']),
                         (ablation, ['malicious_f1', 'mae', 'rmse'])]:
        assert all(math.isfinite(float(r[f])) for r in rows for f in fields)
    assert all(0 <= float(r[f]) <= 1 for r in detection
               for f in ['malicious_precision', 'malicious_recall', 'malicious_f1'])
    for r in visible:
        n, d = int(r['visible_numerator']), int(r['visible_denominator'])
        assert 0 <= n <= d
        assert d == int(r['visible_rows']) == int(r['total_rows']) - int(r['masked_rows'])
        assert math.isclose(float(r['visible_overcorr']), n / d, abs_tol=1e-14)
    expected_num = {'RAW': (7.861, 11.410), 'WEI': (6.397, 10.658),
                    'TD': (7.861, 11.410), 'ST': (7.632, 11.089),
                    'PRBTD-O': (7.256, 10.169), 'DTC': (6.311, 10.231),
                    'DTC-O': (7.122, 10.240)}
    expected_detection = {'WEI': (0.068, 0.069, 0.068), 'TD': (0.100, 0.174, 0.127),
                          'ST': (0.133, 0.146, 0.139), 'PRBTD-O': (0.757, 0.354, 0.404),
                          'DTC': (0.223, 0.509, 0.307), 'DTC-O': (0.427, 0.881, 0.565)}
    for method, values in expected_num.items():
        assert tuple(round(average(numerical, method, f), 3) for f in ['mae', 'rmse']) == values
    for method, values in expected_detection.items():
        assert tuple(round(average(detection, method, f), 3)
                     for f in ['malicious_precision', 'malicious_recall', 'malicious_f1']) == values
    expected_ablation = {'DTC-O': (0.5654, 7.1221, 10.2399),
                         'DTC-O-NE': (0.5637, 7.1226, 10.2407),
                         'DTC-O-NI': (0.4993, 7.1206, 10.2486),
                         'DTC-O-NC': (0.5654, 7.2892, 10.3336)}
    for method, values in expected_ablation.items():
        assert tuple(round(average(ablation, method, f), 4)
                     for f in ['malicious_f1', 'mae', 'rmse']) == values
    expected_beijing = {'DTC-O': (0.693, 4.287, 6.587), 'PRBTD-O': (0.679, 4.106, 6.693)}
    assert len(beijing) == 2
    for r in beijing:
        assert tuple(round(float(r[f]), 3) for f in ['malicious_f1', 'MAE', 'RMSE']) == expected_beijing[r['method']]
    assert round(average(visible, 'DTC-O', 'visible_overcorr'), 3) == 0.404
    assert round(average(visible, 'PRBTD-O', 'visible_overcorr'), 3) == 0.466
    overcorr_difference = 100 * (average(visible, 'DTC-O', 'visible_overcorr') -
                               average(visible, 'PRBTD-O', 'visible_overcorr'))
    f1_loss = 100 * (average(ablation, 'DTC-O', 'malicious_f1') -
                    average(ablation, 'DTC-O-NI', 'malicious_f1'))
    assert round(overcorr_difference, 2) == -6.17
    assert round(f1_loss, 2) == 6.62
    print('PASS: checksums, schemas, row counts, scenario grids, denominators, and released table values.')
    print('DTC-O minus PRBTD-O visible-only overcorrection: {:.12f} percentage points'.format(overcorr_difference))
    print('DTC-O to DTC-O-NI F1 loss: {:.12f} percentage points'.format(f1_loss))

if __name__ == '__main__':
    main()
