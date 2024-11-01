#! /usr/bin/env python3
# -*- coding: utf-8 -*-

#-----------------------#
# Import custom modules #
#-----------------------#

from pygenutils.arrays_and_lists.data_manipulation import flatten_to_string
from pygenutils.operative_systems.os_operations import exit_info, run_system_command
from paramlib.parameters_and_constants import global_parameters
from pygenutils.strings import information_output_formatters, string_handler
from pygenutils.time_handling.date_and_time_utils import find_time_key
from filewise.file_operations.ops_handler import rename_objects
from filewise.xarray_utils.patterns import get_file_variables, get_times

# Create aliases #
#----------------#

basic_four_rules = global_parameters.basic_four_rules
common_delim_list = global_parameters.common_delim_list
freq_abbrs = global_parameters.time_frequencies_shorter_1
time_freqs = global_parameters.time_frequencies_short_1

format_string = information_output_formatters.format_string

add_to_path = string_handler.add_to_path
find_substring_index = string_handler.find_substring_index
obj_path_specs = string_handler.obj_path_specs
modify_obj_specs = string_handler.modify_obj_specs

#-------------------------#
# Define custom functions #
#-------------------------#

# Internal Helper Functions #
#---------------------------#

def _get_varname_in_filename(file, return_std=False, varlist_orig=None, varlist_std=None):
    """
    Extracts the variable name from the file name or returns its standardised name.

    Parameters
    ----------
    file : str
        The file path or file name.
    return_std : bool, optional
        If True, returns the standardised variable name, by default False.
    varlist_orig : list, optional
        List of original variable names.
    varlist_std : list, optional
        List of standardised variable names corresponding to varlist_orig.

    Returns
    -------
    str
        The variable name extracted from the file name or its standardised counterpart.

    Raises
    ------
    ValueError
        If the variable is not found in the original variable list when `return_std` is True.
    """
    file_name_parts = obj_path_specs(file, file_spec_key="name_noext_parts", splitdelim=splitdelim1)
    var_file = file_name_parts[0]

    if return_std:
        var_pos = find_substring_index(varlist_orig, var_file)
        if var_pos != -1:
            return varlist_std[var_pos]
        else:
            raise ValueError(f"Variable '{var_file}' in '{file}' not found in original list {varlist_orig}.")
    return var_file


def _standardise_filename(variable, freq, model, experiment, calc_method, period, region, ext):
    """
    Creates a standardised filename based on input components.

    Parameters
    ----------
    variable : str
        Variable name.
    freq : str
        Frequency of the data (e.g., daily, monthly).
    model : str
        Model name.
    experiment : str
        Experiment name or type.
    calc_method : str
        Calculation method.
    period : str
        Time period string (e.g., '2000-2020').
    region : str
        Region or geographic area.
    ext : str
        File extension (e.g., 'nc').

    Returns
    -------
    str
        standardised filename.
    """
    return f"{variable}_{freq}_{model}_{experiment}_{calc_method}_{region}_{period}.{ext}"


# Main methods #
#--------------#

# Core Data Processing Functions #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def cdo_mergetime(file_list, variable, freq, model, experiment, calc_method, period, region, ext):
    """
    Merges time steps of multiple files into one using CDO's mergetime operator.

    Parameters
    ----------
    file_list : list
        List of file paths to merge.
    variable : str
        Variable name.
    freq : str
        Frequency of the data (e.g., daily, monthly).
    model : str
        Model name.
    experiment : str
        Experiment name or type.
    calc_method : str
        Calculation method.
    period : str
        Time period string (e.g., '2000-2020').
    region : str
        Region or geographic area.
    ext : str
        File extension (e.g., 'nc').

    Returns
    -------
    None
    """
    output_name = _standardise_filename(variable, freq, model, experiment, calc_method, period, region, ext)
    start_year, end_year = period.split(splitdelim2)
    file_list_selyear = [f for f in file_list if (year := obj_path_specs(f, "name_noext_parts", splitdelim1)[-1]) >= start_year and year <= end_year]

    allfiles_string = flatten_to_string(file_list_selyear)
    cmd = f"cdo -b F64 -f nc4 mergetime '{allfiles_string}' {output_name}"
    process_exit_info = run_system_command(cmd, capture_output=True)
    exit_info(process_exit_info)


def cdo_selyear(file_list, selyear_str, freq, model, experiment, calc_method, region, ext):
    """
    Selects data for specific years from a file list using CDO's selyear operator.

    Parameters
    ----------
    file_list : list
        List of file paths to select years from.
    selyear_str : str
        Start and end years (e.g., '2000/2010').
    freq : str
        Frequency of the data (e.g., daily, monthly).
    model : str
        Model name.
    experiment : str
        Experiment name or type.
    calc_method : str
        Calculation method.
    region : str
        Region or geographic area.
    ext : str
        File extension (e.g., 'nc').

    Returns
    -------
    None
    """
    selyear_split = obj_path_specs(selyear_str, file_spec_key="name_noext_parts", splitdelim=splitdelim2)
    start_year = f"{selyear_split[0]}"
    end_year = f"{selyear_split[-1]}"
    
    selyear_cdo = f"{start_year}/{end_year}"
    period = f"{start_year}-{end_year}"
    
    for file in file_list:
        var = _get_varname_in_filename(file)
        output_name = _standardise_filename(var, freq, model, experiment, calc_method, period, region, ext)
        cmd = f"cdo selyear,{selyear_cdo} '{file}' {output_name}"
        process_exit_info = run_system_command(cmd, capture_output=True)
        exit_info(process_exit_info)


def cdo_sellonlatbox(file_list, coords, freq, model, experiment, calc_method, region, ext):
    """
    Applies CDO's sellonlatbox operator to select a geographical box from the input files.

    Parameters
    ----------
    file_list : list
        List of file paths.
    coords : str
        Coordinates for the longitude-latitude box.
    freq : str
        Frequency of the data (e.g., daily, monthly).
    model : str
        Model name.
    experiment : str
        Experiment name or type.
    calc_method : str
        Calculation method.
    region : str
        Region or geographic area.
    ext : str
        File extension (e.g., 'nc').

    Returns
    -------
    None
    """
    for file in file_list:
        var = _get_varname_in_filename(file)
        time_var = find_time_key(file)
        times = get_times(file, time_var)
        period = f"{times.dt.year.values[0]}-{times.dt.year.values[-1]}"
        output_name = _standardise_filename(var, freq, model, experiment, calc_method, period, region, ext)
        cmd = f"cdo sellonlatbox,{coords} '{file}' {output_name}"
        process_exit_info = run_system_command(cmd, capture_output=True)
        exit_info(process_exit_info)
        

def cdo_remap(file_list, remap_str, var, freq, model, experiment, calc_method, period, region, ext, remap_method="bilinear"):
    """
    Applies remapping to the files using CDO's remap method.

    Parameters
    ----------
    file_list : list
        List of file paths.
    remap_str : str
        The remapping method to use (e.g., 'bil', 'nearest').
    var : str
        Variable name.
    freq : str
        Frequency of the data (e.g., daily, monthly).
    model : str
        Model name.
    experiment : str
        Experiment name or type.
    calc_method : str
        Calculation method.
    period : str
        Time period string (e.g., '2000-2020').
    region : str
        Region or geographic area.
    ext : str
        File extension (e.g., 'nc').
    remap_method : str, optional
        Remapping method (default is "bilinear").

    Returns
    -------
    None
    """
    output_name = _standardise_filename(var, freq, model, experiment, calc_method, period, region, ext)
    
    if remap_method not in cdo_remap_options:
        raise ValueError(f"Unsupported remap method. Options are {cdo_remap_options}")
    
    remap_cdo = cdo_remap_option_dict[remap_str]
    
    for file in file_list:
        cmd = f"cdo {remap_cdo},{remap_str} '{file}' {output_name}"
        process_exit_info = run_system_command(cmd, capture_output=True)
        exit_info(process_exit_info)


# Statistical and Analytical Functions #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def cdo_time_mean(input_file, var, freq, model, experiment, calc_method, period, region, ext):
    """
    Calculates the time mean for a specific variable using CDO.

    Parameters
    ----------
    input_file : str
        Path to the netCDF file.
    var : str
        Variable name.
    freq : str
        Frequency of the data (e.g., daily, monthly).
    model : str
        Model name.
    experiment : str
        Experiment name or type.
    calc_method : str
        Calculation method (e.g., 'mean', 'sum').
    period : str
        Time period string (e.g., '2000-2020').
    region : str
        Region or geographic area.
    ext : str
        File extension (e.g., 'nc').

    Returns
    -------
    None
    """
    output_name = _standardise_filename(var, freq, model, experiment, calc_method, period, region, ext)
    cmd = f"cdo -{calc_method} '{input_file}' {output_name}"
    process_exit_info = run_system_command(cmd, capture_output=True)
    exit_info(process_exit_info)
        

def cdo_periodic_statkit(nc_file, statistic, is_climatic, freq, season_str=None):
    """
    Calculates basic periodic statkit on a netCDF file using CDO.

    Parameters
    ----------
    nc_file : str
        Path to the netCDF file.
    statistic : str
        Statistic to calculate (e.g., 'mean', 'sum').
    is_climatic : bool
        Whether to calculate climatic statkit.
    freq : str
        Time frequency (e.g., 'monthly', 'yearly').
    season_str : str, optional
        Season to calculate if applicable, by default None.

    Returns
    -------
    None
    """
    if statistic not in statkit:
        raise ValueError(f"Unsupported statistic {statistic}. Options are {statkit}")
    
    period_abbr = freq_abbrs[find_substring_index(time_freqs, freq)]

    statname = f"y{period_abbr}{statistic}" if is_climatic else f"{period_abbr}{statistic}"
    
    if period_abbr == freq_abbrs[3] and season_str:
        statname += f" -select,season={season_str}"

    file_name_noext = add_to_path(nc_file, return_file_name_noext=True)
    string2add = f"{splitdelim1}{statname}" if not season_str else f"{splitdelim1}{statname}_{statname[-3:]}"
    output_name = modify_obj_specs(nc_file, "name_noext", add_to_path(file_name_noext, string2add))

    cmd = f"cdo {statname} {nc_file} {output_name}"
    process_exit_info = run_system_command(cmd, capture_output=True)
    exit_info(process_exit_info)    
    

def cdo_anomalies(input_file_full, input_file_avg, var, freq, model, experiment, calc_method, period, region, ext):
    """
    Calculates anomalies by subtracting the average from the full time series using CDO's sub operator.

    Parameters
    ----------
    input_file_full : str
        File path of the full time series data.
    input_file_avg : str
        File path of the average data (e.g., climatology).
    var : str
        Variable name.
    freq : str
        Frequency of the data (e.g., daily, monthly).
    model : str
        Model name.
    experiment : str
        Experiment name or type.
    calc_method : str
        Calculation method
    period : str
        Time period string (e.g., '2000-2020').
    region : str
        Region or geographic area.
    ext : str
        File extension (e.g., 'nc').

    Returns
    -------
    None
    """
    output_name = _standardise_filename(var, freq, model, experiment, calc_method, period, region, ext)
    cmd = f"cdo sub '{input_file_avg}' '{input_file_full}' {output_name}"
    process_exit_info = run_system_command(cmd, capture_output=True)
    exit_info(process_exit_info)


def calculate_periodic_deltas(proj_file, hist_file, operator="+", delta_period="monthly", model=None):
    """
    Calculates periodic deltas between projected and historical data using CDO.

    Parameters
    ----------
    proj_file : str
        Path to the projected netCDF file.
    hist_file : str
        Path to the historical netCDF file.
    operator : str, optional
        Operation to apply between files ('+', '-', '*', '/'). Default is '+'.
    delta_period : str, optional
        Period for delta calculation (e.g., 'monthly', 'yearly'). Default is 'monthly'.
    model : str, optional
        Model name, required if not inferred from the file name.

    Returns
    -------
    None
    """
    period_idx = find_substring_index(time_freqs_delta, delta_period)
    if period_idx == -1:
        raise ValueError(f"Unsupported delta period. Options are {time_freqs_delta}")

    if model is None:
        raise ValueError("Model must be provided to calculate deltas.")
    
    period_abbr = freq_abbrs_delta[period_idx]
    hist_mean_cmd = f"-y{period_abbr}mean {hist_file}"
    proj_mean_cmd = f"-y{period_abbr}mean {proj_file}"
    
    delta_filename = add_to_path(hist_file, return_file_name_noext=True)
    string2add = f"{period_abbr}Deltas_{model}.nc"
    delta_output = add_to_path(delta_filename, string2add)
    
    if operator not in basic_four_rules:
        raise ValueError(f"Unsupported operator. Options are {basic_four_rules}")
    
    operator_str = cdo_operator_str_dict[operator]
    cmd = f"cdo {operator_str} {hist_mean_cmd} {proj_mean_cmd} {delta_output}"
    process_exit_info = run_system_command(cmd, capture_output=True)
    exit_info(process_exit_info)


def apply_periodic_deltas(proj_file, hist_file, operator="+", delta_period="monthly", model=None):
    """
    Applies periodic deltas between projected and historical data using CDO.

    Parameters
    ----------
    proj_file : str
        Path to the projected netCDF file.
    hist_file : str
        Path to the historical netCDF file.
    operator : str, optional
        Operation to apply between files ('+', '-', '*', '/'). Default is '+'.
    delta_period : str, optional
        Period for delta application (e.g., 'monthly', 'yearly'). Default is 'monthly'.
    model : str, optional
        Model name, required if not inferred from the file name.

    Returns
    -------
    None
    """
    period_idx = find_substring_index(time_freqs_delta, delta_period)
    if period_idx == -1:
        raise ValueError(f"Unsupported delta period. Options are {time_freqs_delta}")

    if model is None:
        raise ValueError("Model must be provided to apply deltas.")
    
    period_abbr = freq_abbrs_delta[period_idx]
    delta_output = add_to_path(hist_file, return_file_name_noext=True)
    string2add = f"{period_abbr}DeltaApplied_{model}.nc"
    delta_applied_output = add_to_path(delta_output, string2add)
    
    hist_mean_cmd = f"-y{period_abbr}mean {hist_file}"
    
    if operator not in basic_four_rules:
        raise ValueError(f"Unsupported operator. Options are {basic_four_rules}")
    
    operator_str = cdo_operator_str_dict[operator]
    cmd = f"cdo {operator_str} {proj_file} {hist_mean_cmd} {delta_applied_output}"
    process_exit_info = run_system_command(cmd, capture_output=True)
    exit_info(process_exit_info)


# File Renaming and Organizational Functions #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    
def cdo_rename(file_list, varlist_orig, varlist_std):
    """
    Renames variables in the files using a standardised variable list via CDO's chname operator.

    Parameters
    ----------
    file_list : list
        List of file paths to rename.
    varlist_orig : list
        List of original variable names.
    varlist_std : list
        List of standardised variable names corresponding to varlist_orig.

    Returns
    -------
    None
    """
    for i, file in enumerate(file_list, start=1):
        var_file = get_file_variables(file)
        var_std = _get_varname_in_filename(file, True, varlist_orig, varlist_std)
        
        print(f"Renaming variable '{var_file}' to '{var_std}' in file {i}/{len(file_list)}...")
        
        temp_file = add_to_path(file)
        cmd = f"cdo chname,{var_file},{var_std} '{file}' '{temp_file}'"
        process_exit_info = run_system_command(cmd, capture_output=True)
        exit_info(process_exit_info)
        
        rename_objects(temp_file, file)
        

def change_filenames_by_var(file_list, varlist_orig, varlist_std):
    """
    Renames files by updating the variable name in their filenames using a standardised variable list.

    Parameters
    ----------
    file_list : list
        List of file paths to rename.
    varlist_orig : list
        List of original variable names.
    varlist_std : list
        List of standardised variable names corresponding to varlist_orig.
    
    Returns
    -------
    None
    """
    for file in file_list:
        std_var = _get_varname_in_filename(file, True, varlist_orig, varlist_std)
        file_name_parts = obj_path_specs(file, file_spec_key="name_noext_parts", splitdelim=splitdelim1)
        new_filename = modify_obj_specs(file, "name_noext_parts", (file_name_parts[0], std_var))
        rename_objects(file, new_filename)

        

# Time and Date Adjustment Functions #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def cdo_inttime(file_list, year0, month0, day0, hour0, minute0, second0, time_step):
    """
    Initialises time steps in the files with a specific starting date and step using CDO's inttime operator.

    Parameters
    ----------
    file_list : list
        List of file paths.
    year0 : int
        Start year.
    month0 : int
        Start month.
    day0 : int
        Start day.
    hour0 : int
        Start hour.
    minute0 : int
        Start minute.
    second0 : int
        Start second.
    time_step : str
        Time step size (e.g., '6hour').

    Returns
    -------
    None
    """
    for file in file_list:
        temp_file = add_to_path(file)
        start_date = f"{year0}-{month0:02d}-{day0:02d} {hour0:02d}:{minute0:02d}:{second0:02d}"
        cmd = f"cdo inttime,{start_date},{time_step} '{file}' '{temp_file}'"
        process_exit_info = run_system_command(cmd, capture_output=True)
        exit_info(process_exit_info)
        rename_objects(temp_file, file)
        

def cdo_shifttime(file_list, shift_val):
    """
    Shifts time steps in the files by a specified value using CDO's shifttime operator.

    Parameters
    ----------
    file_list : list
        List of file paths.
    shift_val : str
        Time shift value (e.g., '+1day', '-6hours').

    Returns
    -------
    None
    """
    for file in file_list:
        temp_file = add_to_path(file)
        cmd = f"cdo shifttime,{shift_val} '{file}' '{temp_file}'"
        process_exit_info = run_system_command(cmd, capture_output=True)
        exit_info(process_exit_info)
        rename_objects(temp_file, file)


# Miscellaneous Functions #
#~~~~~~~~~~~~~~~~~~~~~~~~~#

def create_grid_header_file(output_file, **kwargs):
    """
    Create a grid header file.

    Parameters
    ----------
    output_file : str or Path
        Path to the txt file where the reference grid will be stored.
    kwargs : dict
        Parameters that define the grid (e.g., xmin, ymax, total lines, total columns, etc.).

    Returns
    -------
    None
    """
    kwargs_values = list(kwargs.values())
    kwargs_keys = list(kwargs.keys())
    kwargs_keys.sort()

    if kwargs_keys != keylist:
        kwargs = {key: val for key, val in zip(keylist, kwargs_values)}

    grid_template = """gridtype  = lonlat
xsize     = {0:d}
ysize     = {1:d}
xname     = longitude
xlongname = "Longitude values"
xunits    = "degrees_east"
yname     = latitude
ylongname = "Latitude values"
yunits    = "degrees_north"
xfirst    = {2:.20f}
xinc      = {3:.20f}
yfirst    = {4:.20f}
"""
    grid_str = format_string(grid_template, tuple([kwargs[key] for key in keylist[:6]]))
    
    with open(output_file, 'w') as output_f:
        output_f.write(grid_str)        
        

def custom_cdo_mergetime(file_list, custom_output_name, create_temp_file=False):
    """
    Custom CDO mergetime operation that optionally uses a temporary file.

    Parameters
    ----------
    file_list : list
        List of file paths to merge.
    custom_output_name : str
        Custom output file name.
    create_temp_file : bool, optional
        Whether to use a temporary file for intermediate steps, by default False.

    Returns
    -------
    None
    """
    allfiles_string = flatten_to_string(file_list)
    
    if not create_temp_file:
        cmd = f"cdo -b F64 -f nc4 mergetime '{allfiles_string}' {custom_output_name}"
    else:
        temp_file = add_to_path(file_list[0])
        cmd = f"cdo -b F64 -f nc4 mergetime '{allfiles_string}' {temp_file}"
                     
    process_exit_info = run_system_command(cmd, capture_output=True)
    exit_info(process_exit_info)


#--------------------------#
# Parameters and constants #
#--------------------------#

# Strings #
#---------#

# String-splitting delimiters #
splitdelim1 = common_delim_list[0]
splitdelim2 = common_delim_list[1]

# Grid header file function key list #
keylist = ['total_columns', 'total_lines', 'xmin', 'xres', 'ymin', 'yres']

# Calendar and date-time parameters #
time_freqs_delta = [time_freqs[0]] + time_freqs[2:4]
freq_abbrs_delta = [freq_abbrs[0]] + freq_abbrs[2:4]

# Statistics and operators #
#--------------------------#

# Basic statkit #
statkit = ["max", "min", "sum", 
              "mean", "avg", 
              "var", "var1",
              "std", "std1"]
  
# CDO remapping options #
cdo_remap_option_dict = {
    "ordinary" : "remap",
    "bilinear" : "remapbil",
    "nearest_neighbour" : "remapnn",
    "bicubic" : "remapbic",
    "conservative1" : "remapcon",
    "conservative2" : "remapcon2",
    "conservative1_y" : "remapycon",
    "distance_weighted_average" : "remapdis",
    "vertical_hybrid" : "remapeta",
    "vertical_hybrid_sigma" : "remapeta_s",
    "vertical_hybrid_z" : "remapeta_z",
    "largest_area_fraction" : "remaplaf",
    "sum" : "remapsum",
    }

cdo_remap_options = list(cdo_remap_option_dict.keys())

                          
# Basic operator switch case dictionary #
cdo_operator_str_dict = {
    basic_four_rules[0] : "add",
    basic_four_rules[1] : "sub",
    basic_four_rules[2] : "mul",
    basic_four_rules[3] : "div"
    }
