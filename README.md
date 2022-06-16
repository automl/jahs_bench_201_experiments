# JAHS-Bench-201 experiments

## Setup

Install JAHS-Bench-201 using pip

```bash
pip install jahs_bench_201
```

TODO: Surrogate model path

## Experiments

### First research question
To reproduce results for JAHS, run:

```bash
python src/tasks/run_task.py --dataset DATASET --seed SEED --fidelity None
```

append `--use_default_hps` or `--use_default_arch` for NAS-only or HPO-only, respectively.

### Second research question
To reproduce results, run:

```bash
python src/tasks/run_task.py --dataset DATASET --seed SEED --fidelity FIDELITY
```

where `FIDELITY` may be one of `Epochs, N, W, Resolution`.

### Leaderboard

We provide a script for SLURM-job submission for all leaderboard entries, before running:

```bash
bash src/tasks/run_all.sh
```

please adjust the user-specific paths in `startup.sh` and `run_all.sh`

### Analysis

To reproduce plots from Section 4:

```bash
python src/tasks/analysis/analysis.py
```

To reproduce Table 4 and 5:

```bash
python src/tasks/analysis/compare_runtime.py
```

To generate leaderboard: 

```bash
python src/tasks/analysis/leaderboard.py
```