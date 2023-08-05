import sksurv.metrics
import numpy as np
from numba import njit, jit
from lifelines import KaplanMeierFitter, NelsonAalenFitter
from lifelines.utils import concordance_index

from .constants import TIME_NAME, CENS_NAME

METRIC_DICT = {
    "CI": lambda y_tr, y_tst, pr_time, pr_surv, pr_haz, bins:
        concordance_index(y_tst[TIME_NAME], pr_time),
    "CI_CENS": lambda y_tr, y_tst, pr_time, pr_surv, pr_haz, bins:
        concordance_index(y_tst[TIME_NAME], pr_time, y_tst[CENS_NAME]),
    "IBS": lambda y_tr, y_tst, pr_time, pr_surv, pr_haz, bins:
        ibs(y_tr, y_tst, pr_surv, bins),
    "IAUC": lambda y_tr, y_tst, pr_time, pr_surv, pr_haz, bins:
        iauc(y_tr, y_tst, pr_haz, bins)
}
""" dict: Available metrics in library and its realization """

DESCEND_METRICS = ['ibs', 'IBS']
""" list: Metrics with decreasing quality improvement """

@jit
def get_before(estim, wei):
    return np.square(estim) * wei

@jit
def get_after(estim, prob_cens):
    return np.square(1 - estim) / prob_cens


def ibs(survival_train, survival_test, estimate, times, axis=-1):
    """
    Modified integrated brier score from scikit-survival (add axis)
    Modification: with axis = 0 count ibs for each observation

    Parameters
    ----------
    survival_train : structured array, shape = (n_train_samples,)
        Survival times for training data to estimate the censoring
        distribution from.
        A structured array containing the binary event indicator
        as first field, and time of event or time of censoring as
        second field.
    survival_test : structured array, shape = (n_samples,)
        Survival times of test data.
        A structured array containing the binary event indicator
        as first field, and time of event or time of censoring as
        second field.
    estimate : array-like, shape = (n_samples, n_times)
        Estimated risk of experiencing an event for test data at `times`.
        The i-th column must contain the estimated probability of
        remaining event-free up to the i-th time point.
    times : array-like, shape = (n_times,)
        The time points for which to estimate the Brier score.
    axis : int, optional
        With axis = 1 count bs for each time from times
        With axis = 0 count ibs for each observation.
        With axis = -1 count mean ibs.
        The default is -1.

    Returns
    -------
    ibs_value : float or array-like or None
        if axis = 0 return array of ibs for each observation
           axis = 1 return array of bs for each time from times
           axis = -1 return float
        else
            None

    """
    test_event, test_time = sksurv.metrics.check_y_survival(survival_test, allow_all_censored = True)
    # estimate, times = _check_estimate_2d(estimate, test_time, times)
    estimate = np.array(estimate)
    if estimate.ndim == 1 and times.shape[0] == 1:
        estimate = estimate.reshape(-1, 1)
    estimate[estimate == -np.inf] = 0
    estimate[estimate == np.inf] = 0
    # fit IPCW estimator
    cens = sksurv.metrics.CensoringDistributionEstimator().fit(survival_train)
    # calculate inverse probability of censoring weight at current time point t.
    prob_cens_t = cens.predict_proba(times)
    prob_cens_t[prob_cens_t == 0] = np.inf
    # calculate inverse probability of censoring weights at observed time point
    prob_cens_y = cens.predict_proba(test_time)
    prob_cens_y[prob_cens_y == 0] = np.inf
    wei = test_event / prob_cens_y
    
    estim_before = get_before(estimate, wei[np.newaxis,:].T)
    estim_after = get_after(estimate, prob_cens_t)
    brier_scores = np.array([np.where(test_time <= t, 
                                      estim_before[:, i], 
                                      estim_after[:, i])
                             for i, t in enumerate(times)])
    if axis == -1:  # mean ibs for each time and observation
        brier_scores = np.mean(brier_scores, axis=1)
        return np.trapz(brier_scores, times) / (times[-1] - times[0])
    elif axis == 0:  # ibs for each observation
        return np.trapz(brier_scores, times, axis=0) / (times[-1] - times[0])
    elif axis == 1:  # bs in time (for graphics)
        return np.mean(brier_scores, axis=1)
    return None


def iauc(survival_train, survival_test, estimate, times, tied_tol=1e-8):
    """
    Modified integrated AUC (cumulative_dynamic_auc) 
        from scikit-survival (reduce complexity)

    Parameters
    ----------
    survival_train : structured array, shape = (n_train_samples,)
        Survival times for training data to estimate the censoring
        distribution from.
        A structured array containing the binary event indicator
        as first field, and time of event or time of censoring as
        second field.
    survival_test : structured array, shape = (n_samples,)
        Survival times of test data.
        A structured array containing the binary event indicator
        as first field, and time of event or time of censoring as
        second field.
    estimate : array-like, shape = (n_samples, n_times)
        Estimated risk of experiencing an event for test data at `times`.
        The i-th column must contain the estimated probability of
        remaining event-free up to the i-th time point.
    times : array-like, shape = (n_times,)
        The time points for which to estimate the Brier score.
    tied_tol : float, optional, default: 1e-8
        The tolerance value for considering ties.
        If the absolute difference between risk scores is smaller
        or equal than `tied_tol`, risk scores are considered tied.
        
    Returns
    -------
    mean_auc : float
        Summary measure referring to the mean cumulative/dynamic AUC
        over the specified time range `(times[0], times[-1])`.

    """
    if survival_train[CENS_NAME].sum() == 0:
        survival_train[CENS_NAME] = 1
        survival_test[CENS_NAME] = 1 - survival_test[CENS_NAME]
    if survival_test[CENS_NAME].sum() == 0:
        survival_test[CENS_NAME] = 1
    test_event, test_time = sksurv.metrics.check_y_survival(survival_test)
    # estimate, times = _check_estimate_2d(estimate, test_time, times)
    estimate = np.array(estimate)
    n_samples = estimate.shape[0]
    n_times = times.shape[0]
    if estimate.ndim == 1:
        estimate = np.broadcast_to(estimate[:, np.newaxis], (n_samples, n_times))

    # fit and transform IPCW
    cens = sksurv.metrics.CensoringDistributionEstimator()
    cens.fit(survival_train)
    Ghat = cens.predict_proba(test_time[test_event])
    ipcw = np.zeros(test_time.shape[0])
    Ghat[Ghat == 0] = np.inf
    if not((Ghat == 0.0).any()):
        ipcw[test_event] = 1.0 / Ghat
    else:
        ipcw = np.ones(test_time.shape[0])

    # expand arrays to (n_samples, n_times) shape
    test_time = np.broadcast_to(test_time[:, np.newaxis], (n_samples, n_times))
    test_event = np.broadcast_to(test_event[:, np.newaxis], (n_samples, n_times))
    times_2d = np.broadcast_to(times, (n_samples, n_times))
    ipcw = np.broadcast_to(ipcw[:, np.newaxis], (n_samples, n_times))

    # sort each time point (columns) by risk score (descending)
    o = np.argsort(-estimate, axis=0)
    test_time = np.take_along_axis(test_time, o, axis=0)
    test_event = np.take_along_axis(test_event, o, axis=0)
    estimate = np.take_along_axis(estimate, o, axis=0)
    ipcw = np.take_along_axis(ipcw, o, axis=0)

    is_case = (test_time <= times_2d) & test_event
    is_control = test_time > times_2d
    n_controls = is_control.sum(axis=0)

    # prepend row of infinity values
    estimate_diff = np.concatenate((np.broadcast_to(np.infty, (1, n_times)), estimate))
    is_tied = np.absolute(np.diff(estimate_diff, axis=0)) <= tied_tol

    cumsum_tp = np.cumsum(is_case * ipcw, axis=0)
    cumsum_fp = np.cumsum(is_control, axis=0)
    true_pos = cumsum_tp / cumsum_tp[-1]
    false_pos = cumsum_fp / n_controls

    scores = np.empty(n_times, dtype=float)
    it = np.nditer((true_pos, false_pos, is_tied), order="F", flags=["external_loop"])
    with it:
        for i, (tp, fp, mask) in enumerate(it):
            idx = np.flatnonzero(mask) - 1
            # only keep the last estimate for tied risk scores
            tp_no_ties = np.delete(tp, idx)
            fp_no_ties = np.delete(fp, idx)
            # Add an extra threshold position
            # to make sure that the curve starts at (0, 0)
            tp_no_ties = np.r_[0, tp_no_ties]
            fp_no_ties = np.r_[0, fp_no_ties]
            scores[i] = np.trapz(tp_no_ties, fp_no_ties)

    scores[np.isnan(scores)] = 0
    if n_times == 1:
        mean_auc = scores[0]
    else:
        surv = KaplanMeierFitter()
        surv.fit(survival_test[TIME_NAME], survival_test[CENS_NAME]) 
        s_times = surv.survival_function_at_times(times).to_numpy()
        
        # compute integral of AUC over survival function
        d = -np.diff(np.r_[1.0, s_times])
        integral = (scores * d).sum()
        mean_auc = integral / (1.0 - s_times[-1])

    return mean_auc


def ipa(survival_train, survival_test, estimate, times, axis=-1):
    """
    Index of Prediction Accuracy: General R^2 for binary outcome and right
    censored time to event (survival) outcome also with competing risks.

    Parameters
    ----------
    survival_train : structured array, shape = (n_train_samples,)
        Survival times for training data to estimate the censoring
        distribution from.
        A structured array containing the binary event indicator
        as first field, and time of event or time of censoring as
        second field.
    survival_test : structured array, shape = (n_samples,)
        Survival times of test data.
        A structured array containing the binary event indicator
        as first field, and time of event or time of censoring as
        second field.
    estimate : array-like, shape = (n_samples, n_times)
        Estimated risk of experiencing an event for test data at `times`.
        The i-th column must contain the estimated probability of
        remaining event-free up to the i-th time point.
    times : array-like, shape = (n_times,)
        The time points for which to estimate the Brier score.
    axis : int, optional
        With axis = 1 count ipa for each time from times
        With axis = 0 count ipa for each observation.
        With axis = -1 count mean ipa.
        The default is -1.

    Returns
    -------
    ibs_value : float or array-like or None
        if axis = 0 return array
           axis = 1 return array
           axis = -1 return float
        else
            None

    """
    one_sf = get_survival_func(survival_train['time'], survival_train['cens'], times)[np.newaxis, :]
    kmf_estimate = np.repeat(one_sf, survival_test.shape[0], axis=0)

    ibs_model = ibs(survival_train, survival_test, estimate, times, axis)
    ibs_kmf_model = ibs(survival_train, survival_test, kmf_estimate, times, axis)
    return 1 - (ibs_model + 1e-8) / (ibs_kmf_model + 1e-8)


"""ESTIMATE FUNCTION"""


def get_survival_func(ddeath, cdeath, bins = None):
    """
    Build Kaplan-Meier Estimate of survival function

    Parameters
    ----------
    ddeath : array-like
        Times of occured events
    cdeath : array-like
        Indicate of occured events (Censoring flag)
    bins : array-like, optional
        Points of surival function. The default is None.

    Returns
    -------
    KaplanMeierFitter or array
        If bins is None return kaplan-meier model, 
                   else return values of SF.

    """
    kmf = KaplanMeierFitter()
    kmf.fit(ddeath, cdeath)
    if not(bins is None):
        return kmf.survival_function_at_times(bins).to_numpy()
    return kmf


def get_hazard_func(ddeath, cdeath, bins = None):
    """
    Build Nelson-Aalen Estimate of Hazard function

    Parameters
    ----------
    ddeath : array-like
        Times of occured events
    cdeath : array-like
        Indicate of occured events (Censoring flag)
    bins : array-like, optional
        Points of hazard function. The default is None.

    Returns
    -------
    NelsonAalenFitter or array
        If bins is None return Nelson-Aalen model, 
                   else return values of HF.

    """
    naf = NelsonAalenFitter()
    naf.fit(ddeath, cdeath)
    if not(bins is None):
        return naf.cumulative_hazard_at_times(bins).to_numpy()
    return naf

# def get_norm_hist(x, b):
#     a = np.histogram(x,bins = b)[0]
#     return a/sum(a)

# def plot_predict_surv(surves, bins, true_time, cens = 1):
#     """
#     RUN:
#         res = ssc.get_score_survival_methods(X_tv, X_tst, new_sign[:-9], bins, True)
#         plot_predict_surv({i:j[0] for i,j in res.items()}, bins, 150.0, 1)
#     """
#     fig, ax = plt.subplots()
    
#     for name, surv in surves.items():
#         ax.plot(bins, surv, 
#                 label = f"{name}, prob:{round(min(surv[np.where(bins < true_time)]),3)}")
#     ax.vlines(true_time, 0, 1, 
#               color = 'k', 
#               linestyles = ('dashed' if cens else 'solid'),
#               linewidth = 2)
#     ax.legend()
#     plt.ylim(-0.1, 1.1)
#     plt.show()

# def print_importance(feature, importance):
#     plt.subplots(figsize=(30, 8))
#     res = {f:i for f,i in zip(feature, importance)}
#     res = dict(sorted(res.items(), key = lambda x: x[1]))
#     print(res)
#     res = dict(sorted(res.items(), key = lambda x: abs(x[1]))[-15:])
#     res = dict(sorted(res.items(), key = lambda x: x[1]))
#     plt.bar(res.keys(), res.values())
#     plt.show()