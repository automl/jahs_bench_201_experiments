X_LABEL = "Approx. Full Evaluations"
Y_LABEL = "Validation Error [%]"

STRATEGIES = {
    "RS": "JAHS",
    "RS_just_hpo": "HPO-only",
    "RS_just_nas": "NAS-only",
    "SH_Epochs": "Epochs",
    "SH_Epochs_just_hpo": "HPO-MF (epochs)",
    "SH_Epochs_just_nas": "NAS-MF (epochs)",
    "SH_N": "Depth multiplier",
    "SH_N_just_hpo": "HPO-MF (repetitions)",
    "SH_N_just_nas": "NAS-MF (repetitions)",
    "SH_W": "Width multiplier",
    "SH_W_just_hpo": "HPO-MF (width)",
    "SH_W_just_nas": "NAS-MF (width)",
    "SH_Resolution": "Resolution multiplier",
    "SH_Resolution_just_hpo": "HPO-MF (resolution)",
    "SH_Resolution_just_nas": "NAS-MF (resolution)",
    "BOHB_Epochs": "JAHS-BOHB (epochs)",
    "BOHB_N": "JAHS-BOHB (repetitions)",
    "BOHB_W": "JAHS-BOHB (width)",
    "BOHB_Resolution": "JAHS-BOHB (resolution)",
    "SH_diagonal": "Diagonal"
}

DATASETS = {
    "cifar10": "CIFAR-10",
    "colorectal_histology": "Colorectal-Histology",
    "fashion_mnist": "Fashion-MNIST"
}


COLOR_MARKER_DICT = {
    'RS': "black",
    'RS_just_hpo': "mediumpurple",
    'RS_just_nas': "lightgreen",

    'SH_Epochs': "darkorange",
    'SH_Epochs_just_hpo': "dodgerblue",
    'SH_Epochs_just_nas': "forestgreen",

    'SH_N': "firebrick",
    'SH_N_just_hpo': "dodgerblue",
    'SH_N_just_nas': "forestgreen",

    'SH_W': "yellowgreen",
    'SH_W_just_hpo': "dodgerblue",
    'SH_W_just_nas': "forestgreen",

    'SH_Resolution': "mediumorchid",
    'SH_Resolution_just_hpo': "dodgerblue",
    'SH_Resolution_just_nas': "forestgreen",

    'SH_diagonal': "blue",

    'BOHB_Epochs': "dodgerblue",
    'BOHB_N': "forestgreen",
    'BOHB_W': "firebrick",
    'BOHB_Resolution': "lightpink",
}

Y_MAP = {
    "cifar10": {"RQ_1": [9, 20], "RQ_2": [9, 11], "RQ_2a": [9, 11], "RQ_2b": [9, 11]},
    "colorectal_histology": {"RQ_1": [4, 10], "RQ_2": [4, 10], "RQ_2a": [4, 10], "RQ_2b": [4, 10]},
    "fashion_mnist": {"RQ_1": [4.5, 8], "RQ_2": [4.75, 6], "RQ_2a": [4.5, 10], "RQ_2b": [4.5, 10]},
}

X_MAP = [0, 25, 50, 75, 100]

WIDTH_PT = 398.33864
