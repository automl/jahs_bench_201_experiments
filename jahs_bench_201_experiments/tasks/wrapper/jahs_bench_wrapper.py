import logging
import numpy as np
from typing import Union
from pathlib import Path
from copy import deepcopy

from hpbandster.core.worker import Worker

from jahs_bench.api import Benchmark
from jahs_bench.lib.core.constants import datasets
from jahs_bench.lib.core.configspace import joint_config_space

from jahs_bench_201_experiments.tasks.wrapper.utils import create_config_space
from jahs_bench_201_experiments.tasks.wrapper.utils import fidelities, get_diagonal


METRIC_BOUNDS = {
    "latency": {
        "cifar10": [0.00635562329065232, 114.1251799692699],
        "colorectal_histology": [0.0063284998354704485, 798.9547640807386],
        "fashionMNIST": [0.007562867628561484, 9.461364439356307],
    },
    "valid-acc": [0, 100]
}


def normalize_metric(data, dataset, key="latency"):
    if isinstance(METRIC_BOUNDS[key], dict):
        _min = min(METRIC_BOUNDS[key][dataset])
        _max = max(METRIC_BOUNDS[key][dataset])
    else:
        _min = min(METRIC_BOUNDS[key])
        _max = max(METRIC_BOUNDS[key])
    return (data - _min) / (_max - _min)


class JAHS_Bench_wrapper(Worker):
    def __init__(
        self,
        dataset: str,
        model_path: Union[str, Path, list],
        use_default_hps: bool = False,
        use_default_arch: bool = False,
        fidelity: str = "Epochs",
        use_surrogate: bool = True,
        multi_objective: bool = False,
        seed: int = None,
        **kwargs
    ):
        super().__init__(**kwargs)

        assert dataset in datasets, f"Other benchmarks than {datasets} not supported"

        self.dataset = dataset
        self.use_surrogate = use_surrogate  
        self.multi_objective = multi_objective

        self.benchmark_fn = Benchmark(
            task=dataset,
            save_dir=model_path,
            kind="surrogate" if use_surrogate else "live",
            download=False
        )

        self.fidelity = fidelity
        self.default_config, self._joint_config_space = create_config_space(
            use_default_arch=use_default_arch,
            use_default_hps=use_default_hps,
            fidelity=fidelity,
            seed=seed
        )

    def compute(
        self,
        config,
        budget,
        working_directory,
        *args,
        **kwargs
    ):
        query_config = deepcopy(self.default_config)
        query_config.update(config)
        if isinstance(self.fidelity, list):
            keys, vals = get_diagonal(self.fidelity)
            budgets = np.linspace(0, 1, 3)
            fidelity_dict = dict(zip(keys, vals[0][budgets.tolist().index(budget)]))
            for fidelity, val in fidelity_dict.items():
                if fidelity == "Epochs":
                    nepochs = int(val)
                else:
                    query_config[fidelity] = val
                    nepochs = 200
                if "Epochs" in query_config:
                    query_config.pop("Epochs")
        else:
            if self.fidelity == "Epochs":
                nepochs = int(budget)
            else:
                query_config[self.fidelity] = budget
                nepochs = 200
            if "Epochs" in query_config:
                query_config.pop("Epochs")

        results = self.benchmark_fn(
            config=query_config,
            nepochs=nepochs
        )
        results = results[nepochs]
        valid_acc = float(results["valid-acc"])
        latency = float(results["latency"])
        cost = float(results["runtime"])

        if self.multi_objective:
            _valid_acc = normalize_metric(valid_acc, dataset=self.dataset, key="valid-acc")
            _latency = normalize_metric(latency, dataset=self.dataset, key="latency")
            loss = 1.0 - (_valid_acc - _latency)
        else:
            loss = float(100 - valid_acc)

        return({
            'loss': loss,
            'info': dict(valid_acc=valid_acc, latency=latency, cost=cost)
        })

    @property
    def joint_config_space(self):
        return self._joint_config_space
