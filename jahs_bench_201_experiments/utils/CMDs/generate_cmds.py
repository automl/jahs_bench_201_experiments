import os
from path import Path

SEEDS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
DATASETS = ["cifar10", "colorectal_histology", "fashion_mnist"]
FIDELITIES = ["None", "Epochs", "N", "W", "Resolution", ["Epochs", "N", "W", "Resolution"]]
MULTI_OBJECTIVE = [True, False]

p = Path(__file__).parent
f = open(os.path.join(p, "all_experiments.txt"), "w+")

BASE_PATH = "/home/janowski/jahs_bench/jahs_bench_201_experiments/jahs_bench_201_experiments/tasks/"
BASE_CMD = f"python {BASE_PATH}run_task.py"
for seed in SEEDS:
    cmd = BASE_CMD + f" --seed {seed}"
    for dataset in DATASETS:
        _cmd = cmd + f" --dataset {dataset}"
        for fidelity in FIDELITIES:
            if fidelity == "None":
                fidelity += " --n_iterations 100"
            elif isinstance(fidelity, list):
                fidelity = str(fidelity)[1:-1].replace("'", "").replace(",", "") + " --n_iterations 42"
            __cmd = _cmd + f" --fidelity {fidelity}"
            for multi_objective in MULTI_OBJECTIVE:
                if multi_objective:
                    ___cmd = __cmd + " --multi_objective"
                else:
                    ___cmd = __cmd
                f.writelines(___cmd + "\n")
