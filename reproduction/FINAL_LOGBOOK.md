# PINE Reproduction Logbook

## Submission category

Special Prize #1: rigorous, fully verified reproduction requiring human intervention.

## 1. Objective

The objective of this study is to reproduce selected central claims from
PINE: Pruning Boosted Tree Ensembles with Conformal In-Distribution Prediction
Equivalence.

Because the challenge deadline limited the available execution time, the
study prioritizes depth and verification over reproducing the complete
experimental grid.

The primary reproduced claims are:

1. Alpha controls the coverage of the conformal in-distribution region.
2. The pruned ensemble preserves the original ensemble's predictions inside
   that calibrated region.

A smaller amount of exploratory evidence was also collected regarding pruning
and scalability. A complete PINE-versus-FIPE comparison was not claimed.

---

## 2. Paper overview

PINE prunes boosted-tree ensembles while protecting prediction equivalence
inside a calibrated in-distribution region.

The method combines:

- a tree-ensemble model,
- a Chow-Liu density or conformity model,
- split conformal calibration,
- a threshold tau defining the protected region,
- and a Gurobi-based pruning optimization procedure.

The central trade-off is:

- a smaller protected region can permit more aggressive pruning;
- predictions must remain equivalent inside the protected region;
- prediction equivalence outside the region is not necessarily required.

The paper claims examined in this logbook are:

| Claim | Paper evidence | Reproduction status |
|---|---|---|
| Better pruning than FIPE | Table 1 and Figure 3 | Partial exploratory evidence only |
| Alpha controls coverage | Figure 4 | Reproduced on one controlled setting |
| Prediction equivalence in the ID region | Figure 5 | Empirically reproduced |
| Scalability | Tables 2 and 3 | Limited diagnostic runs only |

---

## 3. Environment

### Hardware and operating environment

- Host operating system: Windows
- Working repository: `D:\Desktop\Research\ICML2026\pine`
- Experiment environment: Windows PowerShell
- Python environment: repository-local `.venv`
- GPU: NVIDIA RTX 3050
- Important note: the PINE optimization workload used Gurobi and was primarily
  CPU-oriented; the GPU was not the principal computational resource.

### Software

- Python: 3.11.9
- Gurobi: 12.0.3
- Repository branch: `main`
- Origin: user fork
- Upstream: official PINE repository

Complete package versions are stored in:

- `pip_freeze.txt`
- `environment.txt`

The exact repository commit is stored in:

- `git_commit.txt`

---

## 4. Repository validation

### Test suite

Command:

```powershell
python -m pytest -q
```

Result:

4 passed

Evidence:

- logs/00_pytest.log

### Official quick-start:

Command:

```powershell
python examples\quickstart.py
```
Measured wall-clock runtime:

- 3.8059948 seconds

Results:

| Metric             |    Value |
| ------------------ | -------: |
| Accuracy           |   0.9021 |
| Overall fidelity   |   1.0000 |
| In-region coverage |   0.8042 |
| In-region fidelity |   1.0000 |
| Pruning rate       |   0.1000 |
| Active estimators  |     9/10 |
| Tau                | 6.655973 |
| Oracle calls       |        3 |

Evidence:

- logs/01_quickstart.log
- logs/01_quickstart_runtime.txt
- results/01_quickstart.json
- tables/quickstart_baseline.csv

---

## 5. Human intervention timeline

The reproduction could not be completed by an automated agent without human
intervention.

### Intervention 1: Separating OpenResearch from the working environment

Human intervention therefore prevented an unnecessary and risky environment
migration.

### Intervention 2: Preventing duplicate experiment rows

The official CLI appends results to an existing CSV. The alpha 0.20 experiment
was initially executed twice against the same output file, producing duplicate
rows.

The duplicate was identified by manually inspecting the CSV. The file was
deleted and the experiment was rerun once using a fully explicit configuration.

The controlled sweep therefore uses one distinct result file per experiment.

### Intervention 3: Correcting the initial automation script

The first PowerShell sweep script omitted the explicit --output argument in
the executed command. Results were therefore written to the CLI's default
location rather than the intended experiment-specific files.

Manual inspection exposed the discrepancy. The script was corrected to:

- use a unique output file per alpha,
- delete stale outputs before execution,
- save an explicit configuration,
- save a runtime record,
- verify that exactly one output row was generated.

### Intervention 4: Correcting result enrichment

An initial PowerShell transformation added the target_coverage field without
providing its value. This caused blank derived columns.

The transformation was replaced with explicit typed PSCustomObject records.
The final table was manually checked against every raw CSV.

### Intervention 5: Scientific interpretation

The agent output alone could report metrics, but it did not establish the
scientific meaning of the results.

Human analysis distinguished:

- in-region fidelity from overall fidelity,
- empirical support from theorem proof,
- controlled experiments from legacy exploratory runs,
- PINE-only pruning evidence from a valid PINE-versus-FIPE comparison.

This prevented unsupported claims from being marked as reproduced.

## 6. Claim 2: Alpha controls coverage

### Objective

Test whether changing alpha changes the empirical coverage of the calibrated
in-distribution region in the expected direction.

The nominal target coverage is:

1 - alpha

### Controlled configuration

| Parameter            | Value                        |
| -------------------- | ---------------------------- |
| Dataset              | breast_cancer                |
| Model                | XGBoost                      |
| Seed                 | 0                            |
| Number of estimators | 10                           |
| Maximum depth        | 2                            |
| Learning rate        | 0.1                          |
| Chow-Liu bins        | 4                            |
| Beta                 | 1.0                          |
| Norm                 | 1                            |
| Maximum oracle calls | 100                          |
| Test size            | 0.25                         |
| Calibration size     | 0.25                         |
| Alpha values         | 0.05, 0.10, 0.20, 0.40, 0.80 |


### Command template

```powershell
python scripts\run_pine_chowliu.py `
    --dataset breast_cancer `
    --model xgb `
    --n-estimators 10 `
    --max-depth 2 `
    --learning-rate 0.1 `
    --seed 0 `
    --alpha <ALPHA> `
    --n-bins 4 `
    --beta 1.0 `
    --norm 1 `
    --max-oracle-calls 100 `
    --test-size 0.25 `
    --calibration-size 0.25 `
    --gurobi-output 0 `
    --output reproduction\results\<EXPERIMENT_ID>.csv
```

### Results

| Alpha | Target coverage | Empirical coverage | Difference |    Tau |
| ----: | --------------: | -----------------: | ---------: | -----: |
|  0.05 |            0.95 |             0.9301 |    -0.0199 | 9.5284 |
|  0.10 |            0.90 |             0.8741 |    -0.0259 | 7.7046 |
|  0.20 |            0.80 |             0.8042 |    +0.0042 | 6.6560 |
|  0.40 |            0.60 |             0.5455 |    -0.0545 | 3.9109 |
|  0.80 |            0.20 |             0.2168 |    +0.0168 | 2.5006 |

Empirical coverage decreased monotonically:

0.9301 -> 0.8741 -> 0.8042 -> 0.5455 -> 0.2168

The closest numerical match occurred at alpha 0.20:

- Target coverage:    0.8000
- Empirical coverage: 0.8042
- Difference:        +0.0042

### Runtime

| Alpha | Internal runtime in seconds |
| ----: | --------------------------: |
|  0.05 |                      1.1836 |
|  0.10 |                      0.6755 |
|  0.20 |                      0.6752 |
|  0.40 |                      0.4265 |
|  0.80 |                      0.4076 |

### Evidence

Configurations:

- configs/C2_A005.txt
- configs/C2_A010.txt
- configs/C2_A020.txt
- configs/C2_A040.txt
- configs/C2_A080.txt

Raw results:

- results/C2_A005.csv
- results/C2_A010.csv
- results/C2_A020.csv
- results/C2_A040.csv
- results/C2_A080.csv

Raw console logs:

- logs/C2_A005.log
- logs/C2_A010.log
- logs/C2_A020.log
- logs/C2_A040.log
- logs/C2_A080.log

Final table:

- tables/claim2_alpha_sweep_final.csv

### Interpretation

The experiment reproduces the expected relationship between alpha and region
coverage. Higher alpha values produce smaller protected regions.

The result is a controlled single-dataset, single-model, single-seed
reproduction. It supports the trend and approximate calibration behavior but
does not reproduce the complete paper grid.

### Verdict

Reproduced qualitatively and approximately quantitatively on the tested
configuration.


## 7. Claim 3: Prediction equivalence in the ID region

### Objective

Evaluate whether the pruned model preserves the original ensemble predictions
inside the conformal in-distribution region.

### Results

| Alpha | Empirical coverage | Overall fidelity | In-region fidelity | Active trees |
| ----: | -----------------: | ---------------: | -----------------: | -----------: |
|  0.05 |             0.9301 |           1.0000 |             1.0000 |        10/10 |
|  0.10 |             0.8741 |           1.0000 |             1.0000 |         9/10 |
|  0.20 |             0.8042 |           1.0000 |             1.0000 |         9/10 |
|  0.40 |             0.5455 |           0.9930 |             1.0000 |         8/10 |
|  0.80 |             0.2168 |           0.9930 |             1.0000 |         8/10 |


In-region fidelity remained exactly 1.0000 in all five runs.

At alpha 0.40 and alpha 0.80:

- Overall fidelity:   0.9930
- In-region fidelity: 1.0000

This distinction is important. It shows that prediction disagreement can occur
outside the protected region while predictions remain equivalent inside it.

### Evidence

- tables/claim3_equivalence_final.csv

the same raw configurations, result files, and logs used for Claim 2

### Interpretation

No disagreement was observed inside the calibrated region for any tested alpha
value.

This is empirical evidence consistent with PINE's prediction-equivalence
objective. It is not presented as a proof of the theoretical guarantee.

### Verdict

Empirically reproduced on the tested configuration.


## 8. Observations

- Coverage decreased monotonically as alpha increased.
- Tau also decreased as alpha increased.
- More pruning became possible when the protected region became smaller.
- Alpha 0.05 retained all 10 trees.
- Alpha 0.40 and alpha 0.80 retained 8 of 10 trees.
- In-region fidelity remained perfect even when overall fidelity decreased.
- The number of oracle calls decreased from five at alpha 0.05 to one at
- alpha 0.40 and alpha 0.80.
- All controlled runs completed quickly for the 10-tree model.
- Legacy 30-tree and 50-tree results were preserved but were not mixed into
- the controlled alpha sweep.

## 9. Deviations from the paper

- Only one dataset was used for the controlled alpha sweep.
- Only XGBoost was used.
- Only one random seed was used.
- The ensemble contained 10 estimators.
- The complete Table 1 and Figure 3 baseline comparison was not reproduced.
- The complete scalability grid from Tables 2 and 3 was not reproduced.
- FIPE was not evaluated under a fully matched controlled setup.
- Hardware differed from the paper's experimental environment.
- The experiment used the repository's public CLI defaults where applicable.


## 10. Limitations

The study does not establish:

- that the observed calibration behavior holds for every dataset or seed,
- that PINE always outperforms FIPE,
- that the full reported scalability behavior reproduces,
- that empirical in-region fidelity proves the theoretical guarantee.

The test set is finite. Coverage differences from the nominal target may
therefore arise from finite-sample variation and split composition.

The controlled results support Claims 2 and 3 for the tested setting only.

## 11. Lessons learned

- Output behavior must be inspected

The CLI appends to CSV files. Without manual inspection, duplicate rows could
have been mistaken for independent evidence.

- Automation also requires validation

A script completing successfully does not imply that it wrote to the expected
location or preserved the intended configuration.

- Raw metrics are not sufficient

Overall fidelity and in-region fidelity answer different questions. The
scientific conclusion depended on interpreting that distinction correctly.


## 12. Conclusion

This study produced a verified partial reproduction of two central PINE claims.

First, increasing alpha reduced the empirical coverage of the protected
in-distribution region from 0.9301 to 0.2168. The values approximately followed
the nominal target relationship 1 - alpha.

Second, in-region fidelity remained 1.0000 across all five tested alpha values.
At larger alpha values, overall fidelity fell slightly to 0.9930 while
in-region fidelity remained perfect. This behavior is consistent with PINE's
goal of protecting predictions inside the calibrated region while allowing
greater pruning freedom elsewhere.

The automated workflow was insufficient without human intervention. The
reproduction required manual environment recovery, output validation,
automation repair, duplicate detection, result transformation, and scientific
interpretation.

The outcome is therefore a rigorous, transparent partial reproduction with
traceable commands, configurations, raw outputs, runtimes, and limitations.