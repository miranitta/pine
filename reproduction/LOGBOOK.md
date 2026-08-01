# PINE Reproduction Logbook

## 1. Objective

Reproduce selected central claims from PINE, ICML 2026.

## 2. Environment

- Repository: D:\Desktop\Research\ICML2026\pine
- Python: 3.11.9
- Gurobi: 12.0.3
- Test suite: 4 passed
- Repository commit: see `git_commit.txt`

## 3. Repository validation

### Tests

- Command: `python -m pytest -q`
- Status: passed
- Evidence: `logs/00_pytest.log`

### Quick-start result

- Command: `python examples\quickstart.py`
- Runtime: 3.806 seconds
- Accuracy: 0.9021
- Overall fidelity: 1.0000
- In-region coverage: 0.8042
- In-region fidelity: 1.0000
- Pruning rate: 0.1000
- Active estimators: 9/10
- Tau: 6.655973
- Oracle calls: 3

Interpretation:
The reproduced coverage of 0.8042 is close to the nominal target coverage
of 0.80 for alpha = 0.20. No prediction disagreements were observed inside
the calibrated region in this run.

## 4. Claim 1 ï¿½ Better pruning than FIPE

Paper evidence:
- Table 1
- Figure 3

Status: pending.

## Claim 2 â€” Alpha controls coverage

### Experimental setup

- Dataset: breast_cancer
- Model: XGBoost
- Seed: 0
- Number of estimators: 10
- Maximum depth: 2
- Learning rate: 0.1
- Alpha values: 0.05, 0.10, 0.20, 0.40, 0.80
- Chow-Liu bins: 4
- Beta: 1.0
- Test size: 0.25
- Calibration size: 0.25

### Results

Empirical in-region coverage decreased monotonically as alpha increased:

- alpha 0.05: 0.9301
- alpha 0.10: 0.8741
- alpha 0.20: 0.8042
- alpha 0.40: 0.5455
- alpha 0.80: 0.2168

The observed coverage values followed the nominal target trend `1 - alpha`.
The closest numerical match occurred at alpha 0.20, where the target was
0.8000 and the observed coverage was 0.8042.

### Verdict

Reproduced qualitatively and approximately quantitatively on one dataset,
one model, and one fixed seed.

## Claim 3 â€” Prediction equivalence in the ID region

Across all five alpha values, in-region fidelity was 1.0000.

Overall fidelity fell slightly to 0.9930 for alpha 0.40 and alpha 0.80,
while in-region fidelity remained 1.0000. This is consistent with PINE's
objective of preserving predictions inside the calibrated region rather
than necessarily over the entire input space.

### Verdict

Empirically reproduced on the tested configuration.

## 7. Optional scalability

Paper evidence:
- Tables 2ï¿½3

Status: limited reproduction only.

## 8. Observations

Pending.

## 9. Deviations

- Reduced experiment grid because of the deadline.
- Full scalability grid not attempted.
- Laptop CPU used for Gurobi optimization.

## 10. Conclusion

Pending.

## Claim 2 — Alpha controls coverage

### Experimental setup

- Dataset: breast_cancer
- Model: XGBoost
- Seed: 0
- Estimators: 10
- Maximum depth: 2
- Learning rate: 0.1
- Alpha values: 0.05, 0.10, 0.20, 0.40, 0.80
- Chow-Liu bins: 4
- Beta: 1.0
- Test size: 0.25
- Calibration size: 0.25

### Results

Empirical coverage decreased monotonically as alpha increased:

| Alpha | Target coverage | Empirical coverage |
|---:|---:|---:|
| 0.05 | 0.95 | 0.9301 |
| 0.10 | 0.90 | 0.8741 |
| 0.20 | 0.80 | 0.8042 |
| 0.40 | 0.60 | 0.5455 |
| 0.80 | 0.20 | 0.2168 |

The observed trend follows the nominal target relation `1 - alpha`.

### Verdict

Reproduced qualitatively and approximately quantitatively on one dataset,
one model, and one fixed seed.

## Claim 3 — Prediction equivalence in the ID region

Across all tested alpha values, in-region fidelity was 1.0000.

For alpha 0.40 and 0.80, overall fidelity decreased slightly to 0.9930,
while in-region fidelity remained 1.0000. This is consistent with PINE's
objective of preserving predictions inside the calibrated region rather
than necessarily over the entire input space.

### Verdict

Empirically reproduced on the tested configuration.
