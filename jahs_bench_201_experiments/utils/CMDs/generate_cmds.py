import os

import ConfigSpace
from path import Path
from jahs_bench_201_experiments.tasks.wrapper.utils import fidelities

SEEDS = 10
MODEL_SEARCH = [True, False]
DATASETS = ["cifar10", "colorectal_histology", "fashion_mnist"]
FIDELITIES = ["None", "Epochs", "N", "W", "Resolution", ["Epochs", "N", "W", "Resolution"]]
MULTI_OBJECTIVE = [True, False]

p = Path(__file__).parent
f = open(os.path.join(p, "all_experiments.txt"), "w+")

BASE_PATH = "/home/janowski/jahs_bench/jahs_bench_201_experiments/jahs_bench_201_experiments/tasks/"
for model_search in MODEL_SEARCH:
    if model_search:
        BASE_CMD = f"python {BASE_PATH}run_model_based.py"
    else:
        BASE_CMD = f"python {BASE_PATH}run_model_free.py"
    for seed in range(1, SEEDS + 1):
        cmd = BASE_CMD + f" --seed {seed}"
        for dataset in DATASETS:
            _cmd = cmd + f" --dataset {dataset}"
            for fidelity in FIDELITIES:
                if fidelity == "None":
                    fidelity += " --n_iterations 100"
                elif isinstance(fidelity, list):
                    fidelity = str(fidelity)[1:-1].replace("'", "").replace(",", "") + " --n_iterations 60" \
                               + "--min_budget 1 --max_budget 3 "
                else:
                    if isinstance(fidelities[fidelity], ConfigSpace.hyperparameters.OrdinalHyperparameter):
                        _min_budget = fidelities[fidelity].sequence[0]
                        _max_budget = fidelities[fidelity].sequence[-1]
                    else:
                        _min_budget = fidelities[fidelity].lower
                        _max_budget = fidelities[fidelity].upper
                    fidelity += f" --min_budget {_min_budget} " \
                               f" --max_budget {_max_budget}"
                __cmd = _cmd + f" --fidelity {fidelity} "
                for multi_objective in MULTI_OBJECTIVE:
                    if multi_objective:
                        ___cmd = __cmd + " --multi_objective"
                    else:
                        ___cmd = __cmd
                    f.writelines(___cmd + "\n")
