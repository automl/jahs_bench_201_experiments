import os
import numpy as np
from pathlib import Path
from tabulate import tabulate
from scipy.stats import gmean

from jahs_bench_201_experiments.jahs_bench_201_experiments.utils.styles import DATASETS
from jahs_bench_201_experiments.jahs_bench_201_experiments.utils.util import get_seed_info, MAX_BUDGET

BASE_PATH = Path(__file__).parent.parent.parent / "jahs_bench_results"


speedups = dict()
# cifar10
speedups["cifar10"] = [
    [99.62572577, 14.86461287],
    [1.62661903, 14.86461287],
    [99.41268423, 12.6741935],
    [3.54399285, 12.6741935]
]
# colorectal_histology
speedups["colorectal_histology"] = [
    [99.78874498, 8.77496486],
    [1.78963823, 8.77496486],
    [99.3626619, 6.74978023],
    [4.5591782, 6.74978023]
]
# fashionMNIST
speedups["fashionMNIST"] = [
    [99.31263957, 5.6245753],
    [4.29611434, 5.6245753],
    [99.31263957, 5.06602542],
    [39.66100938, 5.06602542]
]

new_line = [
        "--------------------",
        "-----------------------",
        "-----------------------",
        "-----------------------",
        "------------------------"
    ]

results = dict()
for dataset_idx, dataset in enumerate(sorted(os.listdir(BASE_PATH))):
    if not os.path.isdir(os.path.join(BASE_PATH, dataset)):
        continue
    _base_path = os.path.join(BASE_PATH, dataset)
    results[dataset] = dict()
    results[dataset]["runtime"] = []
    results[dataset]["cost"] = []
    for strategy_idx, strategy in enumerate(sorted(os.listdir(_base_path))):
        if strategy != "RS":
            continue
        _path = os.path.join(_base_path, strategy)
        for seed in sorted(os.listdir(_path)):
            losses, infos, runtime = get_seed_info(_path, seed)
            results[dataset]["runtime"].append(runtime)
            cost = [i["cost"] for i in infos]
            results[dataset]["cost"].append(cost)

    results[dataset]["runtime"] = np.mean(results[dataset]["runtime"])
    results[dataset]["cost"] = np.mean(
        [(max([_r * MAX_BUDGET[dataset] for _r in results[dataset]["cost"][0]])) for r in
         results[dataset]["cost"]])

col_names = ["Speedup over HPO-only",
             "Speedup over NAS-only",
             "Surrogate-based [s]",
             "Training-based [days]"]
data = []
over_hpo = []
over_nas = []
for dataset in MAX_BUDGET.keys():
    _over_hpo = 100 / speedups[dataset][1][0]
    _over_nas = 100 / speedups[dataset][3][0]
    data.append(
        [DATASETS[dataset],
         "x{:.1f}".format(_over_hpo),
         "x{:.1f}".format(_over_nas),
         "{:.1f}".format(results[dataset]['runtime']),
         "{:.1f}".format(results[dataset]['cost'] / (60 * 60 * 24))
         ]
    )
    over_hpo.append(_over_hpo)
    over_nas.append(_over_nas)
data.append(new_line)
data.append(
    ["Geometric mean",
    "x{:.1f}".format(gmean(over_hpo)),
     "x{:.1f}".format(gmean(over_nas)),
    "-",
    "-"
     ]
)
data.append(new_line)

print(tabulate(data, headers=col_names))
