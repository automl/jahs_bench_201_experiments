# JAHS-Bench-201 Experiments


## Installation

Clone this repository:

```bash
git clone https://github.com/automl/jahs_bench_201_experiments.git
cd jahs_bench_201_experiments
```

Install JAHS-Bench-201 using pip:

```bash
pip install git+https://github.com/automl/jahs_bench_201.git
```

Install this repository using pip:

```bash
pip install .
```

Download the surrogates:

```bash
python -m jahs_bench.download --target surrogates
```

    

## Experiments

### First research question
To reproduce results for JAHS, run:

```bash
python jahs_bench_201_experiments/tasks/run_model_free.py --dataset DATASET --seed SEED --fidelity None
```

where `DATASET` may be one of `cifar10, colorectal_histology, fashion_mnist`.

Append `--use_default_hps` or `--use_default_arch` for NAS-only or HPO-only, respectively.

### Second research question
To reproduce results, run:

```bash
python jahs_bench_201_experiments/tasks/run_model_free.py --dataset DATASET --seed SEED --fidelity FIDELITY --min_budget MIN_BUDGET --max_budget MAX_BUDGET
```

where `FIDELITY` may be one of `Epochs, N, W, Resolution` and  `DATASET` may be one of `cifar10, colorectal_histology, fashion_mnist`.


### Leaderboard

We provide a script for SLURM-job submission for all leaderboard entries, before running:

```bash
bash jahs_bench_201_experiments/tasks/run_all.sh
```

NOTE: please adjust the user-specific paths in `startup.sh` and `run_all.sh`

### Analysis

To reproduce plots from Section 4:

```bash
python jahs_bench_201_experiments/analysis/analysis.py
```

To reproduce Table 4 and 5:

```bash
python jahs_bench_201_experiments/analysis/compare_runtime.py
```

NOTE: this command requires all data.

To generate leaderboard: 

```bash
python jahs_bench_201_experiments/analysis/leaderboard.py
```

NOTE: this command requires all data.

## Repository structure:

    jahs_bench_201_experiments          # This repository
    ├── jahs_bench_201_data             # To be downloaded
    ├── jahs_bench_201_plots            # Created upon regenerating plots
    ├── jahs_bench_201_results          # Created upon running any task
    ├── jahs_bench_201_experiments
    │   ├── analysis                    # Scipts for results analysis
    │   ├── tasks                       # Scipts for results geneartion
    │   │   │── ...
    │   │   │── run_all.sh              # Script submitting SLURM array job
    │   │   │── run_model_free.py       # Main task script (model-free)
    │   │   │── run_model_based.py      # Main task script (model-based)
    │   ├── utils
