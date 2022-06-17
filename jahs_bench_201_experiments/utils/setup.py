from pathlib import Path
import argparse
import os

import numpy as np
import random


def set_seed(seed):
    np.random.seed(seed)
    random.seed(seed)


parser = argparse.ArgumentParser(description="Experiment runner")
parser.add_argument(
    "--dataset",
    default="cifar10",
    help="The benchmark dataset to run the experiments.",
    choices=["cifar10", "colorectal_histology", "fashion_mnist"],
)
parser.add_argument(
    "--run_id",
    default="jahs_bench",
    help="run_id",
)
parser.add_argument(
    "--host",
    default="127.0.0.1",
    help="host",
)
parser.add_argument(
    "--fidelity",
    default="Epochs",
    nargs='+',
    help="fidelity.",
    choices=["Epochs", "N", "W", "Resolution", "None"],
)
parser.add_argument(
    "--model_path",
    default=Path("jahs_bench_data"),
    help="Full path to model dir",
)
parser.add_argument(
    "--working_directory",
    default=Path("jahs_bench_results"),
    help="Full path to model dir",
)
parser.add_argument(
    "--n_iterations",
    type=int, default=42,
    help="Number of search iterations."
)
parser.add_argument(
    "--min_budget",
    type=int, default=12,
    help="Min fidelity value."
)
parser.add_argument(
    "--max_budget",
    type=int, default=200,
    help="Max fidelity value."
)
parser.add_argument(
    "--seed",
    type=int,
    default=None
)
parser.add_argument(
    "--use_default_arch",
    action="store_true",
    help="Whether to use default arch"
)
parser.add_argument(
    "--use_default_hps",
    action="store_true",
    help="Whether to use default hps"
)
parser.add_argument(
    "--eta",
    default=3,
    type=float,
    help="Eta parameter for SH",
)
parser.add_argument(
    "--no_surrogate", action="store_true",
    help="Whether to use surrogate benchmark"
)
parser.add_argument(
    "--multi_objective", action="store_true",
    help="Whether to search for ['valid-acc', 'latency']"
)

args = parser.parse_args()
if len(args.fidelity) == 1:
    args.fidelity = args.fidelity[0]
if args.fidelity == "None":
    args.fidelity = None
