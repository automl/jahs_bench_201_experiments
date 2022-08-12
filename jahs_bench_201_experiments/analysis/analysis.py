import os
import numpy as np
import seaborn as sns
from pathlib import Path
import matplotlib.pyplot as plt

from jahs_bench_201_experiments.utils.util import (
    get_seed_info,
    MAX_BUDGET
)
from jahs_bench_201_experiments.utils.styles import (
    X_LABEL, Y_LABEL,
    X_MAP, Y_MAP
)
from jahs_bench_201_experiments.utils.plotting import (
    set_general_plot_style,
    incumbent_plot,
    save_fig
)


BASE_PATH = Path(".")

EXPERIMENTS = {
    "RQ_1a": ["RS", "RS_just_hpo", "RS_just_nas"],
    "RQ_1b": ["SMAC", "SMAC_just_hpo", "SMAC_just_nas"],
    "RQ_2a": ["SH_Epochs", "SH_N", "SH_W", "SH_Resolution", "SH_diagonal"],
    "RQ_2b": ["SMACHB_Epochs", "SMACHB_N", "SMACHB_W", "SMACHB_Resolution", "SMACHB_diagonal"]
}

for experiment, strategies_to_plot in EXPERIMENTS.items():

    set_general_plot_style()

    fig, axs = plt.subplots(
        nrows=1,
        ncols=len(MAX_BUDGET.keys()),
        figsize=(5.3, 2.2),

    )

    base_path = BASE_PATH / "jahs_bench_results"
    for dataset_idx, dataset in enumerate(sorted(os.listdir(base_path))):
        if not os.path.isdir(os.path.join(base_path, dataset)):
            continue
        _base_path = os.path.join(base_path, dataset)
        for strategy_idx, strategy in enumerate(sorted(os.listdir(_base_path))):
            incumbents = []
            costs = []
            if strategy not in strategies_to_plot:
                continue
            if not os.path.isdir(os.path.join(_base_path, strategy)):
                continue
            _path = os.path.join(_base_path, strategy)

            for seed in sorted(os.listdir(_path)):
                losses, infos, _ = get_seed_info(_path, seed)
                incumbent = np.minimum.accumulate(losses)
                incumbents.append(incumbent)
                cost = [i["cost"] for i in infos]
                costs.append(cost)

            incumbent_plot(
                ax=axs[dataset_idx],
                x=costs,
                y=incumbents,
                title=dataset,
                xlabel=X_LABEL if dataset_idx == 1 else None,
                ylabel=Y_LABEL if dataset_idx == 0 else None,
                strategy=strategy,
                log=False,
            )

            axs[dataset_idx].set_xticks(X_MAP)
            axs[dataset_idx].set_xlim(min(X_MAP), max(X_MAP))
            axs[dataset_idx].set_ylim(
                min(Y_MAP[dataset][experiment]),
                max(Y_MAP[dataset][experiment])
            )

    sns.despine(fig)

    _legend_flag = len(strategies_to_plot) % 2 != 0
    handles, labels = axs[0].get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.15) if _legend_flag else (0.5, -0.25),
        ncol=len(strategies_to_plot) if _legend_flag else 2,
        frameon=False
    )
    fig.tight_layout(pad=0, h_pad=.5)

    save_fig(
        fig,
        filename=f"{experiment}",
        output_dir=BASE_PATH / "jahs_bench_plots"
    )
