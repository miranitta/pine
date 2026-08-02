from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
TABLE = ROOT / "reproduction" / "tables" / "claim2_alpha_sweep_final.csv"
FIGURES = ROOT / "reproduction" / "figures"
FIGURES.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(TABLE).sort_values("alpha")

plt.figure(figsize=(7, 4.5))
plt.plot(df["alpha"], df["target_coverage"], marker="o", label="Target: 1 - alpha")
plt.plot(
    df["alpha"],
    df["empirical_coverage"],
    marker="o",
    label="Empirical coverage",
)
plt.xlabel("Alpha")
plt.ylabel("Coverage")
plt.title("PINE: Alpha versus in-region coverage")
plt.ylim(0, 1)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(FIGURES / "alpha_vs_coverage.png", dpi=180)
plt.close()

plt.figure(figsize=(7, 4.5))
plt.plot(df["alpha"], df["pruning_rate"], marker="o")
plt.xlabel("Alpha")
plt.ylabel("Pruning rate")
plt.title("PINE: Alpha versus pruning rate")
plt.ylim(0, max(0.25, df["pruning_rate"].max() + 0.05))
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(FIGURES / "alpha_vs_pruning.png", dpi=180)
plt.close()

plt.figure(figsize=(7, 4.5))
plt.plot(df["alpha"], df["fidelity"], marker="o", label="Overall fidelity")
plt.plot(
    df["alpha"],
    df["in_region_fidelity"],
    marker="o",
    label="In-region fidelity",
)
plt.xlabel("Alpha")
plt.ylabel("Fidelity")
plt.title("PINE: Overall and in-region fidelity")
plt.ylim(0.98, 1.002)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(FIGURES / "alpha_vs_fidelity.png", dpi=180)
plt.close()

print(f"Wrote figures to {FIGURES}")
