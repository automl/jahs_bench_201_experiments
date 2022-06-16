import os
import torch
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.stats import sem
from botorch.utils.multi_objective.box_decompositions.dominated import (
    DominatedPartitioning
)

from jahs_bench_201_experiments.src.utils.util import get_seed_info
from jahs_bench_201_experiments.src.utils.styles import DATASETS


def calculate_hypervolume(objective_1, objective_2):
    # account for maximization of negative latency
    objective_2 = [[-o for o in obj2] for obj2 in objective_2]

    ref_point = (min([min(obj1) for obj1 in objective_1]),
                 min([min(obj2) for obj2 in objective_2]))
    volumes = []
    for i, (obj1, obj2) in enumerate(zip(objective_1, objective_2)):
        Y = np.stack([obj1, obj2]).T

        if not isinstance(ref_point, torch.Tensor):
            if not isinstance(ref_point, np.ndarray):
                ref_point = np.array(ref_point)
            ref_point = torch.from_numpy(ref_point)

        if not isinstance(Y, torch.Tensor):
            if not isinstance(Y, np.ndarray):
                Y = np.array(Y)
            Y = torch.from_numpy(Y)
        bd = DominatedPartitioning(ref_point=ref_point, Y=Y)
        volume = bd.compute_hypervolume()
        volumes.append(volume.item())

    return np.mean(volumes), sem(volumes)


def _create_markdown_table(entry, optimization="single", previous_markdown=None):
    if previous_markdown is None:
        score = "Accuracy $\pm$ SE" if optimization == "single" else "Hypervolume $\pm$ SE"
        md = f"| Rank | {score} | Name | URL | \n"
        md += "| ---- | ----- | ---- | ---- | \n"
        rank = 1
    else:
        md = previous_markdown
        rank = 100
    score, name, url = entry
    md += f"| {rank} | {score[0]} $\pm$ {score[1]} | {name} | {url} | \n"
    return md


def create_markdown(results):
    for dataset in results.keys():
        for opt in ["single", "multi"]:
            _max = (0, 0)
            for strategy in ["SH_Epochs", "SH_N", "SH_W", "SH_Resolution"]:
                r = results[dataset][opt][strategy]
                if _max[0] < r[0]:
                    _max = r
                    _key = strategy
                results[dataset][opt].pop(strategy)
            results[dataset][opt]["multi_fidelity"] = _max

    reformed_dict = {}
    for out_key, in_dict in results.items():
        for in_key, values in in_dict.items():
            for k, v in values.items():
                values[k] = tuple(np.round(v, 2))

            reformed_dict[(out_key,
                           in_key)] = values

    df = pd.DataFrame(reformed_dict)

    entry_mapping = {
        "Black-box": "RS",
        "Cost-aware": "RS",
        "Multi-fidelity": "multi_fidelity",
        "Multi multi-fidelity": "SH_diagonal"
    }

    method_mapping = {
        "RS": "random search",
        "multi_fidelity": "Hyperband",
        "SH_diagonal": "Hyperband"
    }

    optimization_mapping = {
        "single": "Single Objective",
        "multi": "Multi Objective"
    }

    md = "# JAHS-Bench-201 Leaderboards \n \n"
    for optimization in ["single", "multi"]:
        md += f"## {optimization_mapping[optimization]} \n \n"
        for entry, method in entry_mapping.items():
            md += f"### {entry} \n \n"
            for dataset in results.keys():
                md += f"#### {DATASETS[dataset]} \n \n"
                url = "[JAHS-Bench-201](https://github.com/automl/jahs_bench_201_experiments)"
                md += _create_markdown_table((df[dataset][optimization][method], method_mapping[method], url),
                                             optimization=optimization)
                md += " \n \n"
    return md


BASE_PATH = Path(__file__).parent.parent.parent / "jahs_bench_results"

results = dict()
for dataset_idx, dataset in enumerate(sorted(os.listdir(BASE_PATH))):
    results[dataset] = dict()
    results[dataset]["single"] = dict()
    results[dataset]["multi"] = dict()
    if not os.path.isdir(os.path.join(BASE_PATH, dataset)):
        continue
    _base_path = os.path.join(BASE_PATH, dataset)
    for strategy_idx, strategy in enumerate(sorted(os.listdir(_base_path))):
        accuracies = []
        latencies = []

        if not os.path.isdir(os.path.join(_base_path, strategy)):
            continue

        _path = os.path.join(_base_path, strategy)

        for seed in sorted(os.listdir(_path)):
            _, infos, _ = get_seed_info(_path, seed)
            accuracy = [i["valid_acc"] for i in infos]
            accuracies.append(accuracy)
            latency = [i["latency"] for i in infos]
            latencies.append(latency)

        if "MO" in strategy:
            results[dataset]["multi"][strategy[3:]] = calculate_hypervolume(accuracies, latencies)
        else:
            _accuracies = [np.maximum.accumulate(a)[-1] for a in accuracies]
            results[dataset]["single"][strategy] = (np.mean(_accuracies), sem(_accuracies))

md = create_markdown(results)
print(md)
