from math import ceil

import pandas as pd
import numpy as np
import scipy.stats as stat

from tqdm.auto import tqdm

from ..sensitivity_analysis import gvars_funcs

from typing import (
    Dict,
    Tuple,
    Union, Optional,
)


def g_star(parameters: Dict[Union[str, int], Tuple[Union[float, str]]],
           star_centres: np.ndarray,
           seed : int,
           sampler: str,
           slice_size: int,
           num_stars: int,
           corr_mat: np.ndarray,
           num_dir_samples: int,
           num_factors: int,
           report_verbose: bool,
           fictive_mat_flag: bool,
           dist_sample_file: Optional[str] = None
           ) -> Tuple[Union[pd.DataFrame, pd.Series], Union[np.ndarray, np.ndarray], Union[np.ndarray, np.ndarray]]:

    """
    This function generates a Pandas Dataframe containing ''star_points'' based on [3]

    Parameters
    ----------
    parameters : dictionary
        dictionary containing parameter names, and their attributes
    seed : int
        the seed number used in generating star points
    num_stars : int
        number of star samples
    corr_mat : np.array
        correlation matrix
    num_dir_samples : int
        number of directional samples per star point
    num_factors : int
        number of factors/parameters in model
    report_verbose : boolean
        if True will use a loading bar when generating stars, does nothing if False
    fictive_mat_flag : boolean
        if False will use correlation matrix as fictive matrix
    dist_sample_file : str
        file name of file containing custom distribution data

    Returns
    -------
    star_points_df : array_like
        Pandas DataFrame containing the GVARS star points
    x : array_like
        numpy array containing correlated star centres
    cov_mat : array_like
        numpy array containing fictive correlation matrix


    References
    ----------
    .. [1] Razavi, S., & Gupta, H. V. (2016). A new framework for comprehensive,
           robust, and efficient global sensitivity analysis: 1. Theory. Water
           Resources Research, 52(1), 423-439. doi: 10.1002/2015WR017558
    .. [2] Razavi, S., & Gupta, H. V. (2016). A new framework for comprehensive,
           robust, and efficient global sensitivity analysis: 1. Application. Water
           Resources Research, 52(1), 423-439. doi: 10.1002/2015WR017559
    .. [3] Razavi, S., & Do, C. N. (2020). Correlation Effects? A Major but Often
           Neglected Component in Sensitivity and Uncertainty Analysis. Water Resources
           Research, 56(3). doi: /10.1029/2019WR025436
    """

    # Computing fictive correlation matrix
    # Note: that corr_mat and cov_mat are the same in terms of magnitude
    if not fictive_mat_flag:
        cov_mat = corr_mat
    else:
        cov_mat = gvars_funcs.map_2_cornorm(parameters, corr_mat, report_verbose)

    # load bar if report_verbose is true
    if report_verbose:
        stars_pbar = tqdm(desc='generating star points\n', total=8, dynamic_ncols=True)

    # Generate correlated samples
    # the amount of samples is the same as the amount of stars
    z = star_centres
    j = star_centres
    if sampler == 'rnd':
        z = np.random.default_rng(seed=seed).multivariate_normal(np.zeros(num_factors), cov=cov_mat, size=num_stars)
    elif sampler == 'lhs':
        from ..sampling import lhs
        j = lhs(sp=num_stars,
                                params=len(parameters),
                                seed=seed,
                                )
    elif sampler == 'plhs':
        from ..sampling import plhs
        from ..sampling import lhs
        # autogenerate a slice size if it is not chosen
        if slice_size is None:
            if num_stars % 2 == 0:
                slice_size = num_stars/2
            else:
                slice_size = 1
        num_slices = ceil(num_stars/slice_size)
        if num_slices > 1:
            j = plhs(sp=num_stars,
                                    params=len(parameters),
                                    seed=seed,
                                    slices=num_slices,
                                     )[0]
        else:
            j = lhs(sp=num_stars,
                                    params=len(parameters),
                                    seed=seed,
                                    )

    elif sampler == 'sobol_seq':
        from ..sampling import sobol_sequence
        j = sobol_sequence(sp=num_stars,
                                           params=len(parameters),
                                           seed=seed,
                                           )
    elif sampler == 'halton_seq':
        from ..sampling import halton
        j = halton(sp=num_stars,
                                   params=len(parameters),
                                   seed=seed,
                                   )
    elif sampler == 'symlhs':
        from ..sampling import symlhs
        j = symlhs(sp=num_stars,
                                   params=len(parameters),
                                   seed=seed,
                            )
    elif sampler == None:
        pass
    else:
        raise ValueError(
            "`sampler` must be either None, or one of the following:"
            "'rnd', 'lhs', 'plhs', 'halton_seq', 'sobol_seq', 'symlhs'"
        )

    if sampler == 'lhs' or sampler == 'plhs' or sampler == 'halton_seq' or sampler == 'sobol_seq' or sampler == 'symlhs':
        # transform J to Y, where Y is a set of normally distributed points
        # with no corellation
        y = np.zeros(j.shape)
        for i in range(j.shape[1]):
            y[:, i] = stat.norm.ppf(j[:, i], 0, 1)

        # find square root of covariance matrix using choleski method
        c = np.linalg.cholesky(corr_mat)

        # find normally distributed set of samples with correlation
        z = np.matmul(c, np.transpose(y))
        z = np.transpose(z)



    if report_verbose:
        stars_pbar.update(1)

    # Generate Nstar actual multivariate samples x
    if dist_sample_file:
        x = gvars_funcs.n2x_transform(z, parameters, dist_sample_file)
    else:
        x = gvars_funcs.n2x_transform(z, parameters)

    if report_verbose:
        stars_pbar.update(1)

    # define index matrix of complement subset
    compsub = np.empty([num_factors, num_factors - 1])
    for i in range(0, num_factors):
        temp = np.arange(num_factors)
        compsub[i] = np.delete(temp, i)
    compsub = compsub.astype(int)
    if report_verbose:
        stars_pbar.update(1)

    # computer coditional variance and conditional expectation for each star center
    chol_cond_std = []
    std_cond_norm = []
    mui_on_noti = np.zeros((len(z), num_factors))
    for i in range(0, num_factors):
        noti = compsub[i]
        # 2 dimensional or greater matrix case
        if (cov_mat[noti, :][:, noti].ndim >= 2):
            cond_std = cov_mat[i][i] - np.matmul(cov_mat[i, noti],
                                                 np.matmul(np.linalg.inv(cov_mat[noti, :][:, noti]), cov_mat[noti, i]))
            chol_cond_std.append(np.linalg.cholesky([[cond_std]]).flatten())
            std_cond_norm.append(cond_std)
            for j in range(0, len(z)):
                mui_on_noti[j][i] = np.matmul(cov_mat[i, noti],
                                              np.matmul(np.linalg.inv(cov_mat[noti, :][:, noti]), z[j, noti]))
        # less then 2 dimenional matrix case
        else:
            cond_std = cov_mat[i][i] - np.matmul(cov_mat[i, noti],
                                                 np.matmul(cov_mat[noti, :][:, noti], cov_mat[noti, i]))
            chol_cond_std.append(np.linalg.cholesky([[cond_std]]).flatten())
            std_cond_norm.append(cond_std)
            for j in range(0, len(z)):
                mui_on_noti[j][i] = np.matmul(cov_mat[i, noti], np.matmul(cov_mat[noti, :][:, noti] * z[j, noti]))
    if report_verbose:
        stars_pbar.update(1)

    # Generate directional sample:
    # Create samples in correlated standard normal space
    all_section_cond_z = []
    cond_z = []
    # create num_dir_samples child_seeds for reproducibility in cross sectional samples
    ss = np.random.SeedSequence(seed)
    child_seeds = ss.spawn(num_dir_samples)
    for j in range(0, num_dir_samples):
        stnrm_base = np.random.default_rng(seed=child_seeds[j]).multivariate_normal(np.zeros(num_factors), np.eye(num_factors),
                                                                                    size=num_stars)
        for i in range(0, num_factors):
            cond_z.append(stnrm_base[:, i] * chol_cond_std[i] + mui_on_noti[:, i])
        all_section_cond_z.append(cond_z.copy())
        cond_z.clear()
    if report_verbose:
        stars_pbar.update(1)

    # transform to original distribution and compute response surface
    xi_on_xnoti = []
    tmp1 = []
    xi_on_xnoti_and_xnoti_temp = []
    xi_on_xnoti_and_xnoti = []

    # to ensure n2x transform function works properly
    param_keys = list(parameters.keys())
    param_info = list(parameters.values())

    for j in range(0, num_dir_samples):
        for i in range(0, len(parameters)):
            tmp1.append(gvars_funcs.n2x_transform(np.array([all_section_cond_z[j][i]]).transpose(), {param_keys[i]: param_info[i]}, dist_sample_file).flatten())
            tmp2 = x.copy()
            tmp2[:, i] = tmp1[i]
            xi_on_xnoti_and_xnoti_temp.append(tmp2.copy())
            # attatch results from tmp1 onto Xi_on_Xnoti and Xi_on_Xnoti_and_Xnoti
        xi_on_xnoti.append(tmp1.copy())
        tmp1.clear()  # clear for next iteration
        xi_on_xnoti_and_xnoti.append(xi_on_xnoti_and_xnoti_temp.copy())
        xi_on_xnoti_and_xnoti_temp.clear()  # clear for next iteration
    if report_verbose:
        stars_pbar.update(1)

    # Put Star points into a dataframe
    params = [*parameters]
    star_points = {}
    points = {}
    temp = np.zeros([num_dir_samples, num_factors])
    for i in range(0, num_stars):
        for j in range(0, num_factors):
            for k in range(0, num_dir_samples):
                temp[k, :] = xi_on_xnoti_and_xnoti[k][j][i]
            points[params[j]] = np.copy(temp)
        star_points[i] = points.copy()
    if report_verbose:
        stars_pbar.update(1)

    # put star points in a dataframe
    star_points_df = pd.concat(
        {key: pd.concat({k: pd.DataFrame(d) for k, d in value.items()}) for key, value in star_points.items()})
    star_points_df.index.names = ['centre', 'param', 'points']

    if report_verbose:
        stars_pbar.update(1)
        stars_pbar.close()

    return star_points_df, x, cov_mat
