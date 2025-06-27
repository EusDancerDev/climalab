#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script to download E-OBS data using the configuration file.
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
    make_directories,
    move_files,
    find_files
)
from filewise.xarray_utils.file_utils import scan_ncfiles
from pygenutils.time_handling.program_snippet_exec_timers import program_exec_timer
from pygenutils.strings.string_handler import find_substring_index, substring_replacer

#------------------#
# Define functions #
#------------------#

# Pure backend functions #
#------------------------#

# Set up logging #
def set_up_logging() -> None:
    """
    Set up logging configuration for the E-OBS download script.
    
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
    Load the E-OBS configuration file from the specified path.
    
    Reads and parses a YAML configuration file containing parameters
    for E-OBS observational data download including products, periods,
    variables, and output settings.
    
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
    >>> config = load_config('config/eobs_config.yaml')
    >>> print(config['product_type'])
    'gridded'
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
    Validate that all required E-OBS configuration parameters are present and valid.
    
    Performs comprehensive validation of the configuration dictionary to ensure
    all required parameters are present and their values are within acceptable
    ranges for the E-OBS data download.
    
    Parameters
    ----------
    config : dict[str, Any]
        Configuration dictionary containing E-OBS download parameters.
        Must include required fields such as product type, periods, variables,
        resolution, and file format specifications.
    
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
    >>> config = {'product_type': 'gridded', 'resolution': '0.25deg', ...}
    >>> validate_config(config)  # Validates successfully
    """
    required_params = [
        'project_name', 'product_type', 'periods', 'variable_list',
        'file_format', 'version', 'resolution', 'dataset', 'dataset_lower',
        'product_name', 'product_kw', 'period_kw', 'variable_kw',
        'format_kw', 'version_kw', 'resolution_kw'
    ]
    
    for param in required_params:
        if param not in config:
            logger.error(f"Missing required parameter: {param}")
            sys.exit(1)
    
    # Validate product type
    if config['product_type'] not in config['available_products']:
        logger.error(f"Invalid product type: {config['product_type']}")
        sys.exit(1)
    
    # Validate file format
    if config['file_format'] not in config['available_formats']:
        logger.error(f"Invalid file format: {config['file_format']}")
        sys.exit(1)
    
    # Validate resolution
    if config['resolution'] not in config['available_resolutions']:
        logger.error(f"Invalid resolution: {config['resolution']}")
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
        File extension corresponding to the specified format (e.g., 'nc', 'zip').
        
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

# Return grid resolution #
def return_grid_resolution(config: dict[str, Any]) -> str:
    """
    Return the grid resolution with the appropriate suffix for API requests.
    
    Formats the resolution specification by adding the 'deg' suffix
    required by the CDS API for grid resolution parameters.
    
    Parameters
    ----------
    config : dict[str, Any]
        Configuration dictionary containing resolution specification
        and available resolutions list.
    
    Returns
    -------
    str
        Formatted grid resolution string with 'deg' suffix (e.g., '0.25deg').
        
    Raises
    ------
    ValueError
        If the specified resolution is not in the list of available resolutions.
        
    Examples
    --------
    >>> config = {'resolution': '0.25', 'available_resolutions': ['0.25', '0.5']}
    >>> res = return_grid_resolution(config)
    >>> print(res)
    0.25deg
    """
    if config['resolution'] not in config['available_resolutions']:
        raise ValueError(f"Invalid grid resolution. Choose from {config['available_resolutions']}")
    else:
        resolution = config['resolution'] + "deg"
        return resolution

# Download data #
#---------------#

def download_eobs_data(config: dict[str, Any]) -> None:
    """
    Download E-OBS observational data using the CDS API based on configuration parameters.
    
    This function handles the complete E-OBS data download workflow including
    parameter preparation, file checking, downloading via CDS API for multiple
    time periods, and file organisation. It includes robust error handling
    and avoids duplicate downloads.
    
    Parameters
    ----------
    config : dict[str, Any]
        Complete configuration dictionary containing all necessary parameters
        for E-OBS data download including product type, periods, variables,
        resolution, and file paths.
    
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
    - Loops through multiple time periods for batch downloading
    - Checks for existing files to avoid unnecessary re-downloads
    - Validates downloaded files using netCDF integrity checking
    - Automatically organises files in the specified directory structure
    - Cleans up temporary files after successful completion
    
    Examples
    --------
    >>> config = load_config('eobs_config.yaml')
    >>> download_eobs_data(config)  # Downloads data according to config
    """
    # Get file extension and grid resolution
    extension = return_file_extension(config)
    resolution_std = return_grid_resolution(config)
    
    # Create dataset-specific input directory
    ds_input_data_dir = f"{config['main_input_data_dir']}/{config['dataset']}"
    make_directories(ds_input_data_dir)
    
    # Create temporary output directory
    temp_output_dir = Path(os.getcwd()) / "temp_downloads"
    make_directories(temp_output_dir)
    
    # Loop through the different periods
    for period in config['periods']:
        p_std = substring_replacer(period, "_", "-")
        
        # Set the keyword argument dictionary
        kwargs = {
            config['product_kw']: config['product_type'],
            config['variable_kw']: config['variable_list'],
            config['resolution_kw']: resolution_std,
            config['period_kw']: period,
            config['version_kw']: config['version'],
            config['format_kw']: config['file_format'],
        }
        
        # Generate output filename
        output_file_name = f"{config['dataset_lower']}_{config['product_type']}_{p_std}.{extension}"
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
                    logger.info(f"Downloading E-OBS data to {output_file}")
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
                logger.info(f"Downloading E-OBS data to {output_file}")
                download_data(
                    config['product_name'],
                    str(output_file),
                    **kwargs
                )
                logger.info("Download completed successfully")
            except Exception as e:
                logger.error(f"Error downloading data: {e}")
                sys.exit(1)
    
    # Move the downloaded files to the dataset-specific input directory
    logger.info(f"Moving downloaded files to {ds_input_data_dir}")
    move_files(extension, 
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
    Main function to orchestrate the E-OBS data download process.
    
    Loads configuration, validates parameters, and initiates the download
    process for E-OBS observational gridded data from the CDS.
    
    Returns
    -------
    None
    """
    # Get the configuration file path
    script_dir = Path(__file__).parent.parent.parent
    config_path = script_dir / 'config' / 'eobs_config.yaml'
    
    # Load and validate configuration
    config = load_config(config_path)
    validate_config(config)
    
    # Download data
    download_eobs_data(config)

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