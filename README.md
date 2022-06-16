# JAHS-Bench-201 experiments

## Setup

Repository structure:

    jahs_bench_201_experiments          # This repository
    ├── jahs_bench_201_data             # To be downloaded (see notes below)
    ├── jahs_bench_201_plots            # Created upon regenerating plots
    ├── jahs_bench_201_results          # Created upon running any task
    ├── src
    │   ├── analysis                    # Scipts for results analysis
    │   ├── tasks                       # Scipts for results geneartion
    │   │   │── ...
    │   │   │── run_all.sh              # Script submitting SLURM array job
    │   │   │── run_task.py             # Main task script
    └── utils

Install JAHS-Bench-201 using pip:

```bash
pip install git+https://github.com/automl/jahs_bench_201.git
```

Install experiments-specific packages:

```bash
pip install -r requirements.txt
```

Download the surrogates:

```bash
cd jahs_bench_201_experiments
python -m jahs_bench_201.download --target surrogates
```


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
python src/analysis/analysis.py
```

To reproduce Table 4 and 5:

```bash
python src/analysis/compare_runtime.py
```

To generate leaderboard: 

```bash
python src/analysis/leaderboard.py
```