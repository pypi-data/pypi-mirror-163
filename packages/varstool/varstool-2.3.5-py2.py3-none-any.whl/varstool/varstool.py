"""
VARS Sensitivity Anlaysis Framework
-----------------------------------

The Variogram Analysis of Response Surfaces (VARS) is a
powerful sensitivity analysis (SA) method first applied
to  Earth and Environmental System models.

"""


import warnings
import decimal
import multiprocessing as mp
from math import ceil

import joblib
import contextlib

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from tqdm.auto import tqdm, trange


from joblib import Parallel, delayed


from .sampling import starvars
from .sampling import g_starvars
from .sensitivity_analysis import vars_funcs, tsgvars_funcs
from .sensitivity_analysis import gvars_funcs
from .sensitivity_analysis import tsvars_funcs
from .sensitivity_analysis import dvars_funcs

from typing import (
    Dict,
    Optional,
    Tuple,
    Union,
    Callable,
    Any,
    List,
)

from collections.abc import (
    Iterable,
)


class Model(object):
    """
    Description:
    ------------
    A wrapper class to contain various models and functions
    to be fed into VARS and its variations. The models can be
    called by simply calling the wrapper class itself.


    Parameters:
    -----------
    :param func: function of interest
    :type func: Callable
    :param unknown_options: a dictionary of options with keys as
                            parameters and values of parameter
                            values.
    :type unknown_options: dict
    """
    def __init__(
        self,
        func: Callable = None,
        unknown_options: Dict[str, Any] = {},
    ) -> None:

        # check whether the input is a callable
        assert callable(func)
        self.func = func

        # unkown_options must be a dict
        assert isinstance(unknown_options, dict)
        self.unknown_options = {}

        if unknown_options:
            self.unknown_options = unknown_options

    def __repr__(self, ) -> str:
        """official representation"""
        return "wrapped function: "+self.func.__name__

    def __str__(self, ) -> str:
        """the name of the wrapper function"""
        return self.func.__name__

    def __call__(
        self,
        params,
        options: Dict = None,
    ) -> Union[Iterable, float, int]:
        """calls the function model is wrapping"""

        # check if params is an array-like object
        assert isinstance(params,
            (pd.DataFrame, pd.Series, np.ndarray, List, Tuple))

        if options:
            self.unknown_options = options

        return self.func(params, **self.unknown_options)


class VARS(object):
    """
    Description:
    ------------
    The Python implementation of the Variogram Analysis of Response
    Surfaces (VARS) first introduced in Razavi and Gupta (2015) (see
    [1]_ and [2]_).


    Parameters:
    -----------
    :param star_centres: contains star centres of the analysis
    :type star_centres: numpy.array
    :param num_stars: number of stars to generate
    :type num_stars: int, numpy.int32, numpy.int64, defaults to 100
    :param parameters: the parameters of the model including lower and
                       upper bounds
    :type parameters: dict
    :param delta_h: the resolution of star samples
    :type delta_h: float, defaults to 0.1
    :param ivars_scales: the IVARS scales
    :type ivars_scales: tuple, defaults to (0.1, 0.3, 0.5)
    :param model: the model used in the sensitivity analysis
    :type model: varstool.Model
    :param seed: the seed number used in generating star centres
    :type seed: int, numpy.int32, numpy.int64
    :param sampler: the type of sampler used to generate star centres
    :type sampler: str
    :param slice_size: slice size for "plhs" sampler
    :type slice_size: int, numpy.int32, numpy.int64
    :param bootstrap_flag: flag to bootstrap the sensitivity analysis results
    :type bootstrap_flag: bool, defaults to False
    :param bootstrap_size: the size of bootstrapping experiment
    :type bootstrap_size: int, defaults to 1000
    :param bootstrap_ci: the condifence interval of boostrapping
    :type bootstrap_ci: float, defaults to 0.9
    :param grouping_flag: flag to conduct grouping of sensitive parameters
    :type grouping_flag: bool, defaults to False
    :param num_grps: the number of groups to categorize parameters
    :type num_grps: int, defaults to None
    :param report_verbose: flag to show the sensitvity analysis progress
    :type report_verbose: bool, False


    References:
    -----------
    .. [1] Razavi, S., & Gupta, H. V. (2016). A new framework for comprehensive,
           robust, and efficient global sensitivity analysis: 1. Theory. Water
           Resources Research, 52(1), 423-439. doi: 10.1002/2015WR017558
    .. [2] Razavi, S., & Gupta, H. V. (2016). A new framework for comprehensive,
           robust, and efficient global sensitivity analysis: 1. Application. Water
           Resources Research, 52(1), 423-439. doi: 10.1002/2015WR017559


    Contributors:
    -------------
    Razavi, Saman, (2015): algorithm, code in MATALB (c)
    Gupta, Hoshin, (2015): algorithm, code in MATLAB (c)
    Mattot, Shawn, (2019): code in C/++
    Keshavarz, Kasra, (2021): code in Python 3
    Blanchard, Cordell, (2021): code in Python 3
    """

    #-------------------------------------------
    # Constructors

    def __init__(
        self,
        star_centres: np.ndarray = np.array([]),  # sampled star centres (random numbers) used to create star points
        num_stars: Optional[int] = 100,  # number of stars
        parameters: Dict[Union[str, int], Tuple[float, float]] = {},  # name and bounds
        delta_h: Optional[float] = 0.1,  # delta_h for star sampling
        ivars_scales: Optional[Tuple[float, ...]] = (0.1, 0.3, 0.5),  # ivars scales
        model: Model = None,  # model (function) to run for each star point
        seed: Optional[int] = np.random.randint(1, 123456789),  # randomization state
        sampler: Optional[str] = None,  # one of the default random samplers of varstool
        slice_size: Optional[int] = None, # slice size for when using "plhs" sampling
        bootstrap_flag: Optional[bool] = False,  # bootstrapping flag
        bootstrap_size: Optional[int] = 1000,  # bootstrapping size
        bootstrap_ci: Optional[float] = 0.9,  # bootstrap confidence interval
        grouping_flag: Optional[bool] = False,  # grouping flag
        num_grps: Optional[int] = None,  # number of groups
        report_verbose: Optional[bool] = False,  # reporting verbose
    ) -> None:

        # initialize values
        self.parameters = parameters
        self.num_stars = num_stars
        self.delta_h = delta_h
        self.ivars_scales = ivars_scales
        self.star_centres = star_centres
        self.star_points = pd.DataFrame([])  # an empty list works for now - but needs to be changed - really?
        self.seed = seed  # seed number
        self.bootstrap_flag = bootstrap_flag
        self.bootstrap_size = bootstrap_size
        self.bootstrap_ci = bootstrap_ci
        self.grouping_flag = grouping_flag
        self.num_grps = num_grps
        self.report_verbose = report_verbose
        self.sampler = sampler  # one of the default sampling algorithms or None
        # analysis stage is set to False before running anything
        self.slice_size = slice_size
        self.model = model
        self.run_status = False

        # Check input arguments
        # default value for bootstrap_flag
        if not isinstance(bootstrap_flag, bool):
            warnings.warn(
                "`bootstrap_flag` must be either `True` or `False`."
                "default value of `False` will be considered.",
                UserWarning,
                stacklevel=1
            )
            self.bootstrap_flag = False

        # default value for the IVARS scales are 0.1, 0.3, and 0.5
        if not self.ivars_scales:
            warnings.warn(
                "IVARS scales are not valid, default values of (0.1, 0.3, 0.5) "
                "will be considered.",
                UserWarning,
                stacklevel=1
            )
            self.ivars_scales = (0.1, 0.3, 0.5)

        # if there is any value in IVARS scales that is greater than 0.5
        if any(i for i in self.ivars_scales if i > 0.5):
            warnings.warn(
                "IVARS scales greater than 0.5 are not recommended.",
                UserWarning,
                stacklevel=1
            )

        # if delta_h is not a factor of 1, NaNs or ZeroDivison might happen
        if (decimal.Decimal(str(1)) % decimal.Decimal(str(self.delta_h))) != 0:
            warnings.warn(
                "If delta_h is not a factor of 1, NaNs and ZeroDivisionError are probable. "
                "It is recommended to change `delta_h` to a divisible number by 1.",
                RuntimeWarning,
                stacklevel=1
            )

        # if delta_h is not between 0 and 1
        if (delta_h <= 0) or (delta_h >= 1):
            raise ValueError(
                "`delta_h` must be greater than 0 and less than 1."
            )

        # check seed dtype and sign
        if (not isinstance(seed, int)) or (seed < 0):
            warnings.warn(
                "`seed` must be an integer greater than zero."
                " value is set to default, i.e., randomized integer between 1 and 123456789"
            )
            self.seed = np.random.randint(1, 123456790)

        # check bootstrap dtype and sign
        if (not isinstance(bootstrap_size, int)) or (bootstrap_size < 1):
            raise ValueError(
                "`bootstrap_size` must be an integer greater than one."
                " value is set to default, i.e., 1000"
            )

        # check bootstrap ci dtype, value and sign
        if ((not isinstance(bootstrap_ci, float)) or
                (bootstrap_ci <= 0) or
                (bootstrap_ci >= 1)):
            warnings.warn(
                "bootstrap condifence interval (CI) must be a float"
                " within (0, 1) interval. Setting `boostrap_ci` value"
                " to default, i.e., 0.9"
            )
            self.bootstrap_ci = 0.9

        # check the dtypes and instances
        # `parameters`
        if not isinstance(self.parameters, dict):
            raise ValueError(
                "`parameters` must be of type `dict`; the keys must be"
                "their names, either strings or integers, and values must"
                "be the lower and upper bounds of their factor space."
            )

        if 0 < len(self.parameters) < 2:
            raise ValueError(
                "the number of parameters in a sensitivity analysis problem"
                "must be greater than 1"
            )

        # `model`
        if model:
            if not isinstance(model, Model):
                raise TypeError(
                    "`model` must be of type varstool.Model"
                )
            self.model = model

        # check the sampling algorithms
        if self.sampler == 'rnd':
            np.random.seed(self.seed)
            self.star_centres = np.random.rand(self.num_stars, len(self.parameters))
        elif self.sampler == 'lhs':
            from .sampling import lhs
            self.star_centres = lhs(sp=self.num_stars,
                                    params=len(self.parameters),
                                    seed=self.seed,
                                    )
        elif self.sampler == 'plhs':
            from .sampling import plhs, lhs
            # autogenerate a slice size if it is not chosen
            if slice_size is None:
                if self.num_stars % 2 == 0:
                    self.slice_size = self.num_stars/2
                else:
                    self.slice_size = 1
            num_slices = ceil(self.num_stars/self.slice_size)
            if num_slices > 1:
                self.star_centres = plhs(sp=self.num_stars,
                                        params=len(self.parameters),
                                        seed=self.seed,
                                        slices=num_slices,
                                         )[0]
            else:
                self.star_centres = lhs(sp=self.num_stars,
                                        params=len(self.parameters),
                                        seed=self.seed,
                                        )

        elif self.sampler == 'sobol_seq':
            from .sampling import sobol_sequence
            self.star_centres = sobol_sequence(sp=self.num_stars,
                                               params=len(self.parameters),
                                               seed=self.seed,
                                               )
        elif self.sampler == 'halton_seq':
            from .sampling import halton
            self.star_centres = halton(sp=self.num_stars,
                                       params=len(self.parameters),
                                       seed=self.seed,
                                       )
        elif self.sampler == 'symlhs':
            from .sampling import symlhs
            self.star_centres = symlhs(sp=self.num_stars,
                                       params=len(self.parameters),
                                       seed=self.seed,
                                )
        elif self.sampler == None: # default sampler is lhs
            from .sampling import lhs
            self.star_centres = lhs(sp=self.num_stars,
                                    params=len(self.parameters),
                                    seed=self.seed,
                                    )
        else:
            raise ValueError(
                "`sampler` must be either None, or one of the following:"
                "'rnd', 'lhs', 'plhs', 'halton_seq', 'sobol_seq', 'symlhs'"
            )


    # -------------------------------------------
    # Representators
    def __repr__(self) -> str:
        """shows the status of VARS analysis"""

        status_star_centres = "Star Centres: " + (str(self.star_centres.shape[0])+ " Centers Loaded" if
                                                  len(self.star_centres) != 0 else "Not Loaded")
        status_star_points = "Star Points: " + ("Loaded" if len(self.star_points) != 0 else "Not Loaded")
        status_parameters = "Parameters: " + (str(len(self.parameters))+" paremeters set" if
                                              self.parameters else "None")
        status_delta_h = "Delta h: " + (str(self.delta_h)+"" if self.delta_h else "None")
        status_model = "Model: " + (str(self.model)+"" if self.model else "None")
        status_seed = "Seed Number: " + (str(self.seed)+"" if self.seed else "None")
        status_bstrap = "Bootstrap: " + ("On" if self.bootstrap_flag else "Off")
        status_bstrap_size = "Bootstrap Size: " + (str(self.bootstrap_size)+"" if self.bootstrap_flag else "N/A")
        status_bstrap_ci = "Bootstrap CI: " + (str(self.bootstrap_ci)+"" if self.bootstrap_flag else "N/A")
        status_grouping = "Grouping: " + ("On" if self.grouping_flag else "Off")
        status_num_grps = "Number of Groups: " + (str(self.num_grps)+"" if self.num_grps else "None")
        status_verbose  = "Verbose: " + ("On" if self.report_verbose else "Off")
        status_analysis = "VARS Analysis: " + ("Done" if self.run_status else "Not Done")

        status_report_list = [status_star_centres, status_star_points, status_parameters,
                              status_delta_h, status_model, status_seed, status_bstrap,
                              status_bstrap_size, status_bstrap_ci, status_grouping,
                              status_num_grps, status_verbose, status_analysis]

        return "\n".join(status_report_list)

    def __str__(self) -> str:
        """shows the instance name of the VARS analysis experiment"""

        return self.__class__.__name__

    # -------------------------------------------
    # Core properties

    # using dunder variables for avoiding confusion with D-/GVARS sublcasses.

    @property
    def star_centres(self):
        """returns the star centre samples"""
        return self._star_centres

    @star_centres.setter
    def star_centres(self, new_centres):
        """sets the star centre samples"""
        if not isinstance(new_centres,
              (pd.DataFrame, pd.Series, np.ndarray, List, Tuple)):
            raise TypeError(
                "new_centres must be an array-like object: "
                "pandas.Dataframe, pandas.Series, numpy.array, List, Tuple"
            )
        self._star_centres = new_centres

    @property
    def star_points(self):
        """returns the star point samples"""
        return self._star_points

    @star_points.setter
    def star_points(self, new_points):
        """sets the star point samples"""
        if not isinstance(new_points,
              (pd.DataFrame, pd.Series, np.ndarray, List, Tuple)):
            raise TypeError(
                "new_points must be an array-like object: "
                "pandas.Dataframe, pandas.Series, numpy.array, List, Tuple"
            )
        self._star_points = new_points


    # -------------------------------------------
    # Core functions

    def generate_star(self) -> pd.DataFrame:
        """
        Generate VARS star points

        Returns
        -------
        star_points : pd.DataFrame
            dataframe containing star points
        """

        # generate star points
        self.star_points = starvars.star(self.star_centres,  # star centres
                                    delta_h=self.delta_h,  # delta_h
                                    parameters=[*self.parameters],  # parameters dictionary keys
                                    rettype='DataFrame',
                                    )  # return type is a dataframe

        self.star_points = vars_funcs.scale(df=self.star_points,  # star points must be scaled
                                       bounds={  # bounds are created while scaling
                                       'lb': [val[0] for _, val in self.parameters.items()],
                                       'ub': [val[1] for _, val in self.parameters.items()],
                                        }
                                        )

        self.star_points.index.names = ['centre', 'param', 'points']

        self.star_points.columns = self.parameters.keys()

        # scale star centres to correspond to newly scaled star_points
        self.star_centres = vars_funcs.scale(self.star_centres,
                                             bounds={  # bounds are created while scaling
                                                 'lb': [val[0] for _, val in self.parameters.items()],
                                                 'ub': [val[1] for _, val in self.parameters.items()],
                                             }
                                             )

        return self.star_points

    def factorimportance_plot(self, logy: bool = False):
        """
        plots the ratio of factor importance for IVARS50, VARS-TO,
        and VARS-ABE

        Parameters
        ----------
        logy : boolean
            True if variogram plot is to have a logscale y-axis

        Returns
        -------
        varax : matplotlib.axes.Axes
            the axes of the variogram plot
        barfig : matplotlib.Figure
            the figure of the bar chart
        barax : matplotlib.axes.Axes
            the axes of the bar chart
        """

        if self.run_status:

            # factor importance bar chart for vars-abe, ivars50, and vars-to
            if 0.5 in self.ivars.index:
                # normalize data using mean normalization
                df1 = self.maee.unstack(0).iloc[0]
                df2 = self.st
                df3 = self.ivars.loc[0.5]

                normalized_maee = df1 / df1.sum()
                normalized_sobol = df2 / df2.sum()
                normalized_ivars50 = df3 / df3.sum()

                # plot bar chart
                x = np.arange(len(self.parameters.keys()))  # the label locations
                width = 0.2  # the width of the bars

                barfig, barax = plt.subplots(figsize=(10,5))

                # if there are bootstrap results include them in bar chart
                if self.bootstrap_flag:
                    # normalize confidence interval limits
                    ivars50_err_upp = self.ivarsub.loc[0.5] / df3.sum()
                    ivars50_err_low = self.ivarslb.loc[0.5] / df3.sum()
                    sobol_err_upp = (self.stub / df2.to_numpy().sum()).to_numpy().flatten()
                    sobol_err_low = (self.stlb / df2.to_numpy().sum()).to_numpy().flatten()
                    maee_err_upp = self.maeeub.iloc[0] / df1.sum()
                    maee_err_low = self.maeelb.iloc[0] / df1.sum()

                    # subtract from normalized values so that error bars work properly
                    ivars50_err_upp = np.abs(ivars50_err_upp - normalized_ivars50)
                    ivars50_err_low = np.abs(ivars50_err_low - normalized_ivars50)
                    sobol_err_upp = np.abs(sobol_err_upp - normalized_sobol)
                    sobol_err_low = np.abs(sobol_err_low - normalized_sobol)
                    maee_err_upp = np.abs(maee_err_upp - normalized_maee)
                    maee_err_low = np.abs(maee_err_low - normalized_maee)

                    # create error array for bar charts
                    ivars50_err = np.array([ivars50_err_low, ivars50_err_upp])
                    sobol_err = np.array([sobol_err_low, sobol_err_upp])
                    maee_err = np.array([maee_err_low, maee_err_upp])

                    rects1 = barax.bar(x - width, normalized_maee, width, label='VARS-ABE (Morris)', yerr=maee_err, color='green')
                    rects2 = barax.bar(x, normalized_ivars50, width, label='IVARS50', yerr=ivars50_err, color='gold')
                    rects3 = barax.bar(x + width, normalized_sobol, width, label='VARS-TO (Sobol)', yerr=sobol_err, color='lightblue')
                else:
                    rects1 = barax.bar(x - width, normalized_maee, width, label='VARS-ABE (Morris)')
                    rects2 = barax.bar(x, normalized_ivars50, width, label='IVARS50')
                    rects3 = barax.bar(x + width, normalized_sobol, width, label='VARS-TO (Sobol)')

                # Add some text for labels, and custom x-axis tick labels, etc.
                barax.set_ylabel('Ratio of Factor Importance', fontsize=13)
                barax.set_xticks(x)
                barax.set_xticklabels(self.parameters.keys())
                barax.legend(fontsize=11)

                barfig.tight_layout()

                if logy:
                    barax.set_yscale('log')

                plt.show()

                return barfig, barax

    def correlation_plot(self,
                         param_names: np.ndarray):
        """
        plots the correlation between a pair of parameters, displaying
        the star points and star centres.

        Parameters
        ----------
        param_names : arraylike
            array containing the names of the two parameters you would like plotted

        Returns
        -------
        ax : matplotlib.axes.Axes
            the axes of the plot
        """
        if self.run_status:
            # get list of parameter names
            params = list(self.parameters.keys())

            # plot star centres and cross sections of a pair of parameters
            ax = self.star_points.unstack(0).loc[param_names[0]].stack(-1).plot.scatter(params.index(param_names[0]), params.index(param_names[1]), title='Star Points', color='grey',
                                                                                             marker='*')
            self.star_points.unstack(0).loc[param_names[1]].stack(-1).plot.scatter(params.index(param_names[0]), params.index(param_names[1]), ax=ax, color='green', marker="+",
                                                                                   figsize=(12, 8))
            plt.scatter(self.star_centres[:, params.index(param_names[0])], self.star_centres[:, params.index(param_names[1])], color='orange')
            plt.legend([param_names[0], param_names[1], 'star centers'])
            ax.set_ylabel(param_names[1])
            ax.set_xlabel(param_names[0])

            return ax


    def run_online(self):
        """
        runs the online version of the VARS program
        """

        # generate star points
        self.star_points = starvars.star(self.star_centres,  # star centres
                                         delta_h=self.delta_h,  # delta_h
                                         parameters=[*self.parameters],  # parameters dictionary keys
                                         rettype='DataFrame',
                                         )  # return type is a dataframe

        self.star_points = vars_funcs.scale(df=self.star_points,  # star points must be scaled
                                            bounds={  # bounds are created while scaling
                                            'lb': [val[0] for _, val in self.parameters.items()],
                                            'ub': [val[1] for _, val in self.parameters.items()],
                                             }
                                            )

        self.star_points.columns = self.parameters.keys()

        # scale star centres to correspond to newly scaled star_points
        self.star_centres = vars_funcs.scale(self.star_centres,
                                             bounds={  # bounds are created while scaling
                                                 'lb': [val[0] for _, val in self.parameters.items()],
                                                 'ub': [val[1] for _, val in self.parameters.items()],
                                             }
                                             )

        # apply model to the generated star points
        self.model_df = vars_funcs.apply_unique(func=self.model.func,
                                     df=self.star_points,
                                     axis=1,
                                     progress=self.report_verbose,
                                     )
        self.model_df.index.names = ['centre', 'param', 'points']

        # get paired values for each section based on 'h' - considering the progress bar if report_verbose is True
        if self.report_verbose:
            tqdm.pandas(desc='building pairs', dynamic_ncols=True)
            self.pair_df = self.model_df[str(self.model)].groupby(level=[0,1]).progress_apply(vars_funcs.section_df,
                                                                                   delta_h=self.delta_h)
        else:
            self.pair_df = self.model_df[str(self.model)].groupby(level=[0,1]).apply(vars_funcs.section_df,
                                                                          delta_h=self.delta_h)
        self.pair_df.index.names = ['centre', 'param', 'h', 'pair_ind']

        # include a column containing the dissimilarity between pairs
        self.pair_df['dissimilarity'] = 0.5 * (self.pair_df[0] - self.pair_df[1]).pow(2)

        # progress bar for vars analysis
        if self.report_verbose:
            vars_pbar = tqdm(desc='VARS analysis', total=10, dynamic_ncols=True) # 10 steps for different components

        # get mu_star value
        self.mu_star_df = self.model_df[str(self.model)].groupby(level=[0,1]).mean()
        self.mu_star_df.index.names = ['centre', 'param']
        if self.report_verbose:
            vars_pbar.update(1)
            #vars_pbar.write('Averages of model star evaluations (`mu_star`) calculated - access via .mu_star_df')

        # overall mean of the unique evaluated function value over all star points
        self.mu_overall = self.model_df[str(self.model)].unique().mean()
        if self.report_verbose:
            vars_pbar.update(1)
            #vars_pbar.write('Overall expected value of model evaluations (`mu_overall`) calculated - access via .mu_overall')

        # overall variance of the unique evaluated function over all star points
        self.var_overall = np.nanvar(self.model_df[str(self.model)].unique(), ddof=1)
        if self.report_verbose:
            vars_pbar.update(1)
            #vars_pbar.write('Overall variance of model evaluations (`var_overall`) calculated - access via .var_overall')

        # sectional covariogram calculation
        self.cov_section_all = vars_funcs.cov_section(self.pair_df, self.mu_star_df)
        if self.report_verbose:
            vars_pbar.update(1)
            #vars_pbar.write('Sectional covariogram `cov_section_all` calculated - access via .cov_section_all')

        # variogram calculation
        # MATLAB: Gamma
        self.gamma = vars_funcs.variogram(self.pair_df)
        if self.report_verbose:
            vars_pbar.update(1)
            #vars_pbar.write('Variogram (`gamma`) calculated - access via .gamma')

        # morris calculation
        morris_value = vars_funcs.morris_eq(self.pair_df)
        self.maee = morris_value[0] # MATLAB: MAEE
        self.mee  = morris_value[1] # MATLAB: MEE
        if self.report_verbose:
            vars_pbar.update(1)
            #vars_pbar.write('Morris MAEE and MEE (`maee` and `mee`) calculated - access via .maee and .mee')

        # overall covariogram calculation
        # MATLAB: COV
        self.cov = vars_funcs.covariogram(self.pair_df, self.mu_overall)
        if self.report_verbose:
            vars_pbar.update(1)
            #vars_pbar.write('Covariogram (`cov`) calculated - access via .cov')

        # expected value of the overall covariogram calculation
        # MATLAB: ECOV
        self.ecov = vars_funcs.e_covariogram(self.cov_section_all)
        if self.report_verbose:
            vars_pbar.update(1)
            #vars_pbar.write('Expected value of covariogram (`ecov`) calculated - access via .ecov')

        # sobol calculation
        # MATLAB: ST
        self.st = vars_funcs.sobol_eq(self.gamma, self.ecov, self.var_overall, self.delta_h)
        if self.report_verbose:
            vars_pbar.update(1)
            #vars_pbar.write('Sobol ST (`st`) calculated - access via .st')

        # IVARS calculation
        self.ivars = pd.DataFrame.from_dict({scale: self.gamma.groupby(level=0).apply(vars_funcs.ivars, scale=scale, delta_h=self.delta_h) \
             for scale in self.ivars_scales}, 'index')
        if self.report_verbose:
            vars_pbar.update(1)
            #vars_pbar.write('IVARS (`ivars`) calculated - access via .ivars')
            vars_pbar.close()

        # progress bar for factor ranking
        if self.report_verbose:
            factor_rank_pbar = tqdm(desc='factor ranking', total=2, dynamic_ncols=True) # only two components

        # do factor ranking on sobol results
        sobol_factor_ranking_array = vars_funcs.factor_ranking(self.st)
        # turn results into data frame
        self.st_factor_ranking = pd.DataFrame(data=[sobol_factor_ranking_array], columns=self.parameters.keys(), index=[''])
        if self.report_verbose:
            factor_rank_pbar.update(1)
            #factor_rank_pbar.write('Sobol ST factor ranking (`st_factor_ranking`) calculated - '
                                   #'access via .st_factor_ranking')

        # do factor ranking on IVARS results
        ivars_factor_ranking_list = []
        for scale in self.ivars_scales:
            ivars_factor_ranking_list.append(vars_funcs.factor_ranking(self.ivars.loc[scale]))
        # turn results into data frame
        self.ivars_factor_ranking = pd.DataFrame(data=ivars_factor_ranking_list, columns=self.parameters.keys(), index=self.ivars_scales)
        if self.report_verbose:
            factor_rank_pbar.update(1)
            #factor_rank_pbar.write('IVARS factor ranking (`ivars_factor_ranking`) calculated - '
                                   #'access via .ivars_factor_ranking')
            factor_rank_pbar.close()

        if self.bootstrap_flag and self.grouping_flag:
            self.gammalb, self.gammaub, self.maeelb, self.maeeub, self.stlb, self.stub, self.ivarslb, self.ivarsub, \
            self.rel_st_factor_ranking, self.rel_ivars_factor_ranking, self.ivars50_grp, self.st_grp, \
            self.reli_st_grp, self.reli_ivars50_grp = vars_funcs.bootstrapping(self.num_stars, self.pair_df, self.model_df, self.cov_section_all,
                                                                               self.bootstrap_size, self.bootstrap_ci,
                                                                               self.delta_h, self.ivars_scales,
                                                                               self.parameters, self.st_factor_ranking,
                                                                               self.ivars_factor_ranking, self.grouping_flag,
                                                                               self.num_grps, self.report_verbose)
        elif self.bootstrap_flag:
            self.gammalb, self.gammaub, self.maeelb, self.maeeub, self.stlb, self.stub, self.ivarslb, self.ivarsub, \
            self.rel_st_factor_ranking, self.rel_ivars_factor_ranking = vars_funcs.bootstrapping(self.num_stars, self.pair_df, self.model_df, self.cov_section_all,
                                                                               self.bootstrap_size, self.bootstrap_ci,
                                                                               self.delta_h, self.ivars_scales,
                                                                               self.parameters, self.st_factor_ranking,
                                                                               self.ivars_factor_ranking, self.grouping_flag,
                                                                               self.num_grps, self.report_verbose)

        # for status update
        self.run_status = True

        # output dictionary
        self.output = {
            'Gamma':self.gamma,
            'ST':self.st,
            'MAEE':self.maee,
            'MEE':self.mee,
            'COV':self.cov,
            'ECOV':self.ecov,
            'IVARS':self.ivars,
            'IVARSid':self.ivars_scales,
            'rnkST':self.st_factor_ranking,
            'rnkIVARS':self.ivars_factor_ranking,
            'Gammalb':self.gammalb if self.bootstrap_flag is True else None,
            'Gammaub':self.gammaub if self.bootstrap_flag is True else None,
            'MAEElb' :self.maeelb if self.bootstrap_flag is True else None,
            'MAEEub' :self.maeeub if self.bootstrap_flag is True else None,
            'STlb':self.stlb if self.bootstrap_flag is True else None,
            'STub':self.stub if self.bootstrap_flag is True else None,
            'IVARSlb':self.ivarslb if self.bootstrap_flag is True else None,
            'IVARSub':self.ivarsub if self.bootstrap_flag is True else None,
            'relST':self.rel_st_factor_ranking if self.bootstrap_flag is True else None,
            'relIVARS':self.rel_ivars_factor_ranking if self.bootstrap_flag is True else None,
            'Groups': [self.ivars50_grp, self.st_grp] if ((self.grouping_flag is True) and (self.bootstrap_flag is True)) else None,
            'relGrp': [self.reli_st_grp, self.reli_ivars50_grp] if ((self.grouping_flag is True) and (self.bootstrap_flag is True)) else None,
        }

        return


    def run_offline(self, model_df):
        """
        runs the offline version of VARS program

        Parameters
        ----------
        model_df : array_like
            A Pandas Dataframe that contains model ran on generated stars
        """

        # assign model_df to a class attribute
        self.model_df = model_df

        # get paired values for each section based on 'h' - considering the progress bar if report_verbose is True
        if self.report_verbose:
            tqdm.pandas(desc='building pairs', dynamic_ncols=True)
            self.pair_df = self.model_df.iloc[:, -1].groupby(level=[0,1]).progress_apply(vars_funcs.section_df,
                                                                                   delta_h=self.delta_h)
        else:
            self.pair_df = self.model_df.iloc[:, -1].groupby(level=[0,1]).apply(vars_funcs.section_df,
                                                                          delta_h=self.delta_h)
        self.pair_df.index.names = ['centre', 'param', 'h', 'pair_ind']

        # include a column containing the dissimilarity between pairs
        self.pair_df['dissimilarity'] = 0.5 * (self.pair_df[0] - self.pair_df[1]).pow(2)

        # progress bar for vars analysis
        if self.report_verbose:
            vars_pbar = tqdm(desc='VARS Analysis', total=10, dynamic_ncols=True) # 10 steps for different components

        # get mu_star value
        self.mu_star_df = self.model_df.iloc[:, -1].groupby(level=[0,1]).mean()
        self.mu_star_df.index.names = ['centre', 'param']
        if self.report_verbose:
            vars_pbar.update(1)
            # vars_pbar.write('Averages of function evaluations (`mu_star`) calculated - access via .mu_star_df')

        # overall mean of the unique evaluated function value over all star points
        self.mu_overall = self.model_df.iloc[:, -1].unique().mean()
        if self.report_verbose:
            vars_pbar.update(1)
            # vars_pbar.write('Overall expected value of function evaluations (`mu_overall`) calculated - access via .mu_overall')

        # overall variance of the unique evaluated function over all star points
        self.var_overall = np.nanvar(self.model_df.iloc[:, -1].unique(), ddof=1)
        if self.report_verbose:
            vars_pbar.update(1)
            # vars_pbar.write('Overall variance of function evaluations (`var_overall`) calculated - access via .var_overall')

        # sectional covariogram calculation
        self.cov_section_all = vars_funcs.cov_section(self.pair_df, self.mu_star_df)
        if self.report_verbose:
            vars_pbar.update(1)
            # vars_pbar.write('Sectional covariogram `cov_section_all` calculated - access via .cov_section_all')

        # variogram calculation
        # MATLAB: Gamma
        self.gamma = vars_funcs.variogram(self.pair_df)
        if self.report_verbose:
            vars_pbar.update(1)
            # vars_pbar.write('Variogram (`gamma`) calculated - access via .gamma')

        # morris calculation
        morris_value = vars_funcs.morris_eq(self.pair_df)
        self.maee = morris_value[0] # MATLAB: MAEE
        self.mee  = morris_value[1] # MATLAB: MEE
        if self.report_verbose:
            vars_pbar.update(1)
            # vars_pbar.write('Morris MAEE and MEE (`maee` and `mee`) calculated - access via .maee and .mee')

        # overall covariogram calculation
        # MATLAB: COV
        self.cov = vars_funcs.covariogram(self.pair_df, self.mu_overall)
        if self.report_verbose:
            vars_pbar.update(1)
            # vars_pbar.write('Covariogram (`cov`) calculated - access via .cov')

        # expected value of the overall covariogram calculation
        # MATLAB: ECOV
        self.ecov = vars_funcs.e_covariogram(self.cov_section_all)
        if self.report_verbose:
            vars_pbar.update(1)
            # vars_pbar.write('Expected value of covariogram (`ecov`) calculated - access via .ecov')

        # sobol calculation
        # MATLAB: ST
        self.st = vars_funcs.sobol_eq(self.gamma, self.ecov, self.var_overall, self.delta_h)
        if self.report_verbose:
            vars_pbar.update(1)
            # vars_pbar.write('Sobol ST (`st`) calculated - access via .st')

        # IVARS calculation
        self.ivars = pd.DataFrame.from_dict({scale: self.gamma.groupby(level=0).apply(vars_funcs.ivars, scale=scale, delta_h=self.delta_h) \
             for scale in self.ivars_scales}, 'index')
        if self.report_verbose:
            vars_pbar.update(1)
            vars_pbar.close()

        # progress bar for factor ranking
        if self.report_verbose:
            factor_rank_pbar = tqdm(desc='factor ranking', total=2, dynamic_ncols=True)

        # do factor ranking on sobol results
        sobol_factor_ranking_array = vars_funcs.factor_ranking(self.st)
        # turn results into data frame
        self.st_factor_ranking = pd.DataFrame(data=[sobol_factor_ranking_array], columns=self.parameters.keys(), index=[''])
        if self.report_verbose:
            factor_rank_pbar.update(1)

        # do factor ranking on IVARS results
        ivars_factor_ranking_list = []
        for scale in self.ivars_scales:
            ivars_factor_ranking_list.append(vars_funcs.factor_ranking(self.ivars.loc[scale]))
        # turn results into data frame
        self.ivars_factor_ranking = pd.DataFrame(data=ivars_factor_ranking_list, columns=self.parameters.keys(), index=self.ivars_scales)
        if self.report_verbose:
            factor_rank_pbar.update(1)
            factor_rank_pbar.close()

        if self.bootstrap_flag and self.grouping_flag:
            self.gammalb, self.gammaub, self.maeelb, self.maeeub, self.stlb, self.stub, self.ivarslb, self.ivarsub, \
            self.rel_st_factor_ranking, self.rel_ivars_factor_ranking, self.ivars50_grp, self.st_grp, \
            self.reli_st_grp, self.reli_ivars50_grp = vars_funcs.bootstrapping(self.num_stars, self.pair_df, self.model_df, self.cov_section_all,
                                                                               self.bootstrap_size, self.bootstrap_ci,
                                                                               self.delta_h, self.ivars_scales,
                                                                               self.parameters, self.st_factor_ranking,
                                                                               self.ivars_factor_ranking, self.grouping_flag,
                                                                               self.num_grps, self.report_verbose)
        elif self.bootstrap_flag:
            self.gammalb, self.gammaub, self.maeelb, self.maeeub, self.stlb, self.stub, self.ivarslb, self.ivarsub, \
            self.rel_st_factor_ranking, self.rel_ivars_factor_ranking = vars_funcs.bootstrapping(self.num_stars, self.pair_df, self.model_df, self.cov_section_all,
                                                                               self.bootstrap_size, self.bootstrap_ci,
                                                                               self.delta_h, self.ivars_scales,
                                                                               self.parameters, self.st_factor_ranking,
                                                                               self.ivars_factor_ranking, self.grouping_flag,
                                                                               self.num_grps, self.report_verbose)

        # for status update
        self.run_status = True

        # output dictionary
        self.output = {
            'Gamma':self.gamma,
            'ST': self.st,
            'MAEE':self.maee,
            'MEE':self.mee,
            'COV':self.cov,
            'ECOV':self.ecov,
            'IVARS':self.ivars,
            'IVARSid':self.ivars_scales,
            'rnkST':self.st_factor_ranking,
            'rnkIVARS':self.ivars_factor_ranking,
            'Gammalb':self.gammalb if self.bootstrap_flag is True else None,
            'Gammaub':self.gammaub if self.bootstrap_flag is True else None,
            'MAEElb': self.maeelb if self.bootstrap_flag is True else None,
            'MAEEub': self.maeeub if self.bootstrap_flag is True else None,
            'STlb':self.stlb if self.bootstrap_flag is True else None,
            'STub':self.stub if self.bootstrap_flag is True else None,
            'IVARSlb':self.ivarslb if self.bootstrap_flag is True else None,
            'IVARSub':self.ivarsub if self.bootstrap_flag is True else None,
            'relST':self.rel_st_factor_ranking if self.bootstrap_flag is True else None,
            'relIVARS':self.rel_ivars_factor_ranking if self.bootstrap_flag is True else None,
            'Groups': [self.ivars50_grp, self.st_grp] if ((self.grouping_flag is True) and (self.bootstrap_flag is True)) else None,
            'relGrp': [self.reli_st_grp, self.reli_ivars50_grp] if ((self.grouping_flag is True) and (self.bootstrap_flag is True)) else None,
        }

        return


class GVARS(VARS):
    """
    Description:
    ------------
    The Python implementation of the General Variogram Analysis of Response
    Surfaces (GVARS), this version can handle correlated factors


    Parameters:
    -----------
    :param star_centres: contains star centres of the analysis
    :type star_centres: numpy.array
    :param num_stars: number of stars to generate
    :type num_stars: int, numpy.int32, numpy.int64, defaults to 100
    :param parameters: the parameters of the model including lower and
                       upper bounds
    :type parameters: dict
    :param delta_h: the resolution of star samples
    :type delta_h: float, defaults to 0.1
    :param ivars_scales: the IVARS scales
    :type ivars_scales: tuple, defaults to (0.1, 0.3, 0.5)
    :param model: the model used in the sensitivity analysis
    :type model: varstool.Model
    :param seed: the seed number used in generating star centres
    :type seed: int, numpy.int32, numpy.int64
    :param sampler: the type of sampler used to generate star centres
    :type sampler: str
    :param slice_size: slice size for "plhs" sampler
    :type slice_size: int, numpy.int32, numpy.int64
    :param bootstrap_flag: flag to bootstrap the sensitivity analysis results
    :type bootstrap_flag: bool, defaults to False
    :param bootstrap_size: the size of bootstrapping experiment
    :type bootstrap_size: int, defaults to 1000
    :param bootstrap_ci: the condifence interval of boostrapping
    :type bootstrap_ci: float, defaults to 0.9
    :param grouping_flag: flag to conduct grouping of sensitive parameters
    :type grouping_flag: bool, defaults to False
    :param num_grps: the number of groups to categorize parameters
    :type num_grps: int, defaults to None
    :param report_verbose: flag to show the sensitvity analysis progress
    :type report_verbose: bool, False
    :param corr_mat: correlation matrix
    :type corr_mat: np.ndarray, np.array([])
    :param num_dir_samples: number of directional samples in each star sample
    :type num_dir_samples: int, 50
    :param fictive_mat_flag: flag that sets if correlation matrix it to be used in place of fictive matrix
    :type fictive_mat_flag: bool, False
    :param dist_sample_file: file name that contains custom distribution data
    :type dist_sample_file: str, None
    


    References:
    -----------
    .. [1] Razavi, S., & Gupta, H. V. (2016). A new framework for comprehensive,
           robust, and efficient global sensitivity analysis: 1. Theory. Water
           Resources Research, 52(1), 423-439. doi: 10.1002/2015WR017558
    .. [2] Razavi, S., & Gupta, H. V. (2016). A new framework for comprehensive,
           robust, and efficient global sensitivity analysis: 1. Application. Water
           Resources Research, 52(1), 423-439. doi: 10.1002/2015WR017559
    .. [3] Razavi, S., & Do, C. N. (2020). Correlation Effects? A Major but Often
           Neglected Component in Sensitivity and Uncertainty Analysis. Water Resources
           Research, 56(3). doi: /10.1029/2019WR025436


    Contributors:
    -------------
    Razavi, Saman, (2015): algorithm, code in MATALB (c)
    Gupta, Hoshin, (2015): algorithm, code in MATLAB (c)
    Mattot, Shawn, (2019): code in C/++
    Do, Nhu, (2020): algorithm, code in MATLAB (c)
    Keshavarz, Kasra, (2021): code in Python 3
    Blanchard, Cordell, (2021): code in Python 3
    """

    # -------------------------------------------
    # Constructors

    def __init__(self,
                 star_centres: np.ndarray = np.array([]), # sampled star centres (random numbers) used to create star points
                 num_stars: Optional[int] = 100,  # number of stars
                 parameters: Dict[Union[str, int], Tuple[float, float]] = {},  # name and bounds
                 delta_h: Optional[float] = 0.1,  # delta_h for star sampling
                 ivars_scales: Optional[Tuple[float, ...]] = (0.1, 0.3, 0.5),  # ivars scales
                 model: Model = None,  # model (function) to run for each star point
                 seed: Optional[int] = np.random.randint(1, 123456789),  # randomization state
                 sampler: Optional[str] = None,  # one of the default random samplers of varstool
                 slice_size: Optional[int] = None,  # slice size for when using "plhs" sampling
                 bootstrap_flag: Optional[bool] = False,  # bootstrapping flag
                 bootstrap_size: Optional[int] = 1000,  # bootstrapping size
                 bootstrap_ci: Optional[float] = 0.9,  # bootstrap confidence interval
                 grouping_flag: Optional[bool] = False,  # grouping flag
                 num_grps: Optional[int] = None,  # number of groups
                 report_verbose: Optional[bool] = False,  # reporting verbose
                 corr_mat: np.ndarray = np.array([]),  # correlation matrix
                 num_dir_samples: int = 50,  # number of directional samples
                 fictive_mat_flag: Optional[bool] = True, # if flag is false correlation matrix will be used in place of fictive matrix
                 dist_sample_file: Optional[str] = None # name of file carrying custom distributions
                 ):

        # initialize values
        super().__init__(num_stars=num_stars,
                         parameters=parameters,
                         delta_h=delta_h,
                         ivars_scales=ivars_scales,
                         model=model,
                         seed=seed,
                         bootstrap_flag=bootstrap_flag,
                         bootstrap_size=bootstrap_size,
                         bootstrap_ci=bootstrap_ci,
                         grouping_flag=grouping_flag,
                         num_grps=num_grps,
                         report_verbose=report_verbose) # initialize all values from VARS super method
        self.num_dir_samples = num_dir_samples
        self.corr_mat = corr_mat
        # number of parameters in users model
        self.num_factors = len(self.parameters)
        self.sampler = sampler
        self.slice_size = slice_size
        self.fictive_mat_flag = fictive_mat_flag
        self.dist_sample_file = dist_sample_file

        # if there is no sampler default is 'lhs'
        if sampler == None:
            self.sampler = 'lhs'

        # check if there is a custom distribution
        # for now we will set corr flag to true
        for info in self.parameters.values():
            if info[3] == 'custom':
                self.fictive_mat_flag = False

        # default value for the number of directional samples
        if not self.num_dir_samples:
            warnings.warn(
                "Number of directional samples are not valid, default value of 10 "
                "will be considered.",
                UserWarning,
                stacklevel=1
            )
            self.num_dir_samples = 10

        if not isinstance(corr_mat, np.ndarray):
            warnings.warn(
                "correlation matrix must be a numpy array, "
                "will default to a identity matrix",
                UserWarning,
                stacklevel=1
            )
            self.corr_mat = np.eye(self.num_factors)

    # -------------------------------------------
    # Representators

    def __repr__(self) -> str:
        """shows the status of GVARS analysis"""
        status_star_centres = "Star Centres: " + (str(self.star_centres.shape[0]) + " Centers Loaded" if
                                                  len(self.star_centres) != 0 else "Not Loaded")
        status_star_points = "Star Points: " + ("Loaded " + str(self.num_stars) + " stars with " + \
                                                str(self.num_dir_samples) + " directional samples" \
                                                    if len(self.star_points) != 0 else "Not Loaded")
        status_parameters = "Parameters: " + (
            str(len(self.parameters)) + " paremeters set" if self.parameters else "None")
        status_delta_h = "Delta h: " + (str(self.delta_h) + "" if self.delta_h else "None")
        status_model = "Model: " + (str(self.model) + "" if self.model else "None")
        status_seed = "Seed Number: " + (str(self.seed)+"" if self.seed else "None")
        status_bstrap = "Bootstrap: " + ("On" if self.bootstrap_flag else "Off")
        status_bstrap_size = "Bootstrap Size: " + (str(self.bootstrap_size) + "" if self.bootstrap_flag else "N/A")
        status_bstrap_ci = "Bootstrap CI: " + (str(self.bootstrap_ci) + "" if self.bootstrap_flag else "N/A")
        status_grouping = "Grouping: " + ("On" if self.grouping_flag else "Off")
        status_num_grps = "Number of Groups: " + (str(self.num_grps) + "" if self.num_grps else "None")
        status_verbose = "Verbose: " + ("On" if self.report_verbose else "Off")
        status_analysis = "GVARS Analysis: " + ("Done" if self.run_status else "Not Done")

        status_report_list = [status_star_centres, status_star_points, status_parameters, \
                              status_delta_h, status_model, status_seed, status_bstrap, \
                              status_bstrap_size, status_bstrap_ci, status_grouping, \
                              status_num_grps, status_verbose, status_analysis]

        return "\n".join(status_report_list)

    def __str__(self) -> str:
        """shows the instance name of the GVARS analysis experiment"""

        return self.__class__.__name__

    # -------------------------------------------
    # Core properties
    @property
    def star_centres(self):
        """returns the star centre samples"""
        return self._star_centres

    @star_centres.setter
    def star_centres(self, new_centres):
        """sets the star centre samples"""
        if not isinstance(new_centres,
              (pd.DataFrame, pd.Series, np.ndarray, List, Tuple)):
            raise TypeError(
                "new_centres must be an array-like object: "
                "pandas.Dataframe, pandas.Series, numpy.array, List, Tuple"
            )
        self._star_centres = new_centres

    @property
    def star_points(self):
        """returns the star point samples."""
        return self._star_points

    @star_points.setter
    def star_points(self, new_points):
        """sets the star point samples"""
        if not isinstance(new_points,
                          (pd.DataFrame, pd.Series, np.ndarray, List, Tuple)):
            raise TypeError(
                "new_points must be an array-like object: "
                "pandas.Dataframe, pandas.Series, numpy.array, List, Tuple"
            )
        self._star_points = new_points


    # -------------------------------------------
    # Core functions

    def generate_star(self) -> pd.DataFrame:
        """
        Generate GVARS star points

        Returns
        -------
        star_points : pd.DataFrame
            dataframe containing star points
        """

        # generate g_star points
        self.star_points, self.star_centres, self.cov_mat = g_starvars.g_star(
            self.parameters,  # parameters
            self.star_centres, # star centres
            self.seed,  # seed
            self.sampler, # sample method if any
            self.slice_size, # slice size if using plhs
            self.num_stars,  # number of stars
            self.corr_mat,  # correlation matrix of parameters
            self.num_dir_samples,  # number of directional samples in star points
            self.num_factors,  # number of parameters
            self.report_verbose,  # loading bar boolean value
            self.fictive_mat_flag,
            self.dist_sample_file
        )

        self.star_points.columns = self.parameters.keys()

        return self.star_points

    def factorimportance_plot(self, logy : bool=False):
        """
        plots the ratio of factor importance for IVARS50, VARS-TO,
        and VARS-ABE

        Parameters
        ----------
        logy : boolean
            True if variogram plot is to have a logscale y-axis

        Returns
        -------
        varax : matplotlib.axes.Axes
            the axes of the variogram plot
        barfig : matplotlib.Figure
            the figure of the bar chart
        barax : matplotlib.axes.Axes
            the axes of the bar chart
        """

        if self.run_status:

            # factor importance bar chart for vars-abe, ivars50, and vars-to
            if 0.5 in self.ivars.index:
                # normalize data using mean normalization
                df1 = self.maee.unstack(0).iloc[0]
                df2 = self.st
                df3 = self.ivars.loc[0.5]

                normalized_maee = df1 / df1.sum()
                normalized_sobol = df2 / df2.sum()
                normalized_ivars50 = df3 / df3.sum()

                # plot bar chart
                x = np.arange(len(self.parameters.keys()))  # the label locations
                width = 0.2  # the width of the bars

                barfig, barax = plt.subplots(figsize=(10,5))

                # if there are bootstrap results include them in bar chart
                if self.bootstrap_flag:
                    # normalize confidence interval limits
                    ivars50_err_upp = self.ivarsub.loc[0.5] / df3.sum()
                    ivars50_err_low = self.ivarslb.loc[0.5] / df3.sum()
                    sobol_err_upp = (self.stub / df2.to_numpy().sum()).to_numpy().flatten()
                    sobol_err_low = (self.stlb / df2.to_numpy().sum()).to_numpy().flatten()
                    maee_err_upp = self.maeeub.iloc[0] / df1.sum()
                    maee_err_low = self.maeelb.iloc[0] / df1.sum()

                    # subtract from normalized values so that error bars work properly
                    ivars50_err_upp = np.abs(ivars50_err_upp - normalized_ivars50)
                    ivars50_err_low = np.abs(ivars50_err_low - normalized_ivars50)
                    sobol_err_upp = np.abs(sobol_err_upp - normalized_sobol)
                    sobol_err_low = np.abs(sobol_err_low - normalized_sobol)
                    maee_err_upp = np.abs(maee_err_upp - normalized_maee)
                    maee_err_low = np.abs(maee_err_low - normalized_maee)

                    # create error array for bar charts
                    ivars50_err = np.array([ivars50_err_low, ivars50_err_upp])
                    sobol_err = np.array([sobol_err_low, sobol_err_upp])
                    maee_err = np.array([maee_err_low, maee_err_upp])

                    rects1 = barax.bar(x - width, normalized_maee, width, label='VARS-ABE (Morris)', yerr=maee_err, color='green')
                    rects2 = barax.bar(x, normalized_ivars50, width, label='IVARS50', yerr=ivars50_err, color='gold')
                    rects3 = barax.bar(x + width, normalized_sobol, width, label='VARS-TO (Sobol)', yerr=sobol_err, color='lightblue')
                else:
                    rects1 = barax.bar(x - width, normalized_maee, width, label='VARS-ABE (Morris)')
                    rects2 = barax.bar(x, normalized_ivars50, width, label='IVARS50')
                    rects3 = barax.bar(x + width, normalized_sobol, width, label='VARS-TO (Sobol)')

                # Add some text for labels, and custom x-axis tick labels, etc.
                barax.set_ylabel('Ratio of Factor Importance', fontsize=13)
                barax.set_xticks(x)
                barax.set_xticklabels(self.parameters.keys())
                barax.legend(fontsize=11)

                barfig.tight_layout()

                if logy:
                    barax.set_yscale('log')

                plt.show()

                return barfig, barax

    def correlation_plot(self,
                         param_names: np.ndarray):
        """
        plots the correlation between a pair of parameters, displaying
        the star points and star centres.

        Parameters
        ----------
        param_names : arraylike
            array containing the names of the two parameters you would like plotted

        Returns
        -------
        ax : matplotlib.axes.Axes
            the axes of the plot
        """
        if self.run_status:
            # get list of parameter names
            params = list(self.parameters.keys())

            # plot star centres and cross sections of a pair of parameters
            ax = self.star_points.unstack(0).loc[param_names[0]].stack(-1).plot.scatter(params.index(param_names[0]), params.index(param_names[1]), title='Star Points', color='grey',
                                                                                             marker='*')
            self.star_points.unstack(0).loc[param_names[1]].stack(-1).plot.scatter(params.index(param_names[0]), params.index(param_names[1]), ax=ax, color='green', marker="+", xlabel='x1',
                                                                                    ylabel='x2', figsize=(12, 8))
            plt.scatter(self.star_centres[:, params.index(param_names[0])], self.star_centres[:, params.index(param_names[1])], color='orange')
            plt.legend([param_names[0], param_names[1], 'star centers'])
            ax.set_ylabel(param_names[1])
            ax.set_xlabel(param_names[0])
            return ax

    def run_online(self):
        """
        runs online version of GVARS program
        """

        # generate g_star points
        self.star_points, self.star_centres, self.cov_mat = g_starvars.g_star(
            self.parameters,  # parameters
            self.star_centres, # star centres
            self.seed,  # seed
            self.sampler, # sample method if any
            self.slice_size, # slice size for plhs
            self.num_stars,  # number of stars
            self.corr_mat,  # correlation matrix of parameters
            self.num_dir_samples,  # number of directional samples in star points
            self.num_factors,  # number of parameters
            self.report_verbose,  # loading bar boolean value
            self.fictive_mat_flag,
            self.dist_sample_file
        )

        self.star_points.columns = self.parameters.keys()

        # apply model to the generated star points
        self.model_df = vars_funcs.apply_unique(func=self.model.func,
                                     df=self.star_points,
                                     axis=1,
                                     progress=self.report_verbose,
                                     )
        self.model_df.index.names = ['centre', 'param', 'points']

        # get paired values for each section based on 'h' - considering the progress bar if report_verbose is True
        if self.report_verbose:
            tqdm.pandas(desc='building pairs', dynamic_ncols=True)
            self.pair_df = self.model_df[str(self.model)].groupby(level=[0, 1]).progress_apply(vars_funcs.section_df,
                                                                                    delta_h=self.delta_h)
        else:
            self.pair_df = self.model_df[str(self.model)].groupby(level=[0, 1]).apply(vars_funcs.section_df,
                                                                           delta_h=self.delta_h)
        self.pair_df.index.names = ['centre', 'param', 'h', 'pair_ind']

        # get rid of irrelevant h values
        self.pair_df = self.pair_df.droplevel('h')

        # bin and reorder pairs according to actual 'h' values
        xmin, xmax = gvars_funcs.find_boundaries(self.parameters, self.dist_sample_file)
        self.pair_df = gvars_funcs.reorder_pairs(self.pair_df, self.num_stars, self.parameters, self.model_df, self.delta_h, self.report_verbose, xmax, xmin, False)
        # include a column containing the dissimilarity between pairs
        self.pair_df['dissimilarity'] = 0.5 * (self.pair_df[0] - self.pair_df[1]).pow(2)

        # progress bar for vars analysis
        if self.report_verbose:
            vars_pbar = tqdm(desc='GVARS analysis', total=10, dynamic_ncols=True)  # 10 steps for different components

        # get mu_star value
        self.mu_star_df = self.model_df[str(self.model)].groupby(level=[0, 1]).mean()
        self.mu_star_df.index.names = ['centre', 'param']
        if self.report_verbose:
            vars_pbar.update(1)
            # vars_pbar.write('Averages of function evaluations (`mu_star`) calculated - access via .mu_star_df')

        # overall mean of the unique evaluated function value over all star points
        self.mu_overall = self.model_df[str(self.model)].unique().mean()
        if self.report_verbose:
            vars_pbar.update(1)
            # vars_pbar.write('Overall expected value of function evaluations (`mu_overall`) calculated - access via .mu_overall')

        # overall variance of the unique evaluated function over all star points
        self.var_overall = np.nanvar(self.model_df[str(self.model)].unique(), ddof=1)
        if self.report_verbose:
            vars_pbar.update(1)
            # vars_pbar.write('Overall variance of function evaluations (`var_overall`) calculated - access via .var_overall')

        # sectional covariogram calculation
        self.cov_section_all = vars_funcs.cov_section(self.pair_df, self.mu_star_df)
        if self.report_verbose:
            vars_pbar.update(1)
            # vars_pbar.write('Sectional covariogram `cov_section_all` calculated - access via .cov_section_all')

        # variogram calculation
        # MATLAB: Gamma
        self.gamma = vars_funcs.variogram(self.pair_df)
        if self.report_verbose:
            vars_pbar.update(1)
            # vars_pbar.write('Variogram (`gamma`) calculated - access via .gamma')

        # morris calculation
        morris_value = vars_funcs.morris_eq(self.pair_df)
        self.maee = morris_value[0]  # MATLAB: MAEE
        self.mee = morris_value[1]  # MATLAB: MEE
        if self.report_verbose:
            vars_pbar.update(1)
            # vars_pbar.write('Morris MAEE and MEE (`maee` and `mee`) calculated - access via .maee and .mee')

        # overall covariogram calculation
        # MATLAB: COV
        self.cov = vars_funcs.covariogram(self.pair_df, self.mu_overall)
        if self.report_verbose:
            vars_pbar.update(1)
            # vars_pbar.write('Covariogram (`cov`) calculated - access via .cov')

        # expected value of the overall covariogram calculation
        # MATLAB: ECOV
        self.ecov = vars_funcs.e_covariogram(self.cov_section_all)
        if self.report_verbose:
            vars_pbar.update(1)
            # vars_pbar.write('Expected value of covariogram (`ecov`) calculated - access via .ecov')

        # sobol calculation
        # MATLAB: ST
        self.st = vars_funcs.sobol_eq(self.gamma, self.ecov, self.var_overall, self.delta_h)
        if self.report_verbose:
            vars_pbar.update(1)
            # vars_pbar.write('Sobol ST (`st`) calculated - access via .st')

        # IVARS calculation
        self.ivars = pd.DataFrame.from_dict(
            {scale: self.gamma.groupby(level=0).apply(vars_funcs.ivars, scale=scale, delta_h=self.delta_h) \
             for scale in self.ivars_scales}, 'index')
        if self.report_verbose:
            vars_pbar.update(1)
            vars_pbar.close()


        # progress bar for factor ranking
        if self.report_verbose:
            factor_rank_pbar = tqdm(desc='factor ranking', total=2, dynamic_ncols=True)  # only two components

        # do factor ranking on sobol results
        sobol_factor_ranking_array = vars_funcs.factor_ranking(self.st)
        # turn results into data frame
        self.st_factor_ranking = pd.DataFrame(data=[sobol_factor_ranking_array], columns=self.parameters.keys(),
                                              index=[''])
        if self.report_verbose:
            factor_rank_pbar.update(1)

        # do factor ranking on IVARS results
        ivars_factor_ranking_list = []
        for scale in self.ivars_scales:
            ivars_factor_ranking_list.append(vars_funcs.factor_ranking(self.ivars.loc[scale]))
        # turn results into data frame
        self.ivars_factor_ranking = pd.DataFrame(data=ivars_factor_ranking_list, columns=self.parameters.keys(),
                                                 index=self.ivars_scales)
        if self.report_verbose:
            factor_rank_pbar.update(1)
            factor_rank_pbar.close()

        if self.bootstrap_flag and self.grouping_flag:
            self.gammalb, self.gammaub, self.maeelb, self.maeeub, self.stlb, self.stub, self.ivarslb, self.ivarsub, \
            self.rel_st_factor_ranking, self.rel_ivars_factor_ranking, self.ivars50_grp, self.st_grp, \
            self.reli_st_grp, self.reli_ivars50_grp = vars_funcs.bootstrapping(self.num_stars, self.pair_df, self.model_df, self.cov_section_all,
                                                                               self.bootstrap_size, self.bootstrap_ci,
                                                                               self.delta_h,
                                                                               self.ivars_scales,
                                                                               self.parameters, self.st_factor_ranking,
                                                                               self.ivars_factor_ranking,
                                                                               self.grouping_flag,
                                                                               self.num_grps, self.report_verbose)
        elif self.bootstrap_flag:
            self.gammalb, self.gammaub, self.maeelb, self.maeeub, self.stlb, self.stub, self.ivarslb, self.ivarsub, \
            self.rel_st_factor_ranking, self.rel_ivars_factor_ranking = vars_funcs.bootstrapping(self.num_stars, self.pair_df, self.model_df,
                                                                                                 self.cov_section_all,
                                                                                                 self.bootstrap_size,
                                                                                                 self.bootstrap_ci,
                                                                                                 self.delta_h,
                                                                                                 self.ivars_scales,
                                                                                                 self.parameters,
                                                                                                 self.st_factor_ranking,
                                                                                                 self.ivars_factor_ranking,
                                                                                                 self.grouping_flag,
                                                                                                 self.num_grps,
                                                                                                 self.report_verbose)


        # for status update
        self.run_status = True

        # output dictionary
        self.output = {
            'Gamma': self.gamma,
            'ST': self.st,
            'MAEE': self.maee,
            'MEE': self.mee,
            'COV': self.cov,
            'ECOV': self.ecov,
            'IVARS': self.ivars,
            'IVARSid': self.ivars_scales,
            'rnkST': self.st_factor_ranking,
            'rnkIVARS': self.ivars_factor_ranking,
            'Gammalb': self.gammalb if self.bootstrap_flag is True else None,
            'Gammaub': self.gammaub if self.bootstrap_flag is True else None,
            'MAEElb': self.maeelb if self.bootstrap_flag is True else None,
            'MAEEub': self.maeeub if self.bootstrap_flag is True else None,
            'STlb': self.stlb if self.bootstrap_flag is True else None,
            'STub': self.stub if self.bootstrap_flag is True else None,
            'IVARSlb': self.ivarslb if self.bootstrap_flag is True else None,
            'IVARSub': self.ivarsub if self.bootstrap_flag is True else None,
            'relST': self.rel_st_factor_ranking if self.bootstrap_flag is True else None,
            'relIVARS': self.rel_ivars_factor_ranking if self.bootstrap_flag is True else None,
            'Groups': [self.ivars50_grp, self.st_grp] if ((self.grouping_flag is True) and (self.bootstrap_flag is True)) else None,
            'relGrp': [self.reli_st_grp, self.reli_ivars50_grp] if ((self.grouping_flag is True) and (self.bootstrap_flag is True)) else None,
        }

        return

    def run_offline(self, model_df):
        """
        runs offline version of GVARS program

        Parameters
        ----------
        model_df : array_like
            A Pandas Dataframe that contains model ran on generated stars
        """

        # assign dataframe with model ran on it to class attribute
        self.model_df = model_df

        # get paired values for each section based on 'h' - considering the progress bar if report_verbose is True
        if self.report_verbose:
            tqdm.pandas(desc='building pairs', dynamic_ncols=True)
            self.pair_df = self.model_df.iloc[:, -1].groupby(level=[0, 1]).progress_apply(vars_funcs.section_df,
                                                                                               delta_h=self.delta_h)
        else:
            self.pair_df = self.model_df.iloc[:, -1].groupby(level=[0, 1]).apply(vars_funcs.section_df,
                                                                                      delta_h=self.delta_h)
        self.pair_df.index.names = ['centre', 'param', 'h', 'pair_ind']

        # get rid of irrelevant h values
        self.pair_df = self.pair_df.droplevel('h')

        # bin and reorder pairs according to actual 'h' values
        xmin, xmax = gvars_funcs.find_boundaries(self.parameters, self.dist_sample_file)
        self.pair_df = gvars_funcs.reorder_pairs(self.pair_df, self.num_stars, self.parameters, self.model_df,
                                                 self.delta_h, self.report_verbose, xmax, xmin, True)
        # include a column containing the dissimilarity between pairs
        self.pair_df['dissimilarity'] = 0.5 * (self.pair_df[0] - self.pair_df[1]).pow(2)

        # progress bar for vars analysis
        if self.report_verbose:
            vars_pbar = tqdm(desc='GVARS analysis', total=10, dynamic_ncols=True)  # 10 steps for different components

        # get mu_star value
        self.mu_star_df = self.model_df.iloc[:, -1].groupby(level=[0, 1]).mean()
        self.mu_star_df.index.names = ['centre', 'param']
        if self.report_verbose:
            vars_pbar.update(1)
            # vars_pbar.write('Averages of function evaluations (`mu_star`) calculated - access via .mu_star_df')

        # overall mean of the unique evaluated function value over all star points
        self.mu_overall = self.model_df.iloc[:, -1].unique().mean()
        if self.report_verbose:
            vars_pbar.update(1)
            # vars_pbar.write('Overall expected value of function evaluations (`mu_overall`) calculated - access via .mu_overall')

        # overall variance of the unique evaluated function over all star points
        self.var_overall = np.nanvar(self.model_df.iloc[:, -1].unique(),ddof=1)
        if self.report_verbose:
            vars_pbar.update(1)
            # vars_pbar.write('Overall variance of function evaluations (`var_overall`) calculated - access via .var_overall')

        # sectional covariogram calculation
        self.cov_section_all = vars_funcs.cov_section(self.pair_df, self.mu_star_df)
        if self.report_verbose:
            vars_pbar.update(1)
            # vars_pbar.write('Sectional covariogram `cov_section_all` calculated - access via .cov_section_all')

        # variogram calculation
        # MATLAB: Gamma
        self.gamma = vars_funcs.variogram(self.pair_df)
        if self.report_verbose:
            vars_pbar.update(1)
            # vars_pbar.write('Variogram (`gamma`) calculated - access via .gamma')

        # morris calculation
        morris_value = vars_funcs.morris_eq(self.pair_df)
        self.maee = morris_value[0]  # MATLAB: MAEE
        self.mee = morris_value[1]  # MATLAB: MEE
        if self.report_verbose:
            vars_pbar.update(1)
            # vars_pbar.write('Morris MAEE and MEE (`maee` and `mee`) calculated - access via .maee and .mee')

        # overall covariogram calculation
        # MATLAB: COV
        self.cov = vars_funcs.covariogram(self.pair_df, self.mu_overall)
        if self.report_verbose:
            vars_pbar.update(1)
            # vars_pbar.write('Covariogram (`cov`) calculated - access via .cov')

        # expected value of the overall covariogram calculation
        # MATLAB: ECOV
        self.ecov = vars_funcs.e_covariogram(self.cov_section_all)
        if self.report_verbose:
            vars_pbar.update(1)
            # vars_pbar.write('Expected value of covariogram (`ecov`) calculated - access via .ecov')

        # sobol calculation
        # MATLAB: ST
        self.st = vars_funcs.sobol_eq(self.gamma, self.ecov, self.var_overall, self.delta_h)
        if self.report_verbose:
            vars_pbar.update(1)
            # vars_pbar.write('Sobol ST (`st`) calculated - access via .st')

        # IVARS calculation
        self.ivars = pd.DataFrame.from_dict(
            {scale: self.gamma.groupby(level=0).apply(vars_funcs.ivars, scale=scale, delta_h=self.delta_h) \
             for scale in self.ivars_scales}, 'index')
        if self.report_verbose:
            vars_pbar.update(1)
            vars_pbar.close()

        # progress bar for factor ranking
        if self.report_verbose:
            factor_rank_pbar = tqdm(desc='factor ranking', total=2, dynamic_ncols=True)  # only two components

        # do factor ranking on sobol results
        sobol_factor_ranking_array = vars_funcs.factor_ranking(self.st)
        # turn results into data frame
        self.st_factor_ranking = pd.DataFrame(data=[sobol_factor_ranking_array], columns=self.parameters.keys(),
                                              index=[''])
        if self.report_verbose:
            factor_rank_pbar.update(1)

        # do factor ranking on IVARS results
        ivars_factor_ranking_list = []
        for scale in self.ivars_scales:
            ivars_factor_ranking_list.append(vars_funcs.factor_ranking(self.ivars.loc[scale]))
        # turn results into data frame
        self.ivars_factor_ranking = pd.DataFrame(data=ivars_factor_ranking_list, columns=self.parameters.keys(),
                                                 index=self.ivars_scales)
        if self.report_verbose:
            factor_rank_pbar.update(1)
            factor_rank_pbar.close()

        if self.bootstrap_flag and self.grouping_flag:
            self.gammalb, self.gammaub, self.maeelb, self.maeeub, self.stlb, self.stub, self.ivarslb, self.ivarsub, \
            self.rel_st_factor_ranking, self.rel_ivars_factor_ranking, self.ivars50_grp, self.st_grp, \
            self.reli_st_grp, self.reli_ivars50_grp = vars_funcs.bootstrapping(self.num_stars, self.pair_df, self.model_df,
                                                                               self.cov_section_all,
                                                                               self.bootstrap_size, self.bootstrap_ci,
                                                                               self.delta_h,
                                                                               self.ivars_scales,
                                                                               self.parameters, self.st_factor_ranking,
                                                                               self.ivars_factor_ranking,
                                                                               self.grouping_flag,
                                                                               self.num_grps, self.report_verbose)
        elif self.bootstrap_flag:
            self.gammalb, self.gammaub, self.maeelb, self.maeeub, self.stlb, self.stub, self.ivarslb, self.ivarsub, \
            self.rel_st_factor_ranking, self.rel_ivars_factor_ranking = vars_funcs.bootstrapping(self.num_stars, self.pair_df,
                                                                                                 self.model_df,
                                                                                                 self.cov_section_all,
                                                                                                 self.bootstrap_size,
                                                                                                 self.bootstrap_ci,
                                                                                                 self.delta_h,
                                                                                                 self.ivars_scales,
                                                                                                 self.parameters,
                                                                                                 self.st_factor_ranking,
                                                                                                 self.ivars_factor_ranking,
                                                                                                 self.grouping_flag,
                                                                                                 self.num_grps,
                                                                                                 self.report_verbose)


        # for status update
        self.run_status = True

        # output dictionary
        self.output = {
            'Gamma': self.gamma,
            'ST': self.st,
            'MAEE': self.maee,
            'MEE': self.mee,
            'COV': self.cov,
            'ECOV': self.ecov,
            'IVARS': self.ivars,
            'IVARSid': self.ivars_scales,
            'rnkST': self.st_factor_ranking,
            'rnkIVARS': self.ivars_factor_ranking,
            'Gammalb': self.gammalb if self.bootstrap_flag is True else None,
            'Gammaub': self.gammaub if self.bootstrap_flag is True else None,
            'MAEElb': self.maeelb if self.bootstrap_flag is True else None,
            'MAEEub': self.maeeub if self.bootstrap_flag is True else None,
            'STlb': self.stlb if self.bootstrap_flag is True else None,
            'STub': self.stub if self.bootstrap_flag is True else None,
            'IVARSlb': self.ivarslb if self.bootstrap_flag is True else None,
            'IVARSub': self.ivarsub if self.bootstrap_flag is True else None,
            'relST': self.rel_st_factor_ranking if self.bootstrap_flag is True else None,
            'relIVARS': self.rel_ivars_factor_ranking if self.bootstrap_flag is True else None,
            'Groups': [self.ivars50_grp, self.st_grp] if ((self.grouping_flag is True) and (self.bootstrap_flag is True)) else None,
            'relGrp': [self.reli_st_grp, self.reli_ivars50_grp] if ((self.grouping_flag is True) and (self.bootstrap_flag is True)) else None,
        }

        return


class TSVARS(VARS):
    """ Time-series version of VARS

    """

    def __init__(
        self, #itself
        star_centres = np.array([]),  # sampled star centres (random numbers) used to create star points
        num_stars: int = 100, # default number of stars
        parameters: Dict[Union[str, int], Tuple[float, float]] = {}, # name and bounds
        delta_h: Optional[float] = 0.1, # delta_h for star sampling
        ivars_scales: Optional[Tuple[float, ...]] = (0.1, 0.3, 0.5), # ivars scales
        model: Model = None, # model (function) to run for each star point
        seed: Optional[int] = np.random.randint(1, 123456789), # randomization state
        sampler: Optional[str] = None, # one of the default random samplers of varstool
        slice_size: Optional[int] = None,  # slice size for when using "plhs" sampling
        bootstrap_flag: Optional[bool] = False, # bootstrapping flag
        bootstrap_size: Optional[int]  = 1000, # bootstrapping size
        bootstrap_ci: Optional[int] = 0.9, # bootstrap confidence interval
        grouping_flag: Optional[bool] = False, # grouping flag
        num_grps: Optional[int] = None, # number of groups
        report_verbose: Optional[bool] = False, # reporting verbose
        func_eval_method: Optional[str] = 'serial', # the method to evaluate the model or function
        vars_eval_method: Optional[str] = 'serial', # the method to make pair_df dataframe
        vars_chunk_size: Optional[int] = None, # the chunk size to make pair_dfs to save memory
    ) -> None:

        super().__init__(
            star_centres=star_centres,
            num_stars=num_stars,
            parameters=parameters,
            delta_h=delta_h,
            ivars_scales=ivars_scales,
            model=model,
            seed=seed,
            sampler=sampler,
            slice_size=slice_size,
            bootstrap_flag=bootstrap_flag,
            bootstrap_size=bootstrap_size,
            bootstrap_ci=bootstrap_ci,
            grouping_flag=grouping_flag,
            num_grps=num_grps,
            report_verbose=report_verbose,
        ) # main instance variables are just the same as VARS

        # defining the TSVARS specific instance variables
        self.func_eval_method = func_eval_method
        self.vars_eval_method = vars_eval_method
        self.vars_chunk_size = vars_chunk_size

        # writing some errors that might happen here
        if self.vars_eval_method not in ('serial', 'parallel'):
            raise ValueError(
                "`vars_eval_method` must be either 'parallel' or 'serial'"
            )

        if self.func_eval_method not in ('serial', 'parallel'):
            raise ValueError(
                "`func_eval_method` must be either 'parallel' or 'serial'"
            )


    #-------------------------------------------
    # Representators
    def __repr__(self) -> str:
        """method shows the status of VARS analysis"""

        status_star_centres = "Star Centres: " + ("Loaded" if len(self.star_centres) != 0 else "Not Loaded")
        status_star_points = "Star Points: " + ("Loaded" if len(self.star_points) != 0 else "Not Loaded")
        status_parameters = "Parameters: " + (str(len(self.parameters))+" paremeters set" if self.parameters else "None")
        status_delta_h = "Delta h: " + (str(self.delta_h)+"" if self.delta_h else "None")
        status_model = "Model: " + (str(self.model)+"" if self.model else "None")
        status_seed = "Seed Number: " + (str(self.seed)+"" if self.seed else "None")
        status_bstrap = "Bootstrap: " + ("On" if self.bootstrap_flag else "Off")
        status_bstrap_size = "Bootstrap Size: " + (str(self.bootstrap_size)+"" if self.bootstrap_flag else "N/A")
        status_bstrap_ci = "Bootstrap CI: " + (str(self.bootstrap_ci)+"" if self.bootstrap_flag else "N/A")
        status_grouping = "Grouping: " + ("On" if self.grouping_flag else "Off")
        status_num_grps = "Number of Groups: " + (str(self.num_grps)+"" if self.num_grps else "None")
        status_func_eval_method = "Function Evaluation Method: " + self.func_eval_method
        status_vars_eval_method = "TSVARS Evaluation Method: " + self.vars_eval_method
        status_vars_chunk_size  = "TSVARS Chunk Size: " + (str(self.vars_chunk_size) if self.vars_chunk_size else "N/A")

        status_verbose  = "Verbose: " + ("On" if self.report_verbose else "Off")
        status_analysis = "TSVARS Analysis: " + ("Done" if self.run_status else "Not Done")

        status_report_list = [
                                status_star_centres, status_star_points, status_parameters, \
                                status_delta_h, status_model, status_seed, status_bstrap, \
                                status_bstrap_size, status_bstrap_ci, status_grouping, \
                                status_num_grps, status_func_eval_method, status_vars_eval_method, \
                                status_vars_chunk_size, status_verbose, status_analysis
                            ]

        return "\n".join(status_report_list) # join lines together and show them all


    def __str__(self) -> str:

        return self.__class__.__name__


    #-------------------------------------------
    # Core functions

    def generate_star(self) -> pd.DataFrame:
        """
        Generate TSVARS star points

        Returns
        -------
        star_points : pd.DataFrame
            dataframe containing star points
        """
        self.star_points = starvars.star(self.star_centres, # star centres
                                           delta_h=self.delta_h, # delta_h
                                           parameters=[*self.parameters], # parameters dictionary keys
                                           rettype='DataFrame',
                                       ) # return type must be a dataframe
        self.star_points.columns = [*self.parameters]

        self.star_points = tsvars_funcs.scale(df=self.star_points, # star points must be scaled
                                             bounds={ # bounds are created while scaling
                                                 'lb':[val[0] for _, val in self.parameters.items()],
                                                 'ub':[val[1] for _, val in self.parameters.items()],
                                             }
                                        )

        self.star_points.index.names = ['centre', 'param', 'point']

        return self.star_points

    def run_online(self):
        """
        runs online version of TS-VARS
        """

        self.star_points = starvars.star(self.star_centres, # star centres
                                           delta_h=self.delta_h, # delta_h
                                           parameters=[*self.parameters], # parameters dictionary keys
                                           rettype='DataFrame',
                                       ) # return type must be a dataframe
        self.star_points.columns = [*self.parameters]

        self.star_points = tsvars_funcs.scale(df=self.star_points, # star points must be scaled
                                             bounds={ # bounds are created while scaling
                                                 'lb':[val[0] for _, val in self.parameters.items()],
                                                 'ub':[val[1] for _, val in self.parameters.items()],
                                             }
                                        )

        # doing function evaluations either on serial or parallel mode
        if self.func_eval_method == 'serial':
            if self.report_verbose:
                tqdm.pandas(desc='function evaluation', dynamic_ncols=True)
                self.star_points_eval = self.star_points.progress_apply(self.model, axis=1, result_type='expand')
            else:
                self.star_points_eval = self.star_points.apply(self.model, axis=1, result_type='expand')
            self.star_points_eval.index.names = ['centre', 'param', 'point']

        elif self.func_eval_method == 'parallel':
            warnings.warn(
                "Evaluating function in parallel mode is not stable yet. "
                "varstool currently uses `mapply` to parallelize function "
                "evaluations, see https://github.com/ddelange/mapply",
                UserWarning,
                stacklevel=1
            )

            #importing `mapply` inside this if clause to avoid unnecessary overhead
            import mapply
            import psutil

            mapply.init(
                n_workers=-1, # -1 indicates max_chunks_per_worker makes the decision on parallelization
                chunk_size=1, # 1 indicates max_chunks_per_worker makes the decision on parallelization
                max_chunks_per_worker=int(self.star_points.shape[0]//psutil.cpu_count(logical=False)),
                progressbar=True if self.report_verbose else False,
            )
            self.star_points_eval = self.star_points.mapply(self.model, axis=1, result_type='expand')
            self.star_points_eval.index.names = ['centre', 'param', 'point']

        # defining a lambda function to build pairs for each time-step
        ts_pair = lambda ts: ts.groupby(level=['centre', 'param']).apply(tsvars_funcs.section_df, self.delta_h)

        # VARS evaluations can be done in two modes: serial and parallel
        if self.vars_eval_method == 'serial':

            if self.vars_chunk_size:
                warnings.warn(
                    "Chunk size is only applicable in the parallel VARS analysis",
                    UserWarning,
                    stacklevel=1
                    )

            # pair_df is built serially - other functions are the same as parallel
            if self.report_verbose: # making a progress bar
                tqdm.pandas(desc='building pairs', dynamic_ncols=True)
                self.pair_df = self.star_points_eval.groupby(level=0, axis=1).progress_apply(ts_pair)
            else:
                self.pair_df = self.star_points_eval.groupby(level=0, axis=1).apply(ts_pair)
            self.pair_df.index.names = ['centre', 'param', 'h', 'pair_ind']
            self.pair_df.columns.names = ['ts', None]
            self.pair_df = self.pair_df.stack(level='ts').reorder_levels([-1,0,1,2,3]).sort_index()

            vars_pbar = tqdm(desc='TSVARS analysis', total=10, dynamic_ncols=True)
            self.mu_star_df = self.star_points_eval.groupby(level=['centre','param']).mean().stack().reorder_levels(order=[2,0,1]).sort_index()
            self.mu_star_df.index.names = ['ts', 'centre', 'param']
            if self.report_verbose:
                vars_pbar.update(1)

            self.mu_overall = self.star_points_eval.apply(lambda x: np.mean(list(np.unique(x))))
            if self.report_verbose:
                vars_pbar.update(1)

            self.var_overall = self.star_points_eval.apply(lambda x: np.nanvar(list(np.unique(x)), ddof=1))
            if self.report_verbose:
                vars_pbar.update(1)

            self.gamma = tsvars_funcs.variogram(self.pair_df)
            if self.report_verbose:
                vars_pbar.update(1)

            self.sec_covariogram = tsvars_funcs.cov_section(self.pair_df, self.mu_star_df)
            if self.report_verbose:
                vars_pbar.update(1)

            self.morris = tsvars_funcs.morris_eq(self.pair_df)
            self.maee = self.morris[0]
            self.mee  = self.morris[1]
            if self.report_verbose:
                vars_pbar.update(1)

            self.cov = tsvars_funcs.covariogram(self.pair_df, self.mu_overall)
            if self.report_verbose:
                vars_pbar.update(1)

            self.ecov = tsvars_funcs.e_covariogram(self.sec_covariogram)
            if self.report_verbose:
                vars_pbar.update(1)

            self.st = tsvars_funcs.sobol_eq(self.gamma, self.ecov, self.var_overall, self.delta_h)
            if self.report_verbose:
                vars_pbar.update(1)

            self.ivars = pd.DataFrame.from_dict({scale: self.gamma.groupby(level=['ts', 'param']).apply(tsvars_funcs.ivars, scale=scale, delta_h=self.delta_h) \
                  for scale in self.ivars_scales}, 'index').unstack()
            self.ivars.index.names = ['ts', 'param', 'h']
            if self.report_verbose:
                vars_pbar.update(1)
                vars_pbar.close()

            self.run_status = True


        elif self.vars_eval_method == 'parallel':

            if self.vars_chunk_size: # if chunk size is provided by the user

                self.pair_df = pd.DataFrame()
                self.sec_covariogram = pd.DataFrame()
                self.gamma = pd.DataFrame()
                self.mu_star_df = pd.DataFrame()
                self.mu_overall = pd.DataFrame()
                self.var_overall = pd.DataFrame()
                self.maee = pd.DataFrame()
                self.mee  = pd.DataFrame()
                self.cov = pd.DataFrame()
                self.ecov = pd.DataFrame()
                self.st = pd.DataFrame()
                self.ivars = pd.DataFrame()

                for chunk in trange(
                    int(self.star_points_eval.shape[1]//self.vars_chunk_size)+1,
                    desc='chunks',
                    dynamic_ncols=True,
                ): # total number of chunks

                    # make a chunk of the main df (result of func eval)
                    df_temp = self.star_points_eval.iloc[:, chunk*self.vars_chunk_size:min((chunk+1)*self.vars_chunk_size, self.star_points_eval.shape[1]-1)]

                    # make pairs for each chunk
                    temp_pair_df = self._applyParallel(self.star_points_eval.groupby(level=0, axis=1), ts_pair, self.report_verbose)
                    temp_pair_df.index.names = ['ts', 'centre', 'param', 'h', 'pair_ind']

                    if self.report_verbose:
                        vars_pbar = tqdm(desc='VARS analysis', total=10, dynamic_ncols=True)

                    self.pair_df = pd.concat([self.pair_df, temp_pair_df])

                    # mu star
                    temp_mu_star = df_temp.groupby(level=['centre','param']).mean().stack().reorder_levels(order=[2,0,1]).sort_index()
                    temp_mu_star.index.names = ['ts', 'centre', 'param']
                    if self.report_verbose:
                        vars_pbar.update(1)
                    self.mu_star_df = pd.concat([self.mu_star_df, temp_mu_star.to_frame()])

                    # mu overall
                    temp_mu_overall = df_temp.apply(lambda x: np.mean(list(np.unique(x))))
                    if self.report_verbose:
                        vars_pbar.update(1)
                    self.mu_overall = pd.concat([self.mu_overall, temp_mu_overall.to_frame()])

                    #var overall
                    temp_var_overall = df_temp.apply(lambda x: np.nanvar(list(np.unique(x)), ddof=1))
                    if self.report_verbose:
                        vars_pbar.update(1)
                    self.var_overall = pd.concat([self.var_overall, temp_var_overall.to_frame()])

                    #variogram
                    temp_gamma = tsvars_funcs.variogram(temp_pair_df)
                    if self.report_verbose:
                        vars_pbar.update(1)
                    self.gamma = pd.concat([self.gamma, temp_gamma.to_frame()])

                    #sectional variogram
                    temp_sec_covariogram = tsvars_funcs.cov_section(temp_pair_df, temp_mu_star)
                    if self.report_verbose:
                        vars_pbar.update(1)
                    self.sec_covariogram = pd.concat([self.sec_covariogram, temp_sec_covariogram.to_frame()])

                    #morris
                    temp_morris_values = tsvars_funcs.morris_eq(temp_pair_df)
                    temp_maee = temp_morris_values[0]
                    temp_mee  = temp_morris_values[1]
                    self.maee = pd.concat([self.maee, temp_maee.to_frame()])
                    self.mee = pd.concat([self.mee, temp_mee.to_frame()])
                    if self.report_verbose:
                        vars_pbar.update(1)

                    #covariogram
                    temp_covariogram = tsvars_funcs.covariogram(temp_pair_df, temp_mu_overall)
                    if self.report_verbose:
                        vars_pbar.update(1)
                    self.cov = pd.concat([self.cov, temp_covariogram.to_frame()])

                    #e_covariogram
                    temp_e_covariogram = tsvars_funcs.e_covariogram(temp_sec_covariogram)
                    if self.report_verbose:
                        vars_pbar.update(1)
                    self.ecov = pd.concat([self.ecov, temp_e_covariogram.to_frame()])

                    #sobol
                    temp_sobol_values = tsvars_funcs.sobol_eq(temp_gamma, temp_e_covariogram, temp_var_overall, self.delta_h)
                    if self.report_verbose:
                        vars_pbar.update(1)
                    self.st = pd.concat([self.st, temp_sobol_values.to_frame()])

                    #ivars
                    temp_ivars_values = pd.DataFrame.from_dict({scale: temp_gamma.groupby(level=['ts', 'param']).apply(tsvars_funcs.ivars, scale=scale, delta_h=self.delta_h) \
                      for scale in self.ivars_scales}, 'index').unstack()
                    if self.report_verbose:
                        vars_pbar.update(1)
                    temp_ivars_values.index.names = ['ts', 'param', 'h']
                    self.ivars = pd.concat([self.ivars, temp_ivars_values.to_frame()])

                    vars_pbar.close()

                    self.run_status = True

            else:
                # pair_df is built serially - other functions are the same as parallel
                self.pair_df = self._applyParallel(self.star_points_eval.groupby(level=0, axis=1), ts_pair, self.report_verbose)
                self.pair_df.index.names = ['ts', 'centre', 'param', 'h', 'pair_ind']

                if self.report_verbose:
                    vars_pbar = tqdm(desc='VARS analysis', total=10, dynamic_ncols=True)

                self.mu_star_df = self.star_points_eval.groupby(level=['centre','param']).mean().stack().reorder_levels(order=[2,0,1]).sort_index()
                self.mu_star_df.index.names = ['ts', 'centre', 'param']
                if self.report_verbose:
                    vars_pbar.update(1)

                self.mu_overall = self.star_points_eval.apply(lambda x: np.mean(list(np.unique(x))))
                if self.report_verbose:
                    vars_pbar.update(1)

                self.var_overall = self.star_points_eval.apply(lambda x: np.nanvar(list(np.unique(x)), ddof=1))
                if self.report_verbose:
                    vars_pbar.update(1)

                self.gamma = tsvars_funcs.variogram(self.pair_df)
                if self.report_verbose:
                    vars_pbar.update(1)

                self.sec_covariogram = tsvars_funcs.cov_section(self.pair_df, self.mu_star_df)
                if self.report_verbose:
                    vars_pbar.update(1)

                self.morris = tsvars_funcs.morris_eq(self.pair_df)
                self.maee = self.morris[0]
                self.mee  = self.morris[1]
                if self.report_verbose:
                    vars_pbar.update(1)

                self.cov = tsvars_funcs.covariogram(self.pair_df, self.mu_overall)
                if self.report_verbose:
                    vars_pbar.update(1)

                self.ecov = tsvars_funcs.e_covariogram(self.sec_covariogram)
                if self.report_verbose:
                    vars_pbar.update(1)

                self.st = tsvars_funcs.sobol_eq(self.gamma, self.ecov, self.var_overall, self.delta_h)
                if self.report_verbose:
                    vars_pbar.update(1)

                self.ivars = pd.DataFrame.from_dict({scale: self.gamma.groupby(level=['ts', 'param']).apply(tsvars_funcs.ivars, scale=scale, delta_h=self.delta_h) \
                      for scale in self.ivars_scales}, 'index').unstack()
                self.ivars.index.names = ['ts', 'param', 'h']
                if self.report_verbose:
                    vars_pbar.update(1)
                    vars_pbar.close()

                self.run_status = True

        # output dictionary
        self.output = {
            'Gamma':self.gamma,
            'ST': self.st,
            'MAEE':self.maee,
            'MEE':self.mee,
            'COV':self.cov,
            'ECOV':self.ecov,
            'IVARS':self.ivars,
            'IVARSid':self.ivars_scales,
            # 'rnkST':self.st_factor_ranking,
            # 'rnkIVARS':self.ivars_factor_ranking,
            # 'Gammalb':self.gammalb if self.bootstrap_flag is True else None,
            # 'Gammaub':self.gammaub if self.bootstrap_flag is True else None,
            # 'STlb':self.stlb if self.bootstrap_flag is True else None,
            # 'STub':self.stub if self.bootstrap_flag is True else None,
            # 'IVARSlb':self.ivarslb if self.bootstrap_flag is True else None,
            # 'IVARSub':self.ivarsub if self.bootstrap_flag is True else None,
            # 'relST':self.rel_st_factor_ranking if self.bootstrap_flag is True else None,
            # 'relIVARS':self.rel_ivars_factor_ranking if self.bootstrap_flag is True else None,
            # 'Groups': [self.ivars50_grp, self.st_grp] if self.grouping_flag is True else None,
            # 'relGrp': [self.reli_st_grp, self.reli_ivars50_grp] if self.grouping_flag is True else None,
        }

        # defining aggregated values
        self.gamma.aggregate = self.gamma.groupby(level=['param', 'h']).mean()
        self.st.aggregate = self.st.groupby(level=['param']).mean()
        self.maee.aggregate  = self.maee.groupby(level=['param', 'h']).mean()
        self.mee.aggregate   = self.mee.groupby(level=['param', 'h']).mean()
        self.cov.aggregate   = self.cov.groupby(level=['param', 'h']).mean()
        self.ecov.aggregate  = self.ecov.groupby(level=['param', 'h']).mean()
        self.ivars.aggregate = self.ivars.groupby(level=['param', 'h']).mean()

        # defining time normalized values
        self.gamma_normalized = self.gamma.unstack(level=1).div(self.gamma.unstack(level=1).sum(axis=1),
                                         axis=0).stack().swaplevel().reindex_like(self.gamma)
        self.st_normalized = self.st.unstack(level=1).div(self.st.unstack(level=1).sum(axis=1), axis=0).stack()
        self.maee_normalized = self.maee.unstack(level=1).div(self.maee.unstack(level=1).sum(axis=1),
                                        axis=0).stack().swaplevel().reindex_like(self.maee)
        self.mee_normalized = self.mee.unstack(level=1).div(self.mee.unstack(level=1).sum(axis=1), axis=0).stack().swaplevel().reindex_like(
            self.mee)
        self.cov_normalized = self.cov.unstack(level=1).div(self.cov.unstack(level=1).sum(axis=1), axis=0).stack().swaplevel().reindex_like(
            self.cov)
        self.ecov_normalized = self.ecov.unstack(level=1).div(self.ecov.unstack(level=1).sum(axis=1),
                                        axis=0).stack().swaplevel().reindex_like(self.ecov)
        self.ivars_normalized = self.ivars.unstack(level=1).div(self.ivars.unstack(level=1).sum(axis=1),
                                         axis=0).stack().swaplevel().reindex_like(self.ivars)

        # defining time normalized aggregate values
        self.gamma_normalized.aggregate = self.gamma_normalized.groupby(level=['param', 'h']).mean()
        self.st_normalized.aggregate = self.st_normalized.groupby(level=['param']).mean()
        self.maee_normalized.aggregate  = self.maee_normalized.groupby(level=['param', 'h']).mean()
        self.mee_normalized.aggregate   = self.mee_normalized.groupby(level=['param', 'h']).mean()
        self.cov_normalized.aggregate   = self.cov_normalized.groupby(level=['param', 'h']).mean()
        self.ecov_normalized.aggregate  = self.ecov_normalized.groupby(level=['param', 'h']).mean()
        self.ivars_normalized.aggregate = self.ivars_normalized.groupby(level=['param', 'h']).mean()


    def run_offline(self, star_points_eval, star_points: Optional = None):
        """
        runs the offline version of TSVARS program

        Parameters
        ----------
        star_points_eval: array_like
            A Pandas Dataframe that contains model ran on generated stars
        star_points: array_like
            A Pandas Dataframe that contains the generated stars
        """

        self.star_points_eval = star_points_eval

        if isinstance(star_points, pd.DataFrame):
            self.star_points = star_points
        # if star points isnt inputted and it is not currently in the system warn the user
        elif not isinstance(self.star_points, pd.DataFrame):
            warnings.warn(
                "You did not input any star points, please input them or program will crash.",
                UserWarning,
                stacklevel=1
            )


        # defining a lambda function to build pairs for each time-step
        ts_pair = lambda ts: ts.groupby(level=['centre', 'param']).apply(tsvars_funcs.section_df, self.delta_h)

        # VARS evaluations can be done in two modes: serial and parallel
        if self.vars_eval_method == 'serial':

            if self.vars_chunk_size:
                warnings.warn(
                    "Chunk size is only applicable in the parallel VARS analysis",
                    UserWarning,
                    stacklevel=1
                    )

            # pair_df is built serially - other functions are the same as parallel
            if self.report_verbose: # making a progress bar
                tqdm.pandas(desc='building pairs', dynamic_ncols=True)
                self.pair_df = self.star_points_eval.groupby(level=0, axis=1).progress_apply(ts_pair)
            else:
                self.pair_df = self.star_points_eval.groupby(level=0, axis=1).apply(ts_pair)
            self.pair_df.index.names = ['centre', 'param', 'h', 'pair_ind']
            self.pair_df.columns.names = ['ts', None]
            self.pair_df = self.pair_df.stack(level='ts').reorder_levels([-1,0,1,2,3]).sort_index()

            vars_pbar = tqdm(desc='TSVARS analysis', total=10, dynamic_ncols=True)
            self.mu_star_df = self.star_points_eval.groupby(level=['centre','param']).mean().stack().reorder_levels(order=[2,0,1]).sort_index()
            self.mu_star_df.index.names = ['ts', 'centre', 'param']
            if self.report_verbose:
                vars_pbar.update(1)

            self.mu_overall = self.star_points_eval.apply(lambda x: np.mean(list(np.unique(x))))
            if self.report_verbose:
                vars_pbar.update(1)

            self.var_overall = self.star_points_eval.apply(lambda x: np.nanvar(list(np.unique(x)), ddof=1))
            if self.report_verbose:
                vars_pbar.update(1)

            self.gamma = tsvars_funcs.variogram(self.pair_df)
            if self.report_verbose:
                vars_pbar.update(1)

            self.sec_covariogram = tsvars_funcs.cov_section(self.pair_df, self.mu_star_df)
            if self.report_verbose:
                vars_pbar.update(1)

            self.morris = tsvars_funcs.morris_eq(self.pair_df)
            self.maee = self.morris[0]
            self.mee  = self.morris[1]
            if self.report_verbose:
                vars_pbar.update(1)

            self.cov = tsvars_funcs.covariogram(self.pair_df, self.mu_overall)
            if self.report_verbose:
                vars_pbar.update(1)

            self.ecov = tsvars_funcs.e_covariogram(self.sec_covariogram)
            if self.report_verbose:
                vars_pbar.update(1)

            self.st = tsvars_funcs.sobol_eq(self.gamma, self.ecov, self.var_overall, self.delta_h)
            if self.report_verbose:
                vars_pbar.update(1)

            self.ivars = pd.DataFrame.from_dict({scale: self.gamma.groupby(level=['ts', 'param']).apply(tsvars_funcs.ivars, scale=scale, delta_h=self.delta_h) \
                  for scale in self.ivars_scales}, 'index').unstack()
            self.ivars.index.names = ['ts', 'param', 'h']
            if self.report_verbose:
                vars_pbar.update(1)
                vars_pbar.close()

            self.run_status = True


        elif self.vars_eval_method == 'parallel':

            if self.vars_chunk_size: # if chunk size is provided by the user

                self.pair_df = pd.DataFrame()
                self.sec_covariogram = pd.DataFrame()
                self.gamma = pd.DataFrame()
                self.mu_star_df = pd.DataFrame()
                self.mu_overall = pd.DataFrame()
                self.var_overall = pd.DataFrame()
                self.maee = pd.DataFrame()
                self.mee  = pd.DataFrame()
                self.cov = pd.DataFrame()
                self.ecov = pd.DataFrame()
                self.st = pd.DataFrame()
                self.ivars = pd.DataFrame()

                for chunk in trange(
                    int(self.star_points_eval.shape[1]//self.vars_chunk_size)+1,
                    desc='chunks',
                    dynamic_ncols=True,
                ): # total number of chunks

                    # make a chunk of the main df (result of func eval)
                    df_temp = self.star_points_eval.iloc[:, chunk*self.vars_chunk_size:min((chunk+1)*self.vars_chunk_size, self.star_points_eval.shape[1]-1)]

                    # make pairs for each chunk
                    temp_pair_df = self._applyParallel(self.star_points_eval.groupby(level=0, axis=1), ts_pair, self.report_verbose)
                    temp_pair_df.index.names = ['ts', 'centre', 'param', 'h', 'pair_ind']

                    if self.report_verbose:
                        vars_pbar = tqdm(desc='VARS analysis', total=10, dynamic_ncols=True)

                    self.pair_df = pd.concat([self.pair_df, temp_pair_df])

                    # mu star
                    temp_mu_star = df_temp.groupby(level=['centre','param']).mean().stack().reorder_levels(order=[2,0,1]).sort_index()
                    temp_mu_star.index.names = ['ts', 'centre', 'param']
                    if self.report_verbose:
                        vars_pbar.update(1)
                    self.mu_star_df = pd.concat([self.mu_star_df, temp_mu_star.to_frame()])

                    # mu overall
                    temp_mu_overall = df_temp.apply(lambda x: np.mean(list(np.unique(x))))
                    if self.report_verbose:
                        vars_pbar.update(1)
                    self.mu_overall = pd.concat([self.mu_overall, temp_mu_overall.to_frame()])

                    #var overall
                    temp_var_overall = df_temp.apply(lambda x: np.nanvar(list(np.unique(x)), ddof=1))
                    if self.report_verbose:
                        vars_pbar.update(1)
                    self.var_overall = pd.concat([self.var_overall, temp_var_overall.to_frame()])

                    #variogram
                    temp_gamma = tsvars_funcs.variogram(temp_pair_df)
                    if self.report_verbose:
                        vars_pbar.update(1)
                    self.gamma = pd.concat([self.gamma, temp_gamma.to_frame()])

                    #sectional variogram
                    temp_sec_covariogram = tsvars_funcs.cov_section(temp_pair_df, temp_mu_star)
                    if self.report_verbose:
                        vars_pbar.update(1)
                    self.sec_covariogram = pd.concat([self.sec_covariogram, temp_sec_covariogram.to_frame()])

                    #morris
                    temp_morris_values = tsvars_funcs.morris_eq(temp_pair_df)
                    temp_maee = temp_morris_values[0]
                    temp_mee  = temp_morris_values[1]
                    self.maee = pd.concat([self.maee, temp_maee.to_frame()])
                    self.mee = pd.concat([self.mee, temp_mee.to_frame()])
                    if self.report_verbose:
                        vars_pbar.update(1)

                    #covariogram
                    temp_covariogram = tsvars_funcs.covariogram(temp_pair_df, temp_mu_overall)
                    if self.report_verbose:
                        vars_pbar.update(1)
                    self.cov = pd.concat([self.cov, temp_covariogram.to_frame()])

                    #e_covariogram
                    temp_e_covariogram = tsvars_funcs.e_covariogram(temp_sec_covariogram)
                    if self.report_verbose:
                        vars_pbar.update(1)
                    self.ecov = pd.concat([self.ecov, temp_e_covariogram.to_frame()])

                    #sobol
                    temp_sobol_values = tsvars_funcs.sobol_eq(temp_gamma, temp_e_covariogram, temp_var_overall, self.delta_h)
                    if self.report_verbose:
                        vars_pbar.update(1)
                    self.st = pd.concat([self.st, temp_sobol_values.to_frame()])

                    #ivars
                    temp_ivars_values = pd.DataFrame.from_dict({scale: temp_gamma.groupby(level=['ts', 'param']).apply(tsvars_funcs.ivars, scale=scale, delta_h=self.delta_h) \
                      for scale in self.ivars_scales}, 'index').unstack()
                    if self.report_verbose:
                        vars_pbar.update(1)
                    temp_ivars_values.index.names = ['ts', 'param', 'h']
                    self.ivars = pd.concat([self.ivars, temp_ivars_values.to_frame()])

                    vars_pbar.close()

                    self.run_status = True

            else:
                # pair_df is built serially - other functions are the same as parallel
                self.pair_df = self._applyParallel(self.star_points_eval.groupby(level=0, axis=1), ts_pair, self.report_verbose)
                self.pair_df.index.names = ['ts', 'centre', 'param', 'h', 'pair_ind']

                if self.report_verbose:
                    vars_pbar = tqdm(desc='VARS analysis', total=10, dynamic_ncols=True)

                self.mu_star_df = self.star_points_eval.groupby(level=['centre','param']).mean().stack().reorder_levels(order=[2,0,1]).sort_index()
                self.mu_star_df.index.names = ['ts', 'centre', 'param']
                if self.report_verbose:
                    vars_pbar.update(1)

                self.mu_overall = self.star_points_eval.apply(lambda x: np.mean(list(np.unique(x))))
                if self.report_verbose:
                    vars_pbar.update(1)

                self.var_overall = self.star_points_eval.apply(lambda x: np.nanvar(list(np.unique(x)), ddof=1))
                if self.report_verbose:
                    vars_pbar.update(1)

                self.gamma = tsvars_funcs.variogram(self.pair_df)
                if self.report_verbose:
                    vars_pbar.update(1)

                self.sec_covariogram = tsvars_funcs.cov_section(self.pair_df, self.mu_star_df)
                if self.report_verbose:
                    vars_pbar.update(1)

                self.morris = tsvars_funcs.morris_eq(self.pair_df)
                self.maee = self.morris[0]
                self.mee  = self.morris[1]
                if self.report_verbose:
                    vars_pbar.update(1)

                self.cov = tsvars_funcs.covariogram(self.pair_df, self.mu_overall)
                if self.report_verbose:
                    vars_pbar.update(1)

                self.ecov = tsvars_funcs.e_covariogram(self.sec_covariogram)
                if self.report_verbose:
                    vars_pbar.update(1)

                self.st = tsvars_funcs.sobol_eq(self.gamma, self.ecov, self.var_overall, self.delta_h)
                if self.report_verbose:
                    vars_pbar.update(1)

                self.ivars = pd.DataFrame.from_dict({scale: self.gamma.groupby(level=['ts', 'param']).apply(tsvars_funcs.ivars, scale=scale, delta_h=self.delta_h) \
                      for scale in self.ivars_scales}, 'index').unstack()
                self.ivars.index.names = ['ts', 'param', 'h']
                if self.report_verbose:
                    vars_pbar.update(1)
                    vars_pbar.close()

                self.run_status = True

        # output dictionary
        self.output = {
            'Gamma':self.gamma,
            'ST': self.st,
            'MAEE':self.maee,
            'MEE':self.mee,
            'COV':self.cov,
            'ECOV':self.ecov,
            'IVARS':self.ivars,
            'IVARSid':self.ivars_scales,
            # 'rnkST':self.st_factor_ranking,
            # 'rnkIVARS':self.ivars_factor_ranking,
            # 'Gammalb':self.gammalb if self.bootstrap_flag is True else None,
            # 'Gammaub':self.gammaub if self.bootstrap_flag is True else None,
            # 'STlb':self.stlb if self.bootstrap_flag is True else None,
            # 'STub':self.stub if self.bootstrap_flag is True else None,
            # 'IVARSlb':self.ivarslb if self.bootstrap_flag is True else None,
            # 'IVARSub':self.ivarsub if self.bootstrap_flag is True else None,
            # 'relST':self.rel_st_factor_ranking if self.bootstrap_flag is True else None,
            # 'relIVARS':self.rel_ivars_factor_ranking if self.bootstrap_flag is True else None,
            # 'Groups': [self.ivars50_grp, self.st_grp] if self.grouping_flag is True else None,
            # 'relGrp': [self.reli_st_grp, self.reli_ivars50_grp] if self.grouping_flag is True else None,
        }

        # defining aggregated values
        self.gamma.aggregate = self.gamma.groupby(level=['param', 'h']).mean()
        self.st.aggregate = self.st.groupby(level=['param']).mean()
        self.maee.aggregate  = self.maee.groupby(level=['param', 'h']).mean()
        self.mee.aggregate   = self.mee.groupby(level=['param', 'h']).mean()
        self.cov.aggregate   = self.cov.groupby(level=['param', 'h']).mean()
        self.ecov.aggregate  = self.ecov.groupby(level=['param', 'h']).mean()
        self.ivars.aggregate = self.ivars.groupby(level=['param', 'h']).mean()

        # defining time normalized values
        self.gamma_normalized = self.gamma.unstack(level=1).div(self.gamma.unstack(level=1).sum(axis=1),
                                         axis=0).stack().swaplevel().reindex_like(self.gamma)
        self.st_normalized = self.st.unstack(level=1).div(self.st.unstack(level=1).sum(axis=1), axis=0).stack()
        self.maee_normalized = self.maee.unstack(level=1).div(self.maee.unstack(level=1).sum(axis=1),
                                        axis=0).stack().swaplevel().reindex_like(self.maee)
        self.mee_normalized = self.mee.unstack(level=1).div(self.mee.unstack(level=1).sum(axis=1), axis=0).stack().swaplevel().reindex_like(
            self.mee)
        self.cov_normalized = self.cov.unstack(level=1).div(self.cov.unstack(level=1).sum(axis=1), axis=0).stack().swaplevel().reindex_like(
            self.cov)
        self.ecov_normalized = self.ecov.unstack(level=1).div(self.ecov.unstack(level=1).sum(axis=1),
                                        axis=0).stack().swaplevel().reindex_like(self.ecov)
        self.ivars_normalized = self.ivars.unstack(level=1).div(self.ivars.unstack(level=1).sum(axis=1),
                                         axis=0).stack().swaplevel().reindex_like(self.ivars)

        # defining time normalized aggregate values
        self.gamma_normalized.aggregate = self.gamma_normalized.groupby(level=['param', 'h']).mean()
        self.st_normalized.aggregate = self.st_normalized.groupby(level=['param']).mean()
        self.maee_normalized.aggregate  = self.maee_normalized.groupby(level=['param', 'h']).mean()
        self.mee_normalized.aggregate   = self.mee_normalized.groupby(level=['param', 'h']).mean()
        self.cov_normalized.aggregate   = self.cov_normalized.groupby(level=['param', 'h']).mean()
        self.ecov_normalized.aggregate  = self.ecov_normalized.groupby(level=['param', 'h']).mean()
        self.ivars_normalized.aggregate = self.ivars_normalized.groupby(level=['param', 'h']).mean()

    @staticmethod
    def _applyParallel(
        dfGrouped: pd.DataFrame,
        func: Callable,
        progress: bool=False,
        ) -> pd.DataFrame:

        def _temp_func(func, name, group):
            return func(group), name

        @contextlib.contextmanager
        def _tqdm_joblib(tqdm_object):
            """
            Context manager to patch joblib to report into tqdm progress bar given as argument

            Source: https://stackoverflow.com/questions/24983493
                    /tracking-progress-of-joblib-parallel-execution
                    /58936697#58936697
            """
            class TqdmBatchCompletionCallback(joblib.parallel.BatchCompletionCallBack):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)

                def __call__(self, *args, **kwargs):
                    tqdm_object.update(n=self.batch_size)
                    return super().__call__(*args, **kwargs)

            old_batch_callback = joblib.parallel.BatchCompletionCallBack
            joblib.parallel.BatchCompletionCallBack = TqdmBatchCompletionCallback

            try:
                yield tqdm_object
            finally:
                joblib.parallel.BatchCompletionCallBack = old_batch_callback
                tqdm_object.close()

        if progress:
            with _tqdm_joblib(tqdm(desc="building pairs", total=len(dfGrouped), dynamic_ncols=True)) as progress_bar:
                retLst, top_index = zip(*Parallel(n_jobs=mp.cpu_count())\
                                            (delayed(_temp_func)(func, name, group)\
                                        for name, group in dfGrouped))
        else:
            retLst, top_index = zip(*Parallel(n_jobs=mp.cpu_count())\
                                            (delayed(_temp_func)(func, name, group)\
                                        for name, group in dfGrouped))

        return pd.concat(retLst, keys=top_index)


class TSGVARS(GVARS):
    """ Time-series version of GVARS

    """

    def __init__(
        self, #itself
        star_centres: np.ndarray = np.array([]),  # sampled star centres (random numbers) used to create star points
        num_stars: Optional[int] = 100,  # number of stars
        parameters: Dict[Union[str, int], Tuple[float, float]] = {},  # name and bounds
        delta_h: Optional[float] = 0.1,  # delta_h for star sampling
        ivars_scales: Optional[Tuple[float, ...]] = (0.1, 0.3, 0.5),  # ivars scales
        model: Model = None,  # model (function) to run for each star point
        seed: Optional[int] = np.random.randint(1, 123456789),  # randomization state
        sampler: Optional[str] = None,  # one of the default random samplers of varstool
        slice_size: Optional[int] = None,  # slice size for when using "plhs" sampling
        bootstrap_flag: Optional[bool] = False,  # bootstrapping flag
        bootstrap_size: Optional[int] = 1000,  # bootstrapping size
        bootstrap_ci: Optional[float] = 0.9,  # bootstrap confidence interval
        grouping_flag: Optional[bool] = False,  # grouping flag
        num_grps: Optional[int] = None,  # number of groups
        report_verbose: Optional[bool] = False,  # reporting verbose
        corr_mat: np.ndarray = np.array([]),  # correlation matrix
        num_dir_samples: int = 50,  # number of directional samples
        fictive_mat_flag: Optional[bool] = True, # set if corr_mat is to be used in place of fictive matrix
        dist_sample_file: Optional[str] = None, # file name containing distribution data
        func_eval_method: Optional[str] = 'serial', # the method to evaluate the model or function
        vars_eval_method: Optional[str] = 'serial', # the method to make pair_df dataframe
        vars_chunk_size: Optional[int] = None, # the chunk size to make pair_dfs to save memory
    ) -> None:

        super().__init__(
            star_centres=star_centres,
            num_stars=num_stars,
            parameters=parameters,
            delta_h=delta_h,
            ivars_scales=ivars_scales,
            model=model,
            seed=seed,
            sampler=sampler,
            slice_size=slice_size,
            bootstrap_flag=bootstrap_flag,
            bootstrap_size=bootstrap_size,
            bootstrap_ci=bootstrap_ci,
            grouping_flag=grouping_flag,
            num_grps=num_grps,
            report_verbose=report_verbose,
            corr_mat=corr_mat,
            num_dir_samples=num_dir_samples,
            fictive_mat_flag=fictive_mat_flag,
            dist_sample_file=dist_sample_file
        ) # main instance variables are just the same as GVARS

        # defining the TSGVARS specific instance variables
        self.func_eval_method = func_eval_method
        self.vars_eval_method = vars_eval_method
        self.vars_chunk_size = vars_chunk_size

        # writing some errors that might happen here
        if self.vars_eval_method not in ('serial', 'parallel'):
            raise ValueError(
                "`vars_eval_method` must be either 'parallel' or 'serial'"
            )

        if self.func_eval_method not in ('serial', 'parallel'):
            raise ValueError(
                "`func_eval_method` must be either 'parallel' or 'serial'"
            )


    #-------------------------------------------
    # Representators
    def __repr__(self) -> str:
        """method shows the status of VARS analysis"""

        status_star_centres = "Star Centres: " + ("Loaded" if len(self.star_centres) != 0 else "Not Loaded")
        status_star_points = "Star Points: " + ("Loaded" if len(self.star_points) != 0 else "Not Loaded")
        status_parameters = "Parameters: " + (str(len(self.parameters))+" paremeters set" if self.parameters else "None")
        status_delta_h = "Delta h: " + (str(self.delta_h)+"" if self.delta_h else "None")
        status_model = "Model: " + (str(self.model)+"" if self.model else "None")
        status_seed = "Seed Number: " + (str(self.seed)+"" if self.seed else "None")
        status_bstrap = "Bootstrap: " + ("On" if self.bootstrap_flag else "Off")
        status_bstrap_size = "Bootstrap Size: " + (str(self.bootstrap_size)+"" if self.bootstrap_flag else "N/A")
        status_bstrap_ci = "Bootstrap CI: " + (str(self.bootstrap_ci)+"" if self.bootstrap_flag else "N/A")
        status_grouping = "Grouping: " + ("On" if self.grouping_flag else "Off")
        status_num_grps = "Number of Groups: " + (str(self.num_grps)+"" if self.num_grps else "None")
        status_func_eval_method = "Function Evaluation Method: " + self.func_eval_method
        status_vars_eval_method = "TSVARS Evaluation Method: " + self.vars_eval_method
        status_vars_chunk_size  = "TSVARS Chunk Size: " + (str(self.vars_chunk_size) if self.vars_chunk_size else "N/A")

        status_verbose  = "Verbose: " + ("On" if self.report_verbose else "Off")
        status_analysis = "TSVARS Analysis: " + ("Done" if self.run_status else "Not Done")

        status_report_list = [
                                status_star_centres, status_star_points, status_parameters, \
                                status_delta_h, status_model, status_seed, status_bstrap, \
                                status_bstrap_size, status_bstrap_ci, status_grouping, \
                                status_num_grps, status_func_eval_method, status_vars_eval_method, \
                                status_vars_chunk_size, status_verbose, status_analysis
                            ]

        return "\n".join(status_report_list) # join lines together and show them all


    def __str__(self) -> str:

        return self.__class__.__name__


    #-------------------------------------------
    # Core functions

    def generate_star(self) -> pd.DataFrame:
        """
        Generate TSGVARS star points

        Returns
        -------
        star_points : pd.DataFrame
            dataframe containing star points
        """

        # generate g_star points
        self.star_points, self.star_centres, self.cov_mat = g_starvars.g_star(
            self.parameters,  # parameters
            self.star_centres, # star centres
            self.seed,  # seed
            self.sampler, # sample method if any
            self.slice_size, # slice size if using plhs
            self.num_stars,  # number of stars
            self.corr_mat,  # correlation matrix of parameters
            self.num_dir_samples,  # number of directional samples in star points
            self.num_factors,  # number of parameters
            self.report_verbose, # loading bar boolean value
            self.fictive_mat_flag,
            self.dist_sample_file
        )

        self.star_points.columns = self.parameters.keys()

        self.star_points.index.names = ['centre', 'param', 'point']

        return self.star_points

    def run_online(self):
        """
        runs online version of TS-GVARS
        """

        # generate g_star points
        self.star_points, self.star_centres, self.cov_mat = g_starvars.g_star(
            self.parameters,  # parameters
            self.star_centres, # star centres
            self.seed,  # seed
            self.sampler, # sample method if any
            self.slice_size, # slice size if using plhs
            self.num_stars,  # number of stars
            self.corr_mat,  # correlation matrix of parameters
            self.num_dir_samples,  # number of directional samples in star points
            self.num_factors,  # number of parameters
            self.report_verbose, # loading bar boolean value
            self.fictive_mat_flag,
            self.dist_sample_file
        )

        self.star_points.columns = self.parameters.keys()

        # doing function evaluations either on serial or parallel mode
        if self.func_eval_method == 'serial':
            if self.report_verbose:
                tqdm.pandas(desc='function evaluation', dynamic_ncols=True)
                self.star_points_eval = self.star_points.progress_apply(self.model, axis=1, result_type='expand')
            else:
                self.star_points_eval = self.star_points.apply(self.model, axis=1, result_type='expand')
            self.star_points_eval.index.names = ['centre', 'param', 'point']

        elif self.func_eval_method == 'parallel':
            warnings.warn(
                "Evaluating function in parallel mode is not stable yet. "
                "varstool currently uses `mapply` to parallelize function "
                "evaluations, see https://github.com/ddelange/mapply",
                UserWarning,
                stacklevel=1
            )

            #importing `mapply` inside this if clause to avoid unnecessary overhead
            import mapply
            import psutil

            mapply.init(
                n_workers=-1, # -1 indicates max_chunks_per_worker makes the decision on parallelization
                chunk_size=1, # 1 indicates max_chunks_per_worker makes the decision on parallelization
                max_chunks_per_worker=int(self.star_points.shape[0]//psutil.cpu_count(logical=False)),
                progressbar=True if self.report_verbose else False,
            )
            self.star_points_eval = self.star_points.mapply(self.model, axis=1, result_type='expand')
            self.star_points_eval.index.names = ['centre', 'param', 'point']

        # defining a lambda function to build pairs for each time-step
        ts_pair = lambda ts: ts.groupby(level=['centre', 'param']).apply(tsvars_funcs.section_df, self.delta_h)

        # VARS evaluations can be done in two modes: serial and parallel
        if self.vars_eval_method == 'serial':

            if self.vars_chunk_size:
                warnings.warn(
                    "Chunk size is only applicable in the parallel VARS analysis",
                    UserWarning,
                    stacklevel=1
                    )

            # pair_df is built serially - other functions are the same as parallel
            if self.report_verbose: # making a progress bar
                tqdm.pandas(desc='building pairs', dynamic_ncols=True)
                self.pair_df = self.star_points_eval.groupby(level=0, axis=1).progress_apply(ts_pair)
            else:
                self.pair_df = self.star_points_eval.groupby(level=0, axis=1).apply(ts_pair)
            self.pair_df.index.names = ['centre', 'param', 'h', 'pair_ind']
            self.pair_df.columns.names = ['ts', None]
            self.pair_df = self.pair_df.stack(level='ts').reorder_levels([-1,0,1,2,3]).sort_index()

            # get rid of irrelevant h values
            self.pair_df = self.pair_df.droplevel('h')

            # bin and reorder pairs according to actual 'h' values
            xmin, xmax = tsgvars_funcs.find_boundaries(self.parameters, self.dist_sample_file)

            # dataframe to hold new pairs
            new_pair_df = pd.DataFrame()

            # bin and reorder pairs at each time step and insert into new pair df
            binning_flag = True # used to ensure binning is calculated once
            binned_pairs = [] # contains the binned pairs in order
            dist_list = [] # contains actual 'h' values
            for date, new_df in self.pair_df.groupby(level=0):
                if binning_flag:
                    # get the binned pairs (only needs to be calculated once)
                    binned_pairs, dist_list = tsgvars_funcs.reorder_pairs(new_df.droplevel(0), self.num_stars, self.parameters, self.star_points,
                                                    self.delta_h, self.report_verbose, xmax, xmin)
                    binning_flag = False

                    if self.report_verbose:
                        ts_pbar = tqdm(desc='reordering pairs at each time step',
                                       total=len(self.pair_df.groupby(level=0)),
                                       dynamic_ncols=True)

                # drop the date for now
                new_df = new_df.droplevel(0)
                new_df['actual h'] = dist_list

                # re order pairs values according to the bins
                centres = new_df.index.get_level_values(0).to_numpy()
                params = new_df.index.get_level_values(1).to_numpy()
                bps = binned_pairs.index.to_numpy()
                new_index = pd.MultiIndex.from_arrays([centres, params, bps], names=['centre', 'param', 'pair_ind'])
                new_df = new_df.reindex(new_index)

                # add in new index h, according to bin ranges
                # ex.) h = 0.1 = [0-0.15], h = 0.2 = [0.15-0.25]
                h = list(binned_pairs.values)
                new_df['h'] = h

                # format data frame so that it works properly with variogram analsysis functions
                new_df.set_index('h', append=True, inplace=True)
                new_df.set_index('actual h', append=True, inplace=True)

                new_df = new_df.reorder_levels(['centre', 'param', 'h', 'actual h', 'pair_ind'])
                new_pair_df = pd.concat([new_pair_df, (pd.concat({date: new_df}, names=['ts']))])

                if self.report_verbose:
                    ts_pbar.update(1)

            if self.report_verbose:
                ts_pbar.close()

            # set new pair_df
            self.pair_df = new_pair_df

            # include a column containing the dissimilarity between pairs
            self.pair_df['dissimilarity'] = 0.5 * (self.pair_df[0] - self.pair_df[1]).pow(2)

            vars_pbar = tqdm(desc='TSGVARS analysis', total=10, dynamic_ncols=True)
            self.mu_star_df = self.star_points_eval.groupby(level=['centre','param']).mean().stack().reorder_levels(order=[2,0,1]).sort_index()
            self.mu_star_df.index.names = ['ts', 'centre', 'param']
            if self.report_verbose:
                vars_pbar.update(1)

            self.mu_overall = self.star_points_eval.apply(lambda x: np.mean(list(np.unique(x))))
            if self.report_verbose:
                vars_pbar.update(1)

            self.var_overall = self.star_points_eval.apply(lambda x: np.nanvar(list(np.unique(x)), ddof=1))
            if self.report_verbose:
                vars_pbar.update(1)

            self.gamma = tsvars_funcs.variogram(self.pair_df)
            if self.report_verbose:
                vars_pbar.update(1)

            self.sec_covariogram = tsvars_funcs.cov_section(self.pair_df, self.mu_star_df)
            if self.report_verbose:
                vars_pbar.update(1)

            self.morris = tsvars_funcs.morris_eq(self.pair_df)
            self.maee = self.morris[0]
            self.mee  = self.morris[1]
            if self.report_verbose:
                vars_pbar.update(1)

            self.cov = tsvars_funcs.covariogram(self.pair_df, self.mu_overall)
            if self.report_verbose:
                vars_pbar.update(1)

            self.ecov = tsvars_funcs.e_covariogram(self.sec_covariogram)
            if self.report_verbose:
                vars_pbar.update(1)

            self.st = tsvars_funcs.sobol_eq(self.gamma, self.ecov, self.var_overall, self.delta_h)
            if self.report_verbose:
                vars_pbar.update(1)

            self.ivars = pd.DataFrame.from_dict({scale: self.gamma.groupby(level=['ts', 'param']).apply(tsgvars_funcs.ivars, scale=scale, delta_h=self.delta_h) \
                  for scale in self.ivars_scales}, 'index').unstack()
            self.ivars.index.names = ['ts', 'param', 'h']
            if self.report_verbose:
                vars_pbar.update(1)
                vars_pbar.close()

            self.run_status = True


        elif self.vars_eval_method == 'parallel':

            if self.vars_chunk_size: # if chunk size is provided by the user

                self.pair_df = pd.DataFrame()
                self.sec_covariogram = pd.DataFrame()
                self.gamma = pd.DataFrame()
                self.mu_star_df = pd.DataFrame()
                self.mu_overall = pd.DataFrame()
                self.var_overall = pd.DataFrame()
                self.maee = pd.DataFrame()
                self.mee  = pd.DataFrame()
                self.cov = pd.DataFrame()
                self.ecov = pd.DataFrame()
                self.st = pd.DataFrame()
                self.ivars = pd.DataFrame()

                for chunk in trange(
                    int(self.star_points_eval.shape[1]//self.vars_chunk_size)+1,
                    desc='chunks',
                    dynamic_ncols=True,
                ): # total number of chunks

                    # make a chunk of the main df (result of func eval)
                    df_temp = self.star_points_eval.iloc[:, chunk*self.vars_chunk_size:min((chunk+1)*self.vars_chunk_size, self.star_points_eval.shape[1]-1)]

                    # make pairs for each chunk
                    temp_pair_df = self._applyParallel(self.star_points_eval.groupby(level=0, axis=1), ts_pair, self.report_verbose)
                    temp_pair_df.index.names = ['ts', 'centre', 'param', 'h', 'pair_ind']

                    # get rid of irrelevant h values
                    temp_pair_df = temp_pair_df.droplevel('h')

                    # bin and reorder pairs according to actual 'h' values
                    xmin, xmax = tsgvars_funcs.find_boundaries(self.parameters, self.dist_sample_file)

                    # dataframe to hold new pairs
                    new_pair_df = pd.DataFrame()

                    # bin and reorder pairs at each time step and insert into new pair df
                    binning_flag = True  # used to ensure binning is calculated once
                    binned_pairs = []  # contains the binned pairs in order
                    dist_list = []  # contains actual 'h' values
                    for date, new_df in self.pair_df.groupby(level=0):
                        if binning_flag:
                            # get the binned pairs (only needs to be calculated once)
                            binned_pairs, dist_list = tsgvars_funcs.reorder_pairs(new_df.droplevel(0), self.num_stars,
                                                                                  self.parameters, self.star_points,
                                                                                  self.delta_h, self.report_verbose,
                                                                                  xmax, xmin)
                            binning_flag = False

                            if self.report_verbose:
                                ts_pbar = tqdm(desc='reordering pairs at each time step',
                                               total=len(self.pair_df.groupby(level=0)),
                                               dynamic_ncols=True)

                        # drop the date for now
                        new_df = new_df.droplevel(0)
                        new_df['actual h'] = dist_list

                        # re order pairs values according to the bins
                        centres = new_df.index.get_level_values(0).to_numpy()
                        params = new_df.index.get_level_values(1).to_numpy()
                        bps = binned_pairs.index.to_numpy()
                        new_index = pd.MultiIndex.from_arrays([centres, params, bps],
                                                              names=['centre', 'param', 'pair_ind'])
                        new_df = new_df.reindex(new_index)

                        # add in new index h, according to bin ranges
                        # ex.) h = 0.1 = [0-0.15], h = 0.2 = [0.15-0.25]
                        h = list(binned_pairs.values)
                        new_df['h'] = h

                        # format data frame so that it works properly with variogram analsysis functions
                        new_df.set_index('h', append=True, inplace=True)
                        new_df.set_index('actual h', append=True, inplace=True)

                        new_df = new_df.reorder_levels(['centre', 'param', 'h', 'actual h', 'pair_ind'])
                        new_pair_df = pd.concat([new_pair_df, (pd.concat({date: new_df}, names=['ts']))])

                        if self.report_verbose:
                            ts_pbar.update(1)

                    if self.report_verbose:
                        ts_pbar.close()

                    # set new pair_df
                    temp_pair_df = new_pair_df

                    # include_a column containing the dissimilarity between pairs
                    temp_pair_df['dissimilarity'] = 0.5 * (self.pair_df[0] - self.pair_df[1]).pow(2)

                    if self.report_verbose:
                        vars_pbar = tqdm(desc='VARS analysis', total=10, dynamic_ncols=True)

                    self.pair_df = pd.concat([self.pair_df, temp_pair_df])

                    # mu star
                    temp_mu_star = df_temp.groupby(level=['centre','param']).mean().stack().reorder_levels(order=[2,0,1]).sort_index()
                    temp_mu_star.index.names = ['ts', 'centre', 'param']
                    if self.report_verbose:
                        vars_pbar.update(1)
                    self.mu_star_df = pd.concat([self.mu_star_df, temp_mu_star.to_frame()])

                    # mu overall
                    temp_mu_overall = df_temp.apply(lambda x: np.mean(list(np.unique(x))))
                    if self.report_verbose:
                        vars_pbar.update(1)
                    self.mu_overall = pd.concat([self.mu_overall, temp_mu_overall.to_frame()])

                    #var overall
                    temp_var_overall = df_temp.apply(lambda x: np.nanvar(list(np.unique(x)), ddof=1))
                    if self.report_verbose:
                        vars_pbar.update(1)
                    self.var_overall = pd.concat([self.var_overall, temp_var_overall.to_frame()])

                    #variogram
                    temp_gamma = tsvars_funcs.variogram(temp_pair_df)
                    if self.report_verbose:
                        vars_pbar.update(1)
                    self.gamma = pd.concat([self.gamma, temp_gamma.to_frame()])

                    #sectional variogram
                    temp_sec_covariogram = tsvars_funcs.cov_section(temp_pair_df, temp_mu_star)
                    if self.report_verbose:
                        vars_pbar.update(1)
                    self.sec_covariogram = pd.concat([self.sec_covariogram, temp_sec_covariogram.to_frame()])

                    #morris
                    temp_morris_values = tsvars_funcs.morris_eq(temp_pair_df)
                    temp_maee = temp_morris_values[0]
                    temp_mee  = temp_morris_values[1]
                    self.maee = pd.concat([self.maee, temp_maee.to_frame()])
                    self.mee = pd.concat([self.mee, temp_mee.to_frame()])
                    if self.report_verbose:
                        vars_pbar.update(1)

                    #covariogram
                    temp_covariogram = tsvars_funcs.covariogram(temp_pair_df, temp_mu_overall)
                    if self.report_verbose:
                        vars_pbar.update(1)
                    self.cov = pd.concat([self.cov, temp_covariogram.to_frame()])

                    #e_covariogram
                    temp_e_covariogram = tsvars_funcs.e_covariogram(temp_sec_covariogram)
                    if self.report_verbose:
                        vars_pbar.update(1)
                    self.ecov = pd.concat([self.ecov, temp_e_covariogram.to_frame()])

                    #sobol
                    temp_sobol_values = tsvars_funcs.sobol_eq(temp_gamma, temp_e_covariogram, temp_var_overall, self.delta_h)
                    if self.report_verbose:
                        vars_pbar.update(1)
                    self.st = pd.concat([self.st, temp_sobol_values.to_frame()])

                    #ivars
                    temp_ivars_values = pd.DataFrame.from_dict({scale: temp_gamma.groupby(level=['ts', 'param']).apply(tsgvars_funcs.ivars, scale=scale, delta_h=self.delta_h) \
                      for scale in self.ivars_scales}, 'index').unstack()
                    if self.report_verbose:
                        vars_pbar.update(1)
                    temp_ivars_values.index.names = ['ts', 'param', 'h']
                    self.ivars = pd.concat([self.ivars, temp_ivars_values.to_frame()])

                    vars_pbar.close()

                    self.run_status = True

            else:
                # pair_df is built serially - other functions are the same as parallel
                self.pair_df = self._applyParallel(self.star_points_eval.groupby(level=0, axis=1), ts_pair, self.report_verbose)
                self.pair_df.index.names = ['ts', 'centre', 'param', 'h', 'pair_ind']

                # get rid of irrelevant h values
                self.pair_df = self.pair_df.droplevel('h')

                # bin and reorder pairs according to actual 'h' values
                xmin, xmax = tsgvars_funcs.find_boundaries(self.parameters, self.dist_sample_file)

                # dataframe to hold new pairs
                new_pair_df = pd.DataFrame()

                # bin and reorder pairs at each time step and insert into new pair df
                binning_flag = True  # used to ensure binning is calculated once
                binned_pairs = []  # contains the binned pairs in order
                dist_list = []  # contains actual 'h' values
                for date, new_df in self.pair_df.groupby(level=0):
                    if binning_flag:
                        # get the binned pairs (only needs to be calculated once)
                        binned_pairs, dist_list = tsgvars_funcs.reorder_pairs(new_df.droplevel(0), self.num_stars,
                                                                              self.parameters, self.star_points,
                                                                              self.delta_h, self.report_verbose, xmax,
                                                                              xmin)
                        binning_flag = False

                        if self.report_verbose:
                            ts_pbar = tqdm(desc='reordering pairs at each time step',
                                           total=len(self.pair_df.groupby(level=0)),
                                           dynamic_ncols=True)

                    # drop the date for now
                    new_df = new_df.droplevel(0)
                    new_df['actual h'] = dist_list

                    # re order pairs values according to the bins
                    centres = new_df.index.get_level_values(0).to_numpy()
                    params = new_df.index.get_level_values(1).to_numpy()
                    bps = binned_pairs.index.to_numpy()
                    new_index = pd.MultiIndex.from_arrays([centres, params, bps], names=['centre', 'param', 'pair_ind'])
                    new_df = new_df.reindex(new_index)

                    # add in new index h, according to bin ranges
                    # ex.) h = 0.1 = [0-0.15], h = 0.2 = [0.15-0.25]
                    h = list(binned_pairs.values)
                    new_df['h'] = h

                    # format data frame so that it works properly with variogram analsysis functions
                    new_df.set_index('h', append=True, inplace=True)
                    new_df.set_index('actual h', append=True, inplace=True)

                    new_df = new_df.reorder_levels(['centre', 'param', 'h', 'actual h', 'pair_ind'])
                    new_pair_df = pd.concat([new_pair_df, (pd.concat({date: new_df}, names=['ts']))])

                    if self.report_verbose:
                        ts_pbar.update(1)

                if self.report_verbose:
                    ts_pbar.close()

                # set new pair_df
                self.pair_df = new_pair_df

                # include a column containing the dissimilarity between pairs
                self.pair_df['dissimilarity'] = 0.5 * (self.pair_df[0] - self.pair_df[1]).pow(2)

                if self.report_verbose:
                    vars_pbar = tqdm(desc='VARS analysis', total=10, dynamic_ncols=True)

                self.mu_star_df = self.star_points_eval.groupby(level=['centre','param']).mean().stack().reorder_levels(order=[2,0,1]).sort_index()
                self.mu_star_df.index.names = ['ts', 'centre', 'param']
                if self.report_verbose:
                    vars_pbar.update(1)

                self.mu_overall = self.star_points_eval.apply(lambda x: np.mean(list(np.unique(x))))
                if self.report_verbose:
                    vars_pbar.update(1)

                self.var_overall = self.star_points_eval.apply(lambda x: np.nanvar(list(np.unique(x)), ddof=1))
                if self.report_verbose:
                    vars_pbar.update(1)

                self.gamma = tsvars_funcs.variogram(self.pair_df)
                if self.report_verbose:
                    vars_pbar.update(1)

                self.sec_covariogram = tsvars_funcs.cov_section(self.pair_df, self.mu_star_df)
                if self.report_verbose:
                    vars_pbar.update(1)

                self.morris = tsvars_funcs.morris_eq(self.pair_df)
                self.maee = self.morris[0]
                self.mee  = self.morris[1]
                if self.report_verbose:
                    vars_pbar.update(1)

                self.cov = tsvars_funcs.covariogram(self.pair_df, self.mu_overall)
                if self.report_verbose:
                    vars_pbar.update(1)

                self.ecov = tsvars_funcs.e_covariogram(self.sec_covariogram)
                if self.report_verbose:
                    vars_pbar.update(1)

                self.st = tsvars_funcs.sobol_eq(self.gamma, self.ecov, self.var_overall, self.delta_h)
                if self.report_verbose:
                    vars_pbar.update(1)

                self.ivars = pd.DataFrame.from_dict({scale: self.gamma.groupby(level=['ts', 'param']).apply(tsgvars_funcs.ivars, scale=scale, delta_h=self.delta_h) \
                      for scale in self.ivars_scales}, 'index').unstack()
                self.ivars.index.names = ['ts', 'param', 'h']
                if self.report_verbose:
                    vars_pbar.update(1)
                    vars_pbar.close()

                self.run_status = True

        # output dictionary
        self.output = {
            'Gamma':self.gamma,
            'ST': self.st,
            'MAEE':self.maee,
            'MEE':self.mee,
            'COV':self.cov,
            'ECOV':self.ecov,
            'IVARS':self.ivars,
            'IVARSid':self.ivars_scales,
            # 'rnkST':self.st_factor_ranking,
            # 'rnkIVARS':self.ivars_factor_ranking,
            # 'Gammalb':self.gammalb if self.bootstrap_flag is True else None,
            # 'Gammaub':self.gammaub if self.bootstrap_flag is True else None,
            # 'STlb':self.stlb if self.bootstrap_flag is True else None,
            # 'STub':self.stub if self.bootstrap_flag is True else None,
            # 'IVARSlb':self.ivarslb if self.bootstrap_flag is True else None,
            # 'IVARSub':self.ivarsub if self.bootstrap_flag is True else None,
            # 'relST':self.rel_st_factor_ranking if self.bootstrap_flag is True else None,
            # 'relIVARS':self.rel_ivars_factor_ranking if self.bootstrap_flag is True else None,
            # 'Groups': [self.ivars50_grp, self.st_grp] if self.grouping_flag is True else None,
            # 'relGrp': [self.reli_st_grp, self.reli_ivars50_grp] if self.grouping_flag is True else None,
        }

        # defining aggregated values
        self.gamma.aggregate = self.gamma.groupby(level=['param', 'h']).mean()
        self.st.aggregate = self.st.groupby(level=['param']).mean()
        self.maee.aggregate  = self.maee.groupby(level=['param', 'h']).mean()
        self.mee.aggregate   = self.mee.groupby(level=['param', 'h']).mean()
        self.cov.aggregate   = self.cov.groupby(level=['param', 'h']).mean()
        self.ecov.aggregate  = self.ecov.groupby(level=['param', 'h']).mean()
        self.ivars.aggregate = self.ivars.groupby(level=['param', 'h']).mean()

        # defining time normalized values
        self.gamma_normalized = self.gamma.unstack(level=1).div(self.gamma.unstack(level=1).sum(axis=1),
                                         axis=0).stack().swaplevel().reindex_like(self.gamma)
        self.st_normalized = self.st.unstack(level=1).div(self.st.unstack(level=1).sum(axis=1), axis=0).stack()
        self.maee_normalized = self.maee.unstack(level=1).div(self.maee.unstack(level=1).sum(axis=1),
                                        axis=0).stack().swaplevel().reindex_like(self.maee)
        self.mee_normalized = self.mee.unstack(level=1).div(self.mee.unstack(level=1).sum(axis=1), axis=0).stack().swaplevel().reindex_like(
            self.mee)
        self.cov_normalized = self.cov.unstack(level=1).div(self.cov.unstack(level=1).sum(axis=1), axis=0).stack().swaplevel().reindex_like(
            self.cov)
        self.ecov_normalized = self.ecov.unstack(level=1).div(self.ecov.unstack(level=1).sum(axis=1),
                                        axis=0).stack().swaplevel().reindex_like(self.ecov)
        self.ivars_normalized = self.ivars.unstack(level=1).div(self.ivars.unstack(level=1).sum(axis=1),
                                         axis=0).stack().swaplevel().reindex_like(self.ivars)

        # defining time normalized aggregate values
        self.gamma_normalized.aggregate = self.gamma_normalized.groupby(level=['param', 'h']).mean()
        self.st_normalized.aggregate = self.st_normalized.groupby(level=['param']).mean()
        self.maee_normalized.aggregate  = self.maee_normalized.groupby(level=['param', 'h']).mean()
        self.mee_normalized.aggregate   = self.mee_normalized.groupby(level=['param', 'h']).mean()
        self.cov_normalized.aggregate   = self.cov_normalized.groupby(level=['param', 'h']).mean()
        self.ecov_normalized.aggregate  = self.ecov_normalized.groupby(level=['param', 'h']).mean()
        self.ivars_normalized.aggregate = self.ivars_normalized.groupby(level=['param', 'h']).mean()


    def run_offline(self, star_points_eval, star_points: Optional = None):
        """
        runs the offline version of TSGVARS program

        Parameters
        ----------
        star_points_eval: array_like
            A Pandas Dataframe that contains model ran on generated stars
        star_points: array_like
            A Pandas Dataframe that contains generated stars
        """

        self.star_points_eval = star_points_eval

        if isinstance(star_points, pd.DataFrame):
            self.star_points = star_points
        # if star points isnt inputted and it is not currently in the system warn the user
        elif not isinstance(self.star_points, pd.DataFrame):
            warnings.warn(
                "You did not input any star points, please input them or program will crash.",
                UserWarning,
                stacklevel=1
            )

        # defining a lambda function to build pairs for each time-step
        ts_pair = lambda ts: ts.groupby(level=['centre', 'param']).apply(tsvars_funcs.section_df, self.delta_h)

        # VARS evaluations can be done in two modes: serial and parallel
        if self.vars_eval_method == 'serial':

            if self.vars_chunk_size:
                warnings.warn(
                    "Chunk size is only applicable in the parallel VARS analysis",
                    UserWarning,
                    stacklevel=1
                    )

            # pair_df is built serially - other functions are the same as parallel
            if self.report_verbose: # making a progress bar
                tqdm.pandas(desc='building pairs', dynamic_ncols=True)
                self.pair_df = self.star_points_eval.groupby(level=0, axis=1).progress_apply(ts_pair)
            else:
                self.pair_df = self.star_points_eval.groupby(level=0, axis=1).apply(ts_pair)
            self.pair_df.index.names = ['centre', 'param', 'h', 'pair_ind']
            self.pair_df.columns.names = ['ts', None]
            self.pair_df = self.pair_df.stack(level='ts').reorder_levels([-1,0,1,2,3]).sort_index()

            # get rid of irrelevant h values
            self.pair_df = self.pair_df.droplevel('h')

            # bin and reorder pairs according to actual 'h' values
            xmin, xmax = tsgvars_funcs.find_boundaries(self.parameters, self.dist_sample_file)

            # dataframe to hold new pairs
            new_pair_df = pd.DataFrame()

            # bin and reorder pairs at each time step and insert into new pair df
            binning_flag = True  # used to ensure binning is calculated once
            binned_pairs = []  # contains the binned pairs in order
            dist_list = []  # contains actual 'h' values
            for date, new_df in self.pair_df.groupby(level=0):
                if binning_flag:
                    # get the binned pairs (only needs to be calculated once)
                    binned_pairs, dist_list = tsgvars_funcs.reorder_pairs(new_df.droplevel(0), self.num_stars,
                                                                          self.parameters, self.star_points,
                                                                          self.delta_h, self.report_verbose, xmax, xmin)
                    binning_flag = False

                    if self.report_verbose:
                        ts_pbar = tqdm(desc='reordering pairs at each time step',
                                       total=len(self.pair_df.groupby(level=0)),
                                       dynamic_ncols=True)

                # drop the date for now
                new_df = new_df.droplevel(0)
                new_df['actual h'] = dist_list

                # re order pairs values according to the bins
                centres = new_df.index.get_level_values(0).to_numpy()
                params = new_df.index.get_level_values(1).to_numpy()
                bps = binned_pairs.index.to_numpy()
                new_index = pd.MultiIndex.from_arrays([centres, params, bps], names=['centre', 'param', 'pair_ind'])
                new_df = new_df.reindex(new_index)

                # add in new index h, according to bin ranges
                # ex.) h = 0.1 = [0-0.15], h = 0.2 = [0.15-0.25]
                h = list(binned_pairs.values)
                new_df['h'] = h

                # format data frame so that it works properly with variogram analsysis functions
                new_df.set_index('h', append=True, inplace=True)
                new_df.set_index('actual h', append=True, inplace=True)

                new_df = new_df.reorder_levels(['centre', 'param', 'h', 'actual h', 'pair_ind'])
                new_pair_df = pd.concat([new_pair_df, (pd.concat({date: new_df}, names=['ts']))])

                if self.report_verbose:
                    ts_pbar.update(1)

            if self.report_verbose:
                ts_pbar.close()

            # set new pair_df
            self.pair_df = new_pair_df

            # include a column containing the dissimilarity between pairs
            self.pair_df['dissimilarity'] = 0.5 * (self.pair_df[0] - self.pair_df[1]).pow(2)

            vars_pbar = tqdm(desc='TSGVARS analysis', total=10, dynamic_ncols=True)
            self.mu_star_df = self.star_points_eval.groupby(level=['centre','param']).mean().stack().reorder_levels(order=[2,0,1]).sort_index()
            self.mu_star_df.index.names = ['ts', 'centre', 'param']
            if self.report_verbose:
                vars_pbar.update(1)

            self.mu_overall = self.star_points_eval.apply(lambda x: np.mean(list(np.unique(x))))
            if self.report_verbose:
                vars_pbar.update(1)

            self.var_overall = self.star_points_eval.apply(lambda x: np.nanvar(list(np.unique(x)), ddof=1))
            if self.report_verbose:
                vars_pbar.update(1)

            self.gamma = tsvars_funcs.variogram(self.pair_df)
            if self.report_verbose:
                vars_pbar.update(1)

            self.sec_covariogram = tsvars_funcs.cov_section(self.pair_df, self.mu_star_df)
            if self.report_verbose:
                vars_pbar.update(1)

            self.morris = tsvars_funcs.morris_eq(self.pair_df)
            self.maee = self.morris[0]
            self.mee  = self.morris[1]
            if self.report_verbose:
                vars_pbar.update(1)

            self.cov = tsvars_funcs.covariogram(self.pair_df, self.mu_overall)
            if self.report_verbose:
                vars_pbar.update(1)

            self.ecov = tsvars_funcs.e_covariogram(self.sec_covariogram)
            if self.report_verbose:
                vars_pbar.update(1)

            self.st = tsvars_funcs.sobol_eq(self.gamma, self.ecov, self.var_overall, self.delta_h)
            if self.report_verbose:
                vars_pbar.update(1)

            self.ivars = pd.DataFrame.from_dict({scale: self.gamma.groupby(level=['ts', 'param']).apply(tsgvars_funcs.ivars, scale=scale, delta_h=self.delta_h) \
                  for scale in self.ivars_scales}, 'index').unstack()
            self.ivars.index.names = ['ts', 'param', 'h']
            if self.report_verbose:
                vars_pbar.update(1)
                vars_pbar.close()

            self.run_status = True


        elif self.vars_eval_method == 'parallel':

            if self.vars_chunk_size: # if chunk size is provided by the user

                self.pair_df = pd.DataFrame()
                self.sec_covariogram = pd.DataFrame()
                self.gamma = pd.DataFrame()
                self.mu_star_df = pd.DataFrame()
                self.mu_overall = pd.DataFrame()
                self.var_overall = pd.DataFrame()
                self.maee = pd.DataFrame()
                self.mee  = pd.DataFrame()
                self.cov = pd.DataFrame()
                self.ecov = pd.DataFrame()
                self.st = pd.DataFrame()
                self.ivars = pd.DataFrame()

                for chunk in trange(
                    int(self.star_points_eval.shape[1]//self.vars_chunk_size)+1,
                    desc='chunks',
                    dynamic_ncols=True,
                ): # total number of chunks

                    # make a chunk of the main df (result of func eval)
                    df_temp = self.star_points_eval.iloc[:, chunk*self.vars_chunk_size:min((chunk+1)*self.vars_chunk_size, self.star_points_eval.shape[1]-1)]

                    # make pairs for each chunk
                    temp_pair_df = self._applyParallel(self.star_points_eval.groupby(level=0, axis=1), ts_pair, self.report_verbose)
                    temp_pair_df.index.names = ['ts', 'centre', 'param', 'h', 'pair_ind']

                    # get rid of irrelevant h values
                    temp_pair_df = temp_pair_df.droplevel('h')

                    # bin and reorder pairs according to actual 'h' values
                    xmin, xmax = tsgvars_funcs.find_boundaries(self.parameters, self.dist_sample_file)

                    # dataframe to hold new pairs
                    new_pair_df = pd.DataFrame()

                    # bin and reorder pairs at each time step and insert into new pair df
                    binning_flag = True  # used to ensure binning is calculated once
                    binned_pairs = []  # contains the binned pairs in order
                    dist_list = []  # contains actual 'h' values
                    for date, new_df in self.pair_df.groupby(level=0):
                        if binning_flag:
                            # get the binned pairs (only needs to be calculated once)
                            binned_pairs, dist_list = tsgvars_funcs.reorder_pairs(new_df.droplevel(0), self.num_stars,
                                                                                  self.parameters, self.star_points,
                                                                                  self.delta_h, self.report_verbose,
                                                                                  xmax, xmin)
                            binning_flag = False

                            if self.report_verbose:
                                ts_pbar = tqdm(desc='reordering pairs at each time step',
                                               total=len(self.pair_df.groupby(level=0)),
                                               dynamic_ncols=True)

                        # drop the date for now
                        new_df = new_df.droplevel(0)
                        new_df['actual h'] = dist_list

                        # re order pairs values according to the bins
                        centres = new_df.index.get_level_values(0).to_numpy()
                        params = new_df.index.get_level_values(1).to_numpy()
                        bps = binned_pairs.index.to_numpy()
                        new_index = pd.MultiIndex.from_arrays([centres, params, bps],
                                                              names=['centre', 'param', 'pair_ind'])
                        new_df = new_df.reindex(new_index)

                        # add in new index h, according to bin ranges
                        # ex.) h = 0.1 = [0-0.15], h = 0.2 = [0.15-0.25]
                        h = list(binned_pairs.values)
                        new_df['h'] = h

                        # format data frame so that it works properly with variogram analsysis functions
                        new_df.set_index('h', append=True, inplace=True)
                        new_df.set_index('actual h', append=True, inplace=True)

                        new_df = new_df.reorder_levels(['centre', 'param', 'h', 'actual h', 'pair_ind'])
                        new_pair_df = pd.concat([new_pair_df, (pd.concat({date: new_df}, names=['ts']))])

                        if self.report_verbose:
                            ts_pbar.update(1)

                    if self.report_verbose:
                        ts_pbar.close()

                    # set new pair_df
                    temp_pair_df = new_pair_df

                    # include_a column containing the dissimilarity between pairs
                    temp_pair_df['dissimilarity'] = 0.5 * (self.pair_df[0] - self.pair_df[1]).pow(2)


                    if self.report_verbose:
                        vars_pbar = tqdm(desc='VARS analysis', total=10, dynamic_ncols=True)

                    self.pair_df = pd.concat([self.pair_df, temp_pair_df])

                    # mu star
                    temp_mu_star = df_temp.groupby(level=['centre','param']).mean().stack().reorder_levels(order=[2,0,1]).sort_index()
                    temp_mu_star.index.names = ['ts', 'centre', 'param']
                    if self.report_verbose:
                        vars_pbar.update(1)
                    self.mu_star_df = pd.concat([self.mu_star_df, temp_mu_star.to_frame()])

                    # mu overall
                    temp_mu_overall = df_temp.apply(lambda x: np.mean(list(np.unique(x))))
                    if self.report_verbose:
                        vars_pbar.update(1)
                    self.mu_overall = pd.concat([self.mu_overall, temp_mu_overall.to_frame()])

                    #var overall
                    temp_var_overall = df_temp.apply(lambda x: np.nanvar(list(np.unique(x)), ddof=1))
                    if self.report_verbose:
                        vars_pbar.update(1)
                    self.var_overall = pd.concat([self.var_overall, temp_var_overall.to_frame()])

                    #variogram
                    temp_gamma = tsvars_funcs.variogram(temp_pair_df)
                    if self.report_verbose:
                        vars_pbar.update(1)
                    self.gamma = pd.concat([self.gamma, temp_gamma.to_frame()])

                    #sectional variogram
                    temp_sec_covariogram = tsvars_funcs.cov_section(temp_pair_df, temp_mu_star)
                    if self.report_verbose:
                        vars_pbar.update(1)
                    self.sec_covariogram = pd.concat([self.sec_covariogram, temp_sec_covariogram.to_frame()])

                    #morris
                    temp_morris_values = tsvars_funcs.morris_eq(temp_pair_df)
                    temp_maee = temp_morris_values[0]
                    temp_mee  = temp_morris_values[1]
                    self.maee = pd.concat([self.maee, temp_maee.to_frame()])
                    self.mee = pd.concat([self.mee, temp_mee.to_frame()])
                    if self.report_verbose:
                        vars_pbar.update(1)

                    #covariogram
                    temp_covariogram = tsvars_funcs.covariogram(temp_pair_df, temp_mu_overall)
                    if self.report_verbose:
                        vars_pbar.update(1)
                    self.cov = pd.concat([self.cov, temp_covariogram.to_frame()])

                    #e_covariogram
                    temp_e_covariogram = tsvars_funcs.e_covariogram(temp_sec_covariogram)
                    if self.report_verbose:
                        vars_pbar.update(1)
                    self.ecov = pd.concat([self.ecov, temp_e_covariogram.to_frame()])

                    #sobol
                    temp_sobol_values = tsvars_funcs.sobol_eq(temp_gamma, temp_e_covariogram, temp_var_overall, self.delta_h)
                    if self.report_verbose:
                        vars_pbar.update(1)
                    self.st = pd.concat([self.st, temp_sobol_values.to_frame()])

                    #ivars
                    temp_ivars_values = pd.DataFrame.from_dict({scale: temp_gamma.groupby(level=['ts', 'param']).apply(tsgvars_funcs.ivars, scale=scale, delta_h=self.delta_h) \
                      for scale in self.ivars_scales}, 'index').unstack()
                    if self.report_verbose:
                        vars_pbar.update(1)
                    temp_ivars_values.index.names = ['ts', 'param', 'h']
                    self.ivars = pd.concat([self.ivars, temp_ivars_values.to_frame()])

                    vars_pbar.close()

                    self.run_status = True

            else:
                # pair_df is built serially - other functions are the same as parallel
                self.pair_df = self._applyParallel(self.star_points_eval.groupby(level=0, axis=1), ts_pair, self.report_verbose)
                self.pair_df.index.names = ['ts', 'centre', 'param', 'h', 'pair_ind']

                # get rid of irrelevant h values
                self.pair_df = self.pair_df.droplevel('h')

                # bin and reorder pairs according to actual 'h' values
                xmin, xmax = tsgvars_funcs.find_boundaries(self.parameters, self.dist_sample_file)

                # dataframe to hold new pairs
                new_pair_df = pd.DataFrame()

                # bin and reorder pairs at each time step and insert into new pair df
                binning_flag = True  # used to ensure binning is calculated once
                binned_pairs = []  # contains the binned pairs in order
                dist_list = []  # contains actual 'h' values
                for date, new_df in self.pair_df.groupby(level=0):
                    if binning_flag:
                        # get the binned pairs (only needs to be calculated once)
                        binned_pairs, dist_list = tsgvars_funcs.reorder_pairs(new_df.droplevel(0), self.num_stars,
                                                                              self.parameters, self.star_points,
                                                                              self.delta_h, self.report_verbose, xmax,
                                                                              xmin)
                        binning_flag = False

                        if self.report_verbose:
                            ts_pbar = tqdm(desc='reordering pairs at each time step',
                                           total=len(self.pair_df.groupby(level=0)),
                                           dynamic_ncols=True)

                    # drop the date for now
                    new_df = new_df.droplevel(0)
                    new_df['actual h'] = dist_list

                    # re order pairs values according to the bins
                    centres = new_df.index.get_level_values(0).to_numpy()
                    params = new_df.index.get_level_values(1).to_numpy()
                    bps = binned_pairs.index.to_numpy()
                    new_index = pd.MultiIndex.from_arrays([centres, params, bps], names=['centre', 'param', 'pair_ind'])
                    new_df = new_df.reindex(new_index)

                    # add in new index h, according to bin ranges
                    # ex.) h = 0.1 = [0-0.15], h = 0.2 = [0.15-0.25]
                    h = list(binned_pairs.values)
                    new_df['h'] = h

                    # format data frame so that it works properly with variogram analsysis functions
                    new_df.set_index('h', append=True, inplace=True)
                    new_df.set_index('actual h', append=True, inplace=True)

                    new_df = new_df.reorder_levels(['centre', 'param', 'h', 'actual h', 'pair_ind'])
                    new_pair_df = pd.concat([new_pair_df, (pd.concat({date: new_df}, names=['ts']))])

                    if self.report_verbose:
                        ts_pbar.update(1)

                if self.report_verbose:
                    ts_pbar.close()

                # set new pair_df
                self.pair_df = new_pair_df

                # include a column containing the dissimilarity between pairs
                self.pair_df['dissimilarity'] = 0.5 * (self.pair_df[0] - self.pair_df[1]).pow(2)

                if self.report_verbose:
                    vars_pbar = tqdm(desc='VARS analysis', total=10, dynamic_ncols=True)

                self.mu_star_df = self.star_points_eval.groupby(level=['centre','param']).mean().stack().reorder_levels(order=[2,0,1]).sort_index()
                self.mu_star_df.index.names = ['ts', 'centre', 'param']
                if self.report_verbose:
                    vars_pbar.update(1)

                self.mu_overall = self.star_points_eval.apply(lambda x: np.mean(list(np.unique(x))))
                if self.report_verbose:
                    vars_pbar.update(1)

                self.var_overall = self.star_points_eval.apply(lambda x: np.nanvar(list(np.unique(x)), ddof=1))
                if self.report_verbose:
                    vars_pbar.update(1)

                self.gamma = tsvars_funcs.variogram(self.pair_df)
                if self.report_verbose:
                    vars_pbar.update(1)

                self.sec_covariogram = tsvars_funcs.cov_section(self.pair_df, self.mu_star_df)
                if self.report_verbose:
                    vars_pbar.update(1)

                self.morris = tsvars_funcs.morris_eq(self.pair_df)
                self.maee = self.morris[0]
                self.mee  = self.morris[1]
                if self.report_verbose:
                    vars_pbar.update(1)

                self.cov = tsvars_funcs.covariogram(self.pair_df, self.mu_overall)
                if self.report_verbose:
                    vars_pbar.update(1)

                self.ecov = tsvars_funcs.e_covariogram(self.sec_covariogram)
                if self.report_verbose:
                    vars_pbar.update(1)

                self.st = tsvars_funcs.sobol_eq(self.gamma, self.ecov, self.var_overall, self.delta_h)
                if self.report_verbose:
                    vars_pbar.update(1)

                self.ivars = pd.DataFrame.from_dict({scale: self.gamma.groupby(level=['ts', 'param']).apply(tsgvars_funcs.ivars, scale=scale, delta_h=self.delta_h) \
                      for scale in self.ivars_scales}, 'index').unstack()
                self.ivars.index.names = ['ts', 'param', 'h']
                if self.report_verbose:
                    vars_pbar.update(1)
                    vars_pbar.close()

                self.run_status = True

        # output dictionary
        self.output = {
            'Gamma':self.gamma,
            'ST': self.st,
            'MAEE':self.maee,
            'MEE':self.mee,
            'COV':self.cov,
            'ECOV':self.ecov,
            'IVARS':self.ivars,
            'IVARSid':self.ivars_scales,
            # 'rnkST':self.st_factor_ranking,
            # 'rnkIVARS':self.ivars_factor_ranking,
            # 'Gammalb':self.gammalb if self.bootstrap_flag is True else None,
            # 'Gammaub':self.gammaub if self.bootstrap_flag is True else None,
            # 'STlb':self.stlb if self.bootstrap_flag is True else None,
            # 'STub':self.stub if self.bootstrap_flag is True else None,
            # 'IVARSlb':self.ivarslb if self.bootstrap_flag is True else None,
            # 'IVARSub':self.ivarsub if self.bootstrap_flag is True else None,
            # 'relST':self.rel_st_factor_ranking if self.bootstrap_flag is True else None,
            # 'relIVARS':self.rel_ivars_factor_ranking if self.bootstrap_flag is True else None,
            # 'Groups': [self.ivars50_grp, self.st_grp] if self.grouping_flag is True else None,
            # 'relGrp': [self.reli_st_grp, self.reli_ivars50_grp] if self.grouping_flag is True else None,
        }

        # defining aggregated values
        self.gamma.aggregate = self.gamma.groupby(level=['param', 'h']).mean()
        self.st.aggregate = self.st.groupby(level=['param']).mean()
        self.maee.aggregate  = self.maee.groupby(level=['param', 'h']).mean()
        self.mee.aggregate   = self.mee.groupby(level=['param', 'h']).mean()
        self.cov.aggregate   = self.cov.groupby(level=['param', 'h']).mean()
        self.ecov.aggregate  = self.ecov.groupby(level=['param', 'h']).mean()
        self.ivars.aggregate = self.ivars.groupby(level=['param', 'h']).mean()

        # defining time normalized values
        self.gamma_normalized = self.gamma.unstack(level=1).div(self.gamma.unstack(level=1).sum(axis=1),
                                         axis=0).stack().swaplevel().reindex_like(self.gamma)
        self.st_normalized = self.st.unstack(level=1).div(self.st.unstack(level=1).sum(axis=1), axis=0).stack()
        self.maee_normalized = self.maee.unstack(level=1).div(self.maee.unstack(level=1).sum(axis=1),
                                        axis=0).stack().swaplevel().reindex_like(self.maee)
        self.mee_normalized = self.mee.unstack(level=1).div(self.mee.unstack(level=1).sum(axis=1), axis=0).stack().swaplevel().reindex_like(
            self.mee)
        self.cov_normalized = self.cov.unstack(level=1).div(self.cov.unstack(level=1).sum(axis=1), axis=0).stack().swaplevel().reindex_like(
            self.cov)
        self.ecov_normalized = self.ecov.unstack(level=1).div(self.ecov.unstack(level=1).sum(axis=1),
                                        axis=0).stack().swaplevel().reindex_like(self.ecov)
        self.ivars_normalized = self.ivars.unstack(level=1).div(self.ivars.unstack(level=1).sum(axis=1),
                                         axis=0).stack().swaplevel().reindex_like(self.ivars)

        # defining time normalized aggregate values
        self.gamma_normalized.aggregate = self.gamma_normalized.groupby(level=['param', 'h']).mean()
        self.st_normalized.aggregate = self.st_normalized.groupby(level=['param']).mean()
        self.maee_normalized.aggregate  = self.maee_normalized.groupby(level=['param', 'h']).mean()
        self.mee_normalized.aggregate   = self.mee_normalized.groupby(level=['param', 'h']).mean()
        self.cov_normalized.aggregate   = self.cov_normalized.groupby(level=['param', 'h']).mean()
        self.ecov_normalized.aggregate  = self.ecov_normalized.groupby(level=['param', 'h']).mean()
        self.ivars_normalized.aggregate = self.ivars_normalized.groupby(level=['param', 'h']).mean()

    @staticmethod
    def _applyParallel(
        dfGrouped: pd.DataFrame,
        func: Callable,
        progress: bool=False,
        ) -> pd.DataFrame:

        def _temp_func(func, name, group):
            return func(group), name

        @contextlib.contextmanager
        def _tqdm_joblib(tqdm_object):
            """
            Context manager to patch joblib to report into tqdm progress bar given as argument

            Source: https://stackoverflow.com/questions/24983493
                    /tracking-progress-of-joblib-parallel-execution
                    /58936697#58936697
            """
            class TqdmBatchCompletionCallback(joblib.parallel.BatchCompletionCallBack):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)

                def __call__(self, *args, **kwargs):
                    tqdm_object.update(n=self.batch_size)
                    return super().__call__(*args, **kwargs)

            old_batch_callback = joblib.parallel.BatchCompletionCallBack
            joblib.parallel.BatchCompletionCallBack = TqdmBatchCompletionCallback

            try:
                yield tqdm_object
            finally:
                joblib.parallel.BatchCompletionCallBack = old_batch_callback
                tqdm_object.close()

        if progress:
            with _tqdm_joblib(tqdm(desc="building pairs", total=len(dfGrouped), dynamic_ncols=True)) as progress_bar:
                retLst, top_index = zip(*Parallel(n_jobs=mp.cpu_count())\
                                            (delayed(_temp_func)(func, name, group)\
                                        for name, group in dfGrouped))
        else:
            retLst, top_index = zip(*Parallel(n_jobs=mp.cpu_count())\
                                            (delayed(_temp_func)(func, name, group)\
                                        for name, group in dfGrouped))

        return pd.concat(retLst, keys=top_index)


class DVARS(object):
    """
    Description:
    ------------
    The Python implementation of the Data Driven Variogram Analysis of Response
    Surfaces (DVARS) first introduced in Razavi and Gupta (2020) (see [3]_).



    Parameters:
    ----------
    simulation_file : pd.DataFrame
        The file name of file containing input and output data.
    outvarname : str
        The name of the output variable to calculate sensitivities for. Note
        that the output variable must be scalar.
    Hj : float, default: 0.5
        The fraction of the total parameter space to integrate over. Note that
        the linear correlation function only has one hyperparameter, so as the
        Reference notes it is unable to distinguish variogram effects at varying
        length scales.
    tol : float, default 1e-6
        The convergence tolerance for scipy's minimize function acting on the
        negative log likelihood function.
    verbose : bool, default False
        Whether to print diagnostic information.


    References:
    -----------
    .. [1] Razavi, S., & Gupta, H. V. (2016). A new framework for comprehensive,
           robust, and efficient global sensitivity analysis: 1. Theory. Water
           Resources Research, 52(1), 423-439. doi: 10.1002/2015WR017558
    .. [2] Razavi, S., & Gupta, H. V. (2016). A new framework for comprehensive,
           robust, and efficient global sensitivity analysis: 1. Application. Water
           Resources Research, 52(1), 423-439. doi: 10.1002/2015WR017559
    .. [3] Sheikholeslami, R., & Razavi, S. (2020). A Fresh Look at Variography:
           Measuring Dependence and Possible Sensitivities Across Geophysical
           Systems From Any Given Data. Geophysical Research Letters, 47(20).
           https://doi.org/10.1029/2020gl089829


    Contributors:
    -------------
    Razavi, Saman, (2015): algorithm, code in MATALB (c)
    Blanchard, Cordell, (2022): code in Python 3
    Shambaugh, Scott, (2022): code in Python 3
    """

    #-------------------------------------------
    # Constructors

    def __init__(
        self,
        data_file: str,
        outvarname: str,
        ivars_range: Optional[float] = 0.5,
        phi_max: Optional[float]= 1e6,
        phi0: Optional[float] = 1,
        correlation_func_type: Optional[str] = 'linear',
        tol: Optional[float] = 1e-6,
        report_verbose: Optional[bool] = False,  # reporting verbose
    ) -> None:

        # initialize values
        self.data_df = pd.read_csv(data_file)
        self.outvarname = outvarname
        self.ivars_range = ivars_range
        self.phi_max = phi_max
        self.report_verbose = report_verbose
        self.phi0 = phi0
        self.tol = tol # tolerance for optimizing phi values
        self.correlation_func_type = correlation_func_type
        # analysis stage is set to False before running anything
        self.run_status = False

        # Check input arguments
        # default value for bootstrap_flag
        if not isinstance(report_verbose, bool):
            warnings.warn(
                "`report_verbose` must be either `True` or `False`."
                "default value of `False` will be considered.",
                UserWarning,
                stacklevel=1
            )
            self.report_verbose = False


        ninvars = self.data_df.shape[1] - 1
        if 0 < ninvars < 2:
            raise ValueError(
                "the number of parameters in a sensitivity analysis problem"
                "must be greater than 1"
            )

    # -------------------------------------------
    # Representators
    def __repr__(self) -> str:
        """shows the status of VARS analysis"""

        status_verbose  = "Verbose: " + ("On" if self.report_verbose else "Off")
        status_analysis = "DVARS Analysis: " + ("Done" if self.run_status else "Not Done")

        status_report_list = [status_verbose, status_analysis]

        return "\n".join(status_report_list)

    def __str__(self) -> str:
        """shows the instance name of the VARS analysis experiment"""

        return self.__class__.__name__


    # -------------------------------------------
    # Core functions

    def run(self):
        """
        Runs DVARS analysis.

        """

        # run dvars to get sensitivites and ratios
        self.ivars, self.ratios, self.phi_opt, self.variance = dvars_funcs.calc_sensitivities(self.data_df, self.outvarname,
                                                                         self.ivars_range, self.phi_max,
                                                                         self.phi0, self.correlation_func_type, self.tol,
                                                                         self.report_verbose)

        # turn results into a dataframe
        self.ivars = pd.DataFrame([self.ivars], index=[self.ivars_range], columns=self.data_df.columns[self.data_df.columns != self.outvarname])
        self.ratios = pd.DataFrame([self.ratios], index=[self.ivars_range], columns=self.data_df.columns[self.data_df.columns != self.outvarname])

        self.run_status = True # for reporting