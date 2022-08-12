import os
import json
import pickle
import numpy as np
from path import Path

from jahs_bench_201_experiments.utils.setup import set_seed, args
from jahs_bench_201_experiments.tasks.wrapper.jahs_bench_wrapper import JAHS_Bench_wrapper

from smac.scenario.scenario import Scenario
from smac.facade.smac_mf_facade import SMAC4MF
from smac.facade.smac_hpo_facade import SMAC4HPO


set_seed(args.seed)

experiment = "SMAC"
if args.multi_objective:
    experiment += "_MO_"
else:
    experiment += ""
if args.fidelity is None:
    experiment += "RS"
elif args.fidelity is not None:
    suffix = "SH"
    if len(args.fidelity) == 4:
        experiment += f"{suffix}_diagonal"
    else:
        experiment += f"{suffix}_{args.fidelity}"
if args.use_default_hps:
    experiment += "_just_nas"
elif args.use_default_arch:
    experiment += "_just_hpo"
args.working_directory = os.path.join(args.working_directory, f"{args.dataset}")
args.working_directory = os.path.join(args.working_directory, experiment, str(args.seed))

working_dir = Path(args.working_directory)
working_dir.makedirs_p()

worker = JAHS_Bench_wrapper(
    dataset=args.dataset,
    model_path=args.model_path,
    use_default_hps=args.use_default_hps,
    use_default_arch=args.use_default_arch,
    fidelity=args.fidelity,
    multi_objective=args.multi_objective,
    seed=args.seed,
    run_id=args.run_id,
)

scenario = Scenario(
    {
        "run_obj": "quality",
        "runcount-limit": args.n_iterations,
        "cs": worker.joint_config_space,
        "deterministic": "true",
        "initial_incumbent": "RANDOM",
        "output_dir": args.working_directory
    }
)

rng = np.random.RandomState(np.random.randint(low=1, high=10e8))

if args.fidelity is None:
    smac = SMAC4HPO(
        scenario=scenario,
        tae_runner=worker,
        rng=rng,
    )
else:
    intensifier_kwargs = {
        'initial_budget': args.min_budget,
        'max_budget': args.max_budget,
        'eta': args.eta
    }

    smac = SMAC4MF(
        scenario=scenario,
        tae_runner=worker,
        rng=rng,
        intensifier_kwargs=intensifier_kwargs,
    )

tae = smac.get_tae_runner()

try:
    incumbent = smac.optimize()
finally:
    incumbent = smac.solver.incumbent

res = []
for id, config in smac.runhistory.ids_config.items():
    _budget = list(smac.runhistory.data.keys())[id-1].budget if args.fidelity is not None else 200
    config_id = list(smac.runhistory.data.keys())[id-1].config_id
    full_result = worker(config, budget=_budget, return_dict=True)
    res.append([config_id, {}, full_result])

with open(os.path.join(args.working_directory, 'results.json'), 'w') as fh:
    json.dump(res, fh, ensure_ascii=False, indent=1)
