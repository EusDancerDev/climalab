#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-----------------------#
# Import custom modules #
#-----------------------#

from climalab.cds_tools import download_data
from paramlib.global_parameters import climate_file_extensions
from pygenutils.strings.string_handler import find_substring_index
from pygenutils.time_handling.program_snippet_exec_timers import program_exec_timer
from filewise.file_operations import ops_handler, path_utils
from filewise.xarray_utils import file_utils, xarray_obj_handler

# Create aliases #
#----------------#

make_directories = ops_handler.make_directories
move_files = ops_handler.move_files

find_files = path_utils.find_files

scan_ncfiles = file_utils.scan_ncfiles
grib2nc = xarray_obj_handler.grib2nc

#-------------------------#
# Define custom functions #
#-------------------------#

def return_file_extension(file_format):
    # File extension #
    extension_idx = find_substring_index(available_formats, file_format)
    
    if extension_idx == -1:
        raise ValueError(f"Unsupported file format. Choose from '{available_formats}'.")
    else:
        extension = available_extensions[extension_idx]
        return extension

    
#---------------------#
# Variable parameters #
#---------------------#

# Project name #
project_name = "EusDancerDev"

# Coverage area #
#---------------#

# Country names #
country_list = ["Basque-Country"]

# List of areas #
"""
Order of the cardinal points in each list is the following:
f"{North}, {West}, {South}, {East}"
"""
area_lists = [
    [45, 1, 40, 4],
    ]

# Date and times #
#----------------#

year_range = [f"{i:04d}" for i in range(1977,1978)]
month_range = [f"{i:02d}" for i in range(1,2)]
day_range = [f"{i:02d}" for i in range(1,2)]
hour_range = [f"{i:02d}:00" for i in range(0,1)]

# Variables #
#-----------#

variable_list = [
    '2m_temperature', '2m_dewpoint_temperature', 
    '10m_u_component_of_wind', '10m_v_component_of_wind', 
    'surface_pressure',
    'surface_solar_radiation_downwards', 'surface_thermal_radiation_downwards',
    'total_precipitation'
    ]

# Downloadable formats and extensions #
#-------------------------------------#

file_format = "grib"
extension = return_file_extension(file_format)

# Option to convert 'grib' files to netCDF
convert_to_nc = True

#------------------#
# Fixed parameters #
#------------------#

# Main directories #
#------------------#

# Document containing directory #
repo_path = "/home/jonander/Documents/gordetegiak/pygenutils."

# Project (main) directory #
project_dir = f"{repo_path}/test-base_programs/{project_name}"

# Code-containing directory #
codes_dir = f"{project_dir}/codes"

# Input (downloaded) data main directory #
main_input_data_dir = f"{project_dir}/input_data"

# Dataset #
#---------#

dataset = "ERA5"
dataset_lower = dataset.lower()

# Product attributes #
#--------------------#

product_name = f"reanalysis-{dataset_lower}"

# Area #
#------#

area_kw = "area"

# Date and times #
#----------------#

year_kw = "year"
month_kw = "month"
day_kw = "day"
hour_kw = "hour"

# Variables #
#-----------#

variable_kw = "variable"

# Downloadable formats and extensions #
#-------------------------------------#

format_kw = "format"

available_formats = ["netcdf", "grib", "netcdf_zip"]
available_extensions = climate_file_extensions[:-1]

#--------------------#
# Initialise program #
#--------------------#

program_exec_timer('start')

#-----------------------------------#
# Loop through the different ranges #
#-----------------------------------#

# Create, if necessary, the input data directory specific for the data set #
ds_input_data_dir = f"{main_input_data_dir}/{dataset}"
make_directories(ds_input_data_dir)

"""
The standardised hierarchy for the loops
in the case of this data set is as follows:

    -1. Country and the selected area
    -2. Year
    -3. Month
    -4. Day
    -5. Hour/time
    
It is possible that there will not be data available for certain period(s) of time,
or if it is the case, not every variable will be available.

Analyzing each and every one of the possibilities requires
a great effort, but there is no way to catch the 
exit status of the downloading process, so if there is an error,
the CDS API will specify the type thereof and will lead to a program halt.
"""

for country, area_list in zip(country_list, area_lists):
    for y in year_range:
        for m in month_range:
            for d in day_range:
                for h in hour_range:
                    
                    # Set the keyword argument dictionary to pass in later on #
                    kwargs = {
                        year_kw : y,
                        month_kw : m,
                        day_kw : d,
                        hour_kw : h,
                        area_kw : area_list,
                        variable_kw : variable_list,
                        format_kw : file_format,
                        }
                    
                    # Gather every parameter to form the output file name #
                    output_file_name = f"{dataset_lower}_{country}_{y}-{m}-{d}.{extension}"

                    """
                    Test whether the file is already downloaded
                    (current or downloaded data directory)
                    """
                    ofn_list = find_files(f"*{output_file_name}*",
                                          search_path=project_dir,
                                          match_type="glob")
                    
                    lofnl = len(ofn_list)
                    
                    if lofnl > 0:
                        num_faulty_ncfiles = scan_ncfiles(codes_dir)
                        
                        if num_faulty_ncfiles > 0:   
                            # Download the specified data #
                            download_data(product_name, output_file_name, **kwargs)
                            
                    else:
                        # Download the specified data #
                        download_data(product_name, output_file_name, **kwargs)

# Move the downloaded data from the directory where the code is being called #
if file_format == "grib" and convert_to_nc:
    all_grib_files = find_files(file_format, search_path=project_dir)
    grib2nc(all_grib_files, on_shell=True)
    result_ext = available_extensions[0]
else:
    result_ext = extension
    
move_files(result_ext, 
           input_directories=".", 
           destination_directories=ds_input_data_dir,
           match_type='ext')


#---------------------------------------#
# Calculate full program execution time #
#---------------------------------------#

program_exec_timer('stop')
