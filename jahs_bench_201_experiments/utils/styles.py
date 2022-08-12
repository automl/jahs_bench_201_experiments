X_LABEL = "Approx. Full Evaluations"
Y_LABEL = "Validation Error [%]"

STRATEGIES = {
    "RS": "JAHS",
    "RS_just_hpo": "HPO-only",
    "RS_just_nas": "NAS-only",
    "SMAC": "BO-JAHS",
    "SMAC_just_hpo": "BO-HPO-only",
    "SMAC_just_nas": "BO-NAS-only",
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
    "SMACHB_Epochs": "Epochs",
    "SMACHB_N": "Depth multiplier",
    "SMACHB_W": "Width multiplier",
    "SMACHB_Resolution": "Resolution multiplier",
    "SMACHB_diagonal": "Diagonal traversal",
    "SH_diagonal": "Diagonal traversal"
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

    'SMAC': "black",
    'SMAC_just_hpo': "mediumpurple",
    'SMAC_just_nas': "lightgreen",

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
    'SMACHB_diagonal': "blue",

    'SMACHB_Epochs': "darkorange",
    'SMACHB_N': "firebrick",
    'SMACHB_W': "yellowgreen",
    'SMACHB_Resolution': "mediumorchid",
}

Y_MAP = {
    "cifar10": {"RQ_1a": [7, 20], "RQ_1b": [7, 20], "RQ_2": [9, 11], "RQ_2a": [8, 11], "RQ_2b": [8, 11]},
    "colorectal_histology": {"RQ_1a": [4, 10], "RQ_1b": [4, 10], "RQ_2": [4, 10], "RQ_2a": [4, 8], "RQ_2b": [4, 8]},
    "fashion_mnist": {"RQ_1a": [4.5, 8], "RQ_1b": [4.5, 8], "RQ_2": [4.75, 6], "RQ_2a": [4.5, 6], "RQ_2b": [4.5, 6]},
}

X_MAP = [0, 25, 50, 75, 100]

WIDTH_PT = 398.33864
