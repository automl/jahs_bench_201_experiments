import hpbandster.core.result as hpres
import numpy as np
import os

MAX_BUDGET = {
    "cifar10": 175571,
    "colorectal_histology": 18336,
    "fashionMNIST": 193248
}


def get_seed_info(path, seed, get_loss_from_run_fn=lambda r: r.loss):
    # load runs from log file
    result = hpres.logged_results_to_HBS_result(os.path.join(path, str(seed)))
    # get all executed runs
    all_runs = result.get_all_runs()

    dataset = list(filter(
        None,
        list(map(lambda _d: _d if _d in path else None, MAX_BUDGET.keys()))
    ))[0]

    runtime = {"started": [], "finished": []}
    data = []
    for r in all_runs:
        if r.loss is None:
            continue

        _id = r.config_id
        loss = get_loss_from_run_fn(r)

        info = dict()
        for k, v in r.info.items():
            if k == "cost":
                v /= MAX_BUDGET[dataset]
            info[k] = v

        data.append((_id, loss, info))

        for time, time_list in runtime.items():
            time_list.append(r.time_stamps[time])

    if "Epochs" in path or "diagonal" in path:
        data.reverse()
        for idx, (_id, loss, info) in enumerate(data):
            for _i, _, _info in data[data.index((_id, loss, info)) + 1:]:
                if _i != _id:
                    continue
                info["cost"] -= _info["cost"]
                data[idx] = (_id, loss, info)
                break
        data.reverse()

    data = [(d[1], d[2]) for d in data]
    losses, infos = zip(*data)
    total_runtime = runtime["finished"][-1] - runtime["started"][0]

    return list(losses), list(infos), total_runtime
