# Experiment Evidence Index

## VAL_TESTS

### Command

```powershell
python -m pytest -q
```

### Configuration

Repository test suite under the validated Windows .venv.

### Runtime

Approximately 4.31 seconds during final validation.

### Metrics

- Tests passed: 4
- Tests failed: 0

Raw log:

- logs/00_pytest.log

### Interpretation

The repository test suite passed before the claim experiments were executed.

## VAL_QUICKSTART

### Command

```powershell
python examples\quickstart.py
```

### Configuration

Repository-provided minimal XGBoost example.

### Runtime

3.8059948 seconds wall-clock time.

### Metrics

- Accuracy: 0.9021
- Fidelity: 1.0000
- In-region coverage: 0.8042
- In-region fidelity: 1.0000
- Pruning rate: 0.1000
- Active estimators: 9/10
- Tau: 6.655973
- Oracle calls: 3

### Raw log

- logs/01_quickstart.log

### Interpretation

The official end-to-end example reproduced successfully and validated the
installation, solver, training, calibration, pruning, and evaluation pipeline.

## C2_A005

### Command

- configs/C2_A005.txt and scripts/run_claim2_alpha_sweep.ps1.

### Configuration

- Alpha 0.05; all other controlled parameters fixed.

### Runtime

Internal runtime: 1.1836 seconds.

### Metrics

- Target coverage: 0.95
- Empirical coverage: 0.9301
- In-region fidelity: 1.0000
- Pruning rate: 0.0000
- Active estimators: 10/10

### Raw log

- logs/C2_A005.log

### Interpretation

The largest protected region in the sweep resulted in no pruning.

## C2_A010

### Command

- configs/C2_A010.txt and scripts/run_claim2_alpha_sweep.ps1.

### Configuration

- Alpha 0.10; all other controlled parameters fixed.

### Runtime

Internal runtime: 0.6755 seconds.

### Metrics

- Target coverage: 0.90
- Empirical coverage: 0.8741
- In-region fidelity: 1.0000
- Pruning rate: 0.1000
- Active estimators: 9/10

### Raw log

- logs/C2_A010.log

### Interpretation

Reducing the target coverage permitted one estimator to be removed.

## C2_A020

### Command

- configs/C2_A020.txt and scripts/run_claim2_alpha_sweep.ps1.

### Configuration

- Alpha 0.20; all other controlled parameters fixed.

### Runtime

Internal runtime: 0.6752 seconds.

### Metrics

- Target coverage: 0.80
- Empirical coverage: 0.8042
- In-region fidelity: 1.0000
- Pruning rate: 0.1000
- Active estimators: 9/10

### Raw log

- logs/C2_A020.log

### Interpretation

This run produced the closest empirical match to its nominal coverage target.

## C2_A040

### Command

- configs/C2_A040.txt and scripts/run_claim2_alpha_sweep.ps1.

### Configuration

- Alpha 0.40; all other controlled parameters fixed.

### Runtime

Internal runtime: 0.4265 seconds.

### Metrics

- Target coverage: 0.60
- Empirical coverage: 0.5455
- Overall fidelity: 0.9930
- In-region fidelity: 1.0000
- Pruning rate: 0.2000
- Active estimators: 8/10

### Raw log

- logs/C2_A040.log

### Interpretation

The smaller protected region allowed more pruning. A small overall prediction
difference appeared outside the region, while in-region fidelity remained
perfect.

## C2_A080

### Command

- configs/C2_A080.txt and scripts/run_claim2_alpha_sweep.ps1.

### Configuration

Alpha 0.80; all other controlled parameters fixed.

### Runtime

Internal runtime: 0.4076 seconds.

### Metrics

- Target coverage: 0.20
- Empirical coverage: 0.2168
- Overall fidelity: 0.9930
- In-region fidelity: 1.0000
- Pruning rate: 0.2000
- Active estimators: 8/10

### Raw log

- logs/C2_A080.log

### Interpretation

The smallest protected region preserved perfect in-region fidelity while
overall fidelity remained slightly below one.