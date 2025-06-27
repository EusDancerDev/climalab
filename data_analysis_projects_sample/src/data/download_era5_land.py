#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script to download ERA5-Land data using the configuration file.
"""

#----------------#
# Import modules #
#----------------#

import logging
import os
import sys
from pathlib import Path
from typing import Any

import yaml

#------------------------#
# Import project modules #
#------------------------#

from cds_tools import download_data
from filewise.file_operations.ops_handler import (
    find_files,
    make_directories,
    move_files
)
from filewise.xarray_utils.file_utils import scan_ncfiles
from filewise.xarray_utils.xarray_obj_handler import grib2nc
from pygenutils.strings.string_handler import find_substring_index
from pygenutils.time_handling.program_snippet_exec_timers import program_exec_timer

#------------------#
# Define functions #
#------------------#

# Pure backend functions #
#------------------------#

# Set up logging #
def set_up_logging() -> None:
    """
    Set up logging configuration for the ERA5-Land download script.
    
    Configures the logging module with INFO level and a standard format
    that includes timestamp, logger name, level, and message.
    
    Returns
    -------
    None
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
logger = logging.getLogger(__name__)

# Load configuration #
def load_config(config_path: str | Path) -> dict[str, Any]:
    """
    Load the ERA5-Land configuration file from the specified path.
    
    Reads and parses a YAML configuration file containing parameters
    for ERA5-Land reanalysis data download including geographical areas,
    temporal settings, variables, and output options.
    
    Parameters
    ----------
    config_path : str | Path
        Path to the YAML configuration file. Can be a string path
        or pathlib.Path object.
    
    Returns
    -------
    dict[str, Any]
        Dictionary containing all configuration parameters loaded
        from the YAML file.
        
    Raises
    ------
    FileNotFoundError
        If the configuration file does not exist at the specified path.
    yaml.YAMLError
        If the YAML file is malformed or cannot be parsed.
    SystemExit
        If any error occurs during file loading, the programme exits
        with an error message logged.
        
    Examples
    --------
    >>> config = load_config('config/era5_land_config.yaml')
    >>> print(config['dataset'])
    'ERA5-Land'
    """
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        logger.error(f"Error loading configuration file: {e}")
        sys.exit(1)

# Validate configuration #
def validate_config(config: dict[str, Any]) -> None:
    """
    Validate that all required ERA5-Land configuration parameters are present and valid.
    
    Performs comprehensive validation of the configuration dictionary to ensure
    all required parameters are present and their values are within acceptable
    ranges for the ERA5-Land data download.
    
    Parameters
    ----------
    config : dict[str, Any]
        Configuration dictionary containing ERA5-Land download parameters.
        Must include required fields such as geographical areas, temporal ranges,
        variables, and file format specifications.
    
    Returns
    -------
    None
    
    Raises
    ------
    SystemExit
        If any required parameter is missing or contains invalid values.
        Error details are logged before exit.
        
    Examples
    --------
    >>> config = {'file_format': 'netcdf', 'variable_list': ['2m_temperature'], ...}
    >>> validate_config(config)  # Validates successfully
    """
    required_params = [
        'project_name', 'country_list', 'area_lists', 'year_range',
        'month_range', 'day_range', 'hour_range', 'variable_list',
        'file_format', 'convert_to_nc', 'dataset', 'dataset_lower',
        'product_name', 'area_kw', 'year_kw', 'month_kw', 'day_kw',
        'hour_kw', 'variable_kw', 'format_kw'
    ]
    
    for param in required_params:
        if param not in config:
            logger.error(f"Missing required parameter: {param}")
            sys.exit(1)
    
    # Validate file format
    if config['file_format'] not in config['available_formats']:
        logger.error(f"Invalid file format: {config['file_format']}")
        sys.exit(1)

# Return file extension #
def return_file_extension(config: dict[str, Any]) -> str:
    """
    Return the file extension based on the configured file format.
    
    Maps the file format specification in the configuration to the
    corresponding file extension for proper file naming.
    
    Parameters
    ----------
    config : dict[str, Any]
        Configuration dictionary containing file format and available
        extensions mapping.
    
    Returns
    -------
    str
        File extension corresponding to the specified format (e.g., 'nc', 'grib').
        
    Raises
    ------
    ValueError
        If the specified file format is not supported or not found in
        the available formats list.
        
    Examples
    --------
    >>> config = {'file_format': 'netcdf', 'available_formats': ['netcdf'], 
    ...           'available_extensions': ['nc']}
    >>> ext = return_file_extension(config)
    >>> print(ext)
    nc
    """
    extension_idx = find_substring_index(config['available_formats'], config['file_format'])
    
    if extension_idx == -1:
        raise ValueError(f"Unsupported file format. Choose from '{config['available_formats']}'.")
    else:
        extension = config['available_extensions'][extension_idx]
        return extension

# Download data #
#---------------#

def download_era5_land_data(config: dict[str, Any]) -> None:
    """
    Download ERA5-Land reanalysis data using the CDS API based on configuration parameters.
    
    This function handles the complete ERA5-Land data download workflow including
    parameter preparation, file checking, downloading via CDS API for multiple
    countries/areas and time periods, format conversion, and file organisation.
    It includes robust error handling and avoids duplicate downloads.
    
    Parameters
    ----------
    config : dict[str, Any]
        Complete configuration dictionary containing all necessary parameters
        for ERA5-Land data download including geographical areas, temporal settings,
        variables, format options, and file paths.
    
    Returns
    -------
    None
        Downloads data files to the specified directory structure.
        
    Raises
    ------
    SystemExit
        If critical errors occur during the download process, such as
        network failures, invalid credentials, or file system issues.
        
    Notes
    -----
    - Creates temporary directories for intermediate file handling
    - Loops through multiple countries, years, months, days, and hours
    - Checks for existing files to avoid unnecessary re-downloads
    - Optionally converts GRIB files to netCDF format
    - Validates downloaded files using netCDF integrity checking
    - Automatically organises files in the specified directory structure
    - Cleans up temporary files after successful completion
    
    Examples
    --------
    >>> config = load_config('era5_land_config.yaml')
    >>> download_era5_land_data(config)  # Downloads data according to config
    """
    # Get file extension
    extension = return_file_extension(config)
    
    # Create dataset-specific input directory
    ds_input_data_dir = f"{config['main_input_data_dir']}/{config['dataset']}"
    make_directories(ds_input_data_dir)
    
    # Create temporary output directory
    temp_output_dir = Path(os.getcwd()) / "temp_downloads"
    make_directories(temp_output_dir)
    
    # Loop through the different parameters
    for country, area_list in zip(config['country_list'], config['area_lists']):
        for y in config['year_range']:
            for m in config['month_range']:
                for d in config['day_range']:
                    for h in config['hour_range']:
                        # Set the keyword argument dictionary
                        kwargs = {
                            config['year_kw']: y,
                            config['month_kw']: m,
                            config['day_kw']: d,
                            config['hour_kw']: h,
                            config['area_kw']: area_list,
                            config['variable_kw']: config['variable_list'],
                            config['format_kw']: config['file_format'],
                        }
                        
                        # Generate output filename
                        output_file_name = f"{config['dataset_lower']}_{country}_{y}-{m}-{d}.{extension}"
                        output_file = temp_output_dir / output_file_name
                        
                        # Check if the file already exists
                        existing_files = find_files(f"*{output_file_name}*", search_path=config['project_dir'], match_type="glob")
                        
                        if existing_files:
                            logger.info(f"File {output_file_name} already exists in {config['project_dir']}")
                            
                            # Check if the existing file is valid
                            num_faulty_files = scan_ncfiles(config['codes_dir'])
                            
                            if num_faulty_files > 0:
                                logger.info(f"Found {num_faulty_files} faulty files, re-downloading...")
                                # Download the data
                                try:
                                    logger.info(f"Downloading ERA5-Land data to {output_file}")
                                    download_data(
                                        config['product_name'],
                                        str(output_file),
                                        **kwargs
                                    )
                                    logger.info("Download completed successfully")
                                except Exception as e:
                                    logger.error(f"Error downloading data: {e}")
                                    sys.exit(1)
                            else:
                                logger.info("Existing files are valid, skipping download")
                        else:
                            # File doesn't exist, download it
                            try:
                                logger.info(f"Downloading ERA5-Land data to {output_file}")
                                download_data(
                                    config['product_name'],
                                    str(output_file),
                                    **kwargs
                                )
                                logger.info("Download completed successfully")
                            except Exception as e:
                                logger.error(f"Error downloading data: {e}")
                                sys.exit(1)
    
    # Convert GRIB files to netCDF if requested
    if config['file_format'] == "grib" and config['convert_to_nc']:
        logger.info("Converting GRIB files to netCDF format")
        all_grib_files = find_files(config['file_format'], search_path=str(temp_output_dir))
        grib2nc(all_grib_files, on_shell=True)
        result_ext = config['available_extensions'][0]  # Use netCDF extension
    else:
        result_ext = extension
    
    # Move the downloaded files to the dataset-specific input directory
    logger.info(f"Moving downloaded files to {ds_input_data_dir}")
    move_files(result_ext, 
              input_directories=str(temp_output_dir), 
              destination_directories=ds_input_data_dir,
              match_type='ext')
    
    # Clean up the temporary directory
    try:
        temp_output_dir.rmdir()
        logger.info(f"Removed temporary directory {temp_output_dir}")
    except Exception as e:
        logger.warning(f"Could not remove temporary directory {temp_output_dir}: {e}")

# Main function #
#---------------#

def main() -> None:
    """
    Main function to orchestrate the ERA5-Land data download process.
    
    Loads configuration, validates parameters, and initiates the download
    process for ERA5-Land reanalysis data from the CDS.
    
    Returns
    -------
    None
    """
    # Get the configuration file path
    script_dir = Path(__file__).parent.parent.parent
    config_path = script_dir / 'config' / 'era5_land_config.yaml'
    
    # Load and validate configuration
    config = load_config(config_path)
    validate_config(config)
    
    # Download data
    download_era5_land_data(config)

#--------------------#
# Initialise program #
#--------------------#

program_exec_timer('start')

if __name__ == '__main__':
    main()

#---------------------------------------#
# Calculate full program execution time #
#---------------------------------------#

program_exec_timer('stop') 