short = False

CRAID_param_grid = {
    "depth": [10, 15],
    "criterion": ["peto"] if short else ["peto", "tarone-ware", "wilcoxon", "logrank"],
    "min_samples_leaf": [5] if short else [5],
    'cut' : [True, False],
    "woe" : [False], #if short else [True, False], 
    "signif": [0.05] if short else [0.05, 0.1],
    "max_features": [1.0]
}

BSTR_param_grid = {
    "size_sample": [0.7], 
    "n_estimators": [10] if short else [10, 30],
    "depth": [15],
    "ens_metric_name": ["roc"] if short else ["conc", "ibs", "roc"],
    # "woe" : [], 
    "criterion": ["peto"] if short else ["peto", "tarone-ware", "wilcoxon", "logrank"], 
    "min_samples_leaf": [1, 5, 10],
    "max_features": [0.3] if short else [0.3, "sqrt"]
}

# BOOST_param_grid = {
#     "aggreg_func": ['wei'] if short else ['wei', 'mean'],
#     "criterion": ["logrank"] if short else ["peto", "tarone-ware", "wilcoxon", "logrank"],
#     "depth": [15],
#     "ens_metric_name": ["ibs"] if short else ["conc","ibs"],
#     "max_features": [0.3] if short else [0.3], #"sqrt"],
#     "min_samples_leaf": [1] if short else [1, 5, 15],
#     "mode_wei": ['square', 'exp'] if short else ['square'],#'exp'],
#     "n_estimators": [15] if short else [10, 15, 25],
#     "size_sample": [0.5] if short else [0.5, 0.7],
#     # "woe" : [],
# }

BOOST_param_grid = {
    "aggreg_func": ['wei'] if short else ['wei', 'mean'],
    "criterion": ["logrank"] if short else ["peto", "tarone-ware", "wilcoxon", "logrank"],
    "depth": [15, 25],
    "ens_metric_name": ["ibs"] if short else ["roc"],
    "max_features": [0.3] if short else ["sqrt"],
    "min_samples_leaf": [1] if short else [1, 5, 15],
    "mode_wei": ['square', 'exp'] if short else ['square', 'exp'],
    "n_estimators": [15] if short else [10, 15, 25],
    "size_sample": [0.5] if short else [0.5, 0.7],
    # "woe" : [],
}

PBC_PARAMS = {
    "TREE": CRAID_param_grid,
    "BSTR": BSTR_param_grid,
    "BOOST": BOOST_param_grid
}