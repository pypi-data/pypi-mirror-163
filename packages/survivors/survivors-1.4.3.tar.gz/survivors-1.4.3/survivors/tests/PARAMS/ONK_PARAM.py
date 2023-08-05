short = False

CRAID_param_grid = {
    "depth": [10, 15],
    "criterion": ["peto"] if short else ["peto", "tarone-ware", "wilcoxon", "logrank"],
    "min_samples_leaf": [10] if short else [30, 50],
    'cut' : [False],
    "woe" : [False], #if short else [True, False], 
    "signif": [0.05, 0.15],# if short else [0.05, 0.1, 0.15],
    "max_features": [1.0],
    "n_jobs" : [40]
}

BSTR_param_grid = {
    "size_sample": [0.7],
    "n_estimators": [10] if short else [10, 30], 
    "depth": [15, 20],
    "ens_metric_name": ["conc", "ibs", "roc"],
    # "woe" : [], 
    "criterion": ["peto"] if short else ["peto", "tarone-ware", "wilcoxon", "logrank"], 
    "min_samples_leaf": [30, 50],
    "max_features": [0.2] if short else [0.2, "sqrt"],#["sqrt"],
    "n_jobs" : [40]
}

BOOST_param_grid = {
    "size_sample": [0.9], #[0.5, 0.7],
    "n_estimators": [30],
    "ens_metric_name": ["ibs"] if short else ["conc", "ibs"],
    "depth": [5],
    "mode_wei": ['exp'] if short else ['exp', 'square'],
    # "woe" : [],
    "criterion": ["logrank"] if short else ["peto", "tarone-ware", "wilcoxon", "logrank"],
    "min_samples_leaf": [5] if short else [100], #[20, 100] #[30, 50],
    "max_features": [0.4] if short else [0.5, 0.7], #[0.2, 0.5],
    "aggreg_func": ['wei'] if short else ['wei'],#, 'mean'],
    "n_jobs" : [40]
}

ONK_PARAMS = {
    "TREE": CRAID_param_grid,
    "BSTR": BSTR_param_grid,
    "BOOST": BOOST_param_grid
}