short = False

CRAID_param_grid = {
    "depth": [15],
    "criterion": ["peto"] if short else ["peto", "tarone-ware", "wilcoxon", "logrank"],
    "min_samples_leaf": [5] if short else [5, 10, 20],
    'cut' : [True, False],
    "woe" : [False], #if short else [True, False], 
    "signif": [0.05] if short else [0.05, 0.15],
    "max_features": [1.0],
    "n_jobs" : [32]
}

BSTR_param_grid = {
    "size_sample": [0.7],
    "n_estimators": [10] if short else [10, 30],
    "depth": [15],
    "ens_metric_name": ["conc", "ibs"],
    # "woe" : [], 
    "criterion": ["peto"] if short else ["peto", "tarone-ware", "wilcoxon", "logrank"], 
    "min_samples_leaf": [10, 20] if short else [5, 10],
    "max_features": [0.5] if short else [0.5, "sqrt"],
    "n_jobs" : [32]
}

# BOOST_param_grid = {
#     "size_sample": [0.5] if short else [0.7],
#     "n_estimators": [15] if short else [15], 
#     "ens_metric_name": ["ibs"] if short else ["conc","ibs"],
#     "depth": [15, 25],
#     "mode_wei": ['exp'] if short else ['square','exp'],
#     # "woe" : [],
#     "criterion": ["logrank"] if short else ["peto", "tarone-ware", "wilcoxon", "logrank"],
#     "min_samples_leaf": [5, 10, 20],
#     "max_features": [0.7] if short else [0.7, "sqrt"],
#     "aggreg_func": ['wei'] if short else ['wei', 'mean']
# }

BOOST_param_grid = {
    "size_sample": [0.5] if short else [0.7],
    "n_estimators": [15] if short else [20], 
    "ens_metric_name": ["ibs"] if short else ["conc","ibs"],
    "depth": [15],
    "mode_wei": ['exp'] if short else ['exp', 'linear'],
    # "woe" : [],
    "criterion": ["logrank"] if short else ["peto", "tarone-ware", "wilcoxon", "logrank"],
    "min_samples_leaf": [10, 25],
    "max_features": [0.7] if short else [0.7],
    "aggreg_func": ['wei'] if short else ['wei', 'mean'],
    "n_jobs" : [32]
}


WUHAN_PARAMS = {
    "TREE": CRAID_param_grid,
    "BSTR": BSTR_param_grid,
    "BOOST": BOOST_param_grid
}