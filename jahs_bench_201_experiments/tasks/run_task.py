import os
import pickle
from path import Path

from jahs_bench_201_experiments.jahs_bench_201_experiments.tasks.optimizer.random_search import RandomSearch
from jahs_bench_201_experiments.jahs_bench_201_experiments.tasks.optimizer.successive_halving import SuccessiveHalving
from jahs_bench_201_experiments.jahs_bench_201_experiments.utils.setup import set_seed, args
from jahs_bench_201_experiments.jahs_bench_201_experiments.tasks.wrapper.jahs_bench_wrapper import JAHS_Bench_wrapper

import hpbandster.core.result as hpres
import hpbandster.core.nameserver as hpns

set_seed(args.seed)

if args.multi_objective:
    experiment = "MO_"
else:
    experiment = ""
if args.fidelity is None:
    experiment += "RS"
else:
    if len(args.fidelity) == 4:
        experiment += f"SH_diagonal"
    else:
        experiment += f"SH_{args.fidelity}"
if args.use_default_hps:
    experiment += "_just_nas"
elif args.use_default_arch:
    experiment += "_just_hpo"
args.working_directory = os.path.join(args.working_directory, f"{args.dataset}")
args.working_directory = os.path.join(args.working_directory, experiment, str(args.seed))

working_dir = Path(args.working_directory)
working_dir.makedirs_p()

result_logger = hpres.json_result_logger(directory=args.working_directory,
                                         overwrite=False)

NS = hpns.NameServer(
    run_id=args.run_id,
    host=args.host,
    port=0,
    working_directory=args.working_directory
)
ns_host, ns_port = NS.start()

worker = JAHS_Bench_wrapper(
    dataset=args.dataset,
    model_path=args.model_path,
    use_default_hps=args.use_default_hps,
    use_default_arch=args.use_default_arch,
    fidelity=args.fidelity,
    multi_objective=args.multi_objective,
    seed=args.seed,
    run_id=args.run_id,
    host=args.host,
    nameserver=ns_host,
    nameserver_port=ns_port,
    timeout=120
)

worker.run(background=True)

if args.fidelity is None:
    searcher = RandomSearch(
        configspace=worker.joint_config_space,
        run_id=args.run_id, host=args.host, nameserver=ns_host,
        nameserver_port=ns_port, result_logger=result_logger,
        min_budget=args.max_budget, max_budget=args.max_budget,
    )
else:
    searcher = SuccessiveHalving(
        configspace=worker.joint_config_space,
        run_id=args.run_id, host=args.host, nameserver=ns_host,
        nameserver_port=ns_port, result_logger=result_logger,
        min_budget=args.min_budget, max_budget=args.max_budget, eta=args.eta,
        fidelity=args.fidelity
    )

res = searcher.run(n_iterations=args.n_iterations)

with open(os.path.join(args.working_directory, 'results.pkl'), 'wb') as fh:
    pickle.dump(res, fh)

searcher.shutdown(shutdown_workers=True)
NS.shutdown()

id2config = res.get_id2config_mapping()
incumbent = res.get_incumbent_id()

print('A total of %i unique configurations were sampled.' % len(id2config.keys()))
print('A total of %i runs were executed.' % len(res.get_all_runs()))
