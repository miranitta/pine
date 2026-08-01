$ErrorActionPreference = "Stop"

$runs = @(
    @{ Id = "C2_A005"; Alpha = "0.05" },
    @{ Id = "C2_A010"; Alpha = "0.10" },
    @{ Id = "C2_A020"; Alpha = "0.20" },
    @{ Id = "C2_A040"; Alpha = "0.40" },
    @{ Id = "C2_A080"; Alpha = "0.80" }
)

foreach ($run in $runs) {
    $id = $run.Id
    $alpha = $run.Alpha

    $resultFile = "reproduction\results\$id.csv"
    $logFile = "reproduction\logs\$id.log"
    $runtimeFile = "reproduction\logs\${id}_runtime.txt"
    $configFile = "reproduction\configs\$id.txt"

    if (Test-Path $resultFile) {
        Remove-Item $resultFile
    }

    @"
experiment_id=$id
claim=Claim 2 - alpha controls coverage
dataset=breast_cancer
model=xgb
n_estimators=10
max_depth=2
learning_rate=0.1
seed=0
alpha=$alpha
n_bins=4
beta=1.0
norm=1
max_oracle_calls=100
test_size=0.25
calibration_size=0.25
gurobi_output=0
output=$resultFile
"@ | Set-Content $configFile

    Write-Host "Running $id with alpha=$alpha"

    $runtime = Measure-Command {
        python scripts\run_pine_chowliu.py `
            --dataset breast_cancer `
            --model xgb `
            --n-estimators 10 `
            --max-depth 2 `
            --learning-rate 0.1 `
            --seed 0 `
            --alpha $alpha `
            --n-bins 4 `
            --beta 1.0 `
            --norm 1 `
            --max-oracle-calls 100 `
            --test-size 0.25 `
            --calibration-size 0.25 `
            --gurobi-output 0 `
            --output $resultFile *>&1 |
            Tee-Object -FilePath $logFile
    }

    $runtime |
        Format-List * |
        Set-Content $runtimeFile

    Write-Host "$id completed in $($runtime.TotalSeconds) seconds"
}
