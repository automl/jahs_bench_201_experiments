import os
import json
import numpy as np
from hpbandster.core.result import Result
from hpbandster.core.base_iteration import Datum


MAX_BUDGET = {
    "cifar10": 175571,
    "colorectal_histology": 18336,
    "fashionMNIST": 193248
}


def logged_results_to_HBS_result(directory):
    """
    from hpbandster.core.result
    function to import logged 'live-results' and return a HB_result object


    You can load live run results with this function and the returned
    HB_result object gives you access to the results the same way
    a finished run would.

    Parameters
    ----------
    directory: str
        the directory containing the results.json and config.json files

    Returns
    -------
    hpbandster.core.result.Result: :object:
        TODO

    """
    data = {}
    time_ref = float('inf')
    budget_set = set()

    with open(os.path.join(directory, 'configs.json')) as fh:
        for line in fh:

            line = json.loads(line)

            if len(line) == 3:
                config_id, config, config_info = line
            if len(line) == 2:
                config_id, config, = line
                config_info = 'N/A'

            data[tuple(config_id)] = Datum(config=config, config_info=config_info)

    with open(os.path.join(directory, 'results.json')) as fh:
        for line in fh:
            config_id, budget, time_stamps, result, exception = json.loads(line)

            id = tuple(config_id)

            data[id].time_stamps[budget] = time_stamps
            data[id].results[budget] = result
            data[id].exceptions[budget] = exception

            budget_set.add(budget)
            time_ref = min(time_ref, time_stamps['submitted'])

    # infer the hyperband configuration from the data
    budget_list = sorted(list(budget_set))

    HB_config = {
        # 'eta'        : None if len(budget_list) < 2 else budget_list[1]/budget_list[0],
        # 'min_budget' : min(budget_set),
        # 'max_budget' : max(budget_set),
        'budgets': budget_list,
        'max_SH_iter': len(budget_set),
        'time_ref': time_ref
    }
    return (Result([data], HB_config))


def get_seed_info(path, seed, get_loss_from_run_fn=lambda r: r.loss):
    # load runs from log file
    result = logged_results_to_HBS_result(os.path.join(path, str(seed)))
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



# hpbandster
# torch
# botorch
# matplotlib