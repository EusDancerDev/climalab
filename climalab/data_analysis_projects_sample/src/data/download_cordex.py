#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script to download CORDEX data using the configuration file.
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

#------------------#
# Define functions #
#------------------#

# Pure backend functions #
#------------------------#

# Set up logging #
def set_up_logging() -> None:
    """
    Set up logging configuration for the CORDEX download script.
    
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
    Load the CORDEX configuration file from the specified path.
    
    Reads and parses a YAML configuration file containing parameters
    for CORDEX data download including domains, scenarios, models,
    and output settings.
    
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
    >>> config = load_config('config/cordex_config.yaml')
    >>> print(config['domain'])
    'europe'
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
    Validate that all required CORDEX configuration parameters are present and valid.
    
    Performs comprehensive validation of the configuration dictionary to ensure
    all required parameters are present and their values are within acceptable
    ranges for the CORDEX data download.
    
    Parameters
    ----------
    config : dict[str, Any]
        Configuration dictionary containing CORDEX download parameters.
        Must include required fields such as domain, RCP scenario, resolutions,
        model names, and file format specifications.
    
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
    >>> config = {'domain': 'europe', 'rcp': 'rcp_8_5', ...}
    >>> validate_config(config)  # Validates successfully
    >>> 
    >>> invalid_config = {'domain': 'invalid_domain'}
    >>> validate_config(invalid_config)  # Logs error and exits
    """
    required_params = [
        'project_name', 'domain', 'rcp', 'h_resolution', 't_resolution',
        'variable_list', 'gcm', 'rcm', 'ensemble', 'file_format', 'raw_input_data_dir'
    ]
    
    for param in required_params:
        if param not in config:
            logger.error(f"Missing required parameter: {param}")
            sys.exit(1)
    
    # Validate domain
    if config['domain'].lower() not in [d.lower() for d in config['available_domains']]:
        logger.error(f"Invalid domain: {config['domain']}")
        sys.exit(1)
    
    # Validate RCP
    if config['rcp'].lower() not in [r.lower() for r in config['available_rcps']]:
        logger.error(f"Invalid RCP: {config['rcp']}")
        sys.exit(1)
    
    # Validate resolutions
    if config['h_resolution'] not in config['available_h_resolutions']:
        logger.error(f"Invalid horizontal resolution: {config['h_resolution']}")
        sys.exit(1)
    
    if config['t_resolution'] not in config['available_t_resolutions']:
        logger.error(f"Invalid temporal resolution: {config['t_resolution']}")
        sys.exit(1)
    
    # Validate GCM and RCM
    if config['gcm'].lower() not in [g.lower() for g in config['available_gcms']]:
        logger.error(f"Invalid GCM: {config['gcm']}")
        sys.exit(1)
    
    if config['rcm'].lower() not in [r.lower() for r in config['available_rcms']]:
        logger.error(f"Invalid RCM: {config['rcm']}")
        sys.exit(1)
    
    # Validate file format
    if config['file_format'] not in config['available_formats']:
        logger.error(f"Invalid file format: {config['file_format']}")
        sys.exit(1)

# Get date range #
def get_date_range(config: dict[str, Any]) -> tuple[str, str]:
    """
    Determine the appropriate date range based on the RCP scenario.
    
    Extracts the start and end years for data download based on the
    specified RCP scenario (evaluation, historical, or future projections).
    
    Parameters
    ----------
    config : dict[str, Any]
        Configuration dictionary containing RCP scenario and available
        year ranges for different experiment types.
    
    Returns
    -------
    tuple[str, str]
        A tuple containing (start_year, end_year) as strings.
        
    Examples
    --------
    >>> config = {'rcp': 'historical', 'hist_start_ys': ['1950'], 'hist_end_ys': ['2005']}
    >>> start, end = get_date_range(config)
    >>> print(f"Date range: {start} to {end}")
    Date range: 1950 to 2005
    """
    if config['rcp'].lower() == 'evaluation':
        return config['eval_start_ys'][0], config['eval_end_ys'][-1]
    elif config['rcp'].lower() == 'historical':
        return config['hist_start_ys'][0], config['hist_end_ys'][-1]
    else:
        return config['rcp_all_start_ys'][0], config['rcp_all_end_ys'][-1]

# Download data #
#---------------#

def download_cordex_data(config: dict[str, Any]) -> None:
    """
    Download CORDEX climate data using the CDS API based on configuration parameters.
    
    This function handles the complete CORDEX data download workflow including
    parameter preparation, file checking, downloading via CDS API, and file
    organisation. It includes robust error handling and avoids duplicate downloads.
    
    Parameters
    ----------
    config : dict[str, Any]
        Complete configuration dictionary containing all necessary parameters
        for CORDEX data download including domain, models, variables, temporal
        settings, and file paths.
    
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
    - Checks for existing files to avoid unnecessary re-downloads
    - Validates downloaded files using netCDF integrity checking
    - Automatically organises files in the specified directory structure
    - Cleans up temporary files after successful completion
    
    Examples
    --------
    >>> config = load_config('cordex_config.yaml')
    >>> download_cordex_data(config)  # Downloads data according to config
    """
    # Get date range
    start_year, end_year = get_date_range(config)
    
    # Prepare the request parameters
    request_params = {
        'domain': config['domain'].lower(),
        'gcm': config['gcm'].lower(),
        'rcm': config['rcm'].lower(),
        'ensemble': config['ensemble'],
        'horizontal_resolution': config['h_resolution'],
        'temporal_resolution': config['t_resolution'],
        'variable': config['variable_list'],
        'year': [str(year) for year in range(int(start_year), int(end_year) + 1)],
        'format': config['file_format']
    }
    
    # Add RCP scenario if not evaluation or historical
    if config['rcp'].lower() not in ['evaluation', 'historical']:
        request_params['rcp'] = config['rcp'].lower()
    
    # Create temporary output directory
    temp_output_dir = Path(os.getcwd()) / "temp_downloads"
    make_directories(temp_output_dir)
    
    # Generate output filename using custom format
    output_file_name = f"{config['dataset_lower']}-{config['gcm'].lower()}-{config['rcm'].lower()}-{config['ensemble']}-"\
                       f"{config['h_resolution']}-{config['t_resolution']}-{start_year}.{config['file_format']}"
    
    output_file = temp_output_dir / output_file_name
    
    # Check if the file already exists in the destination directory
    dest_dir = Path(config['raw_input_data_dir'])
    existing_files = find_files(f"*{output_file_name}*", search_path=str(dest_dir), match_type="glob")
    
    if existing_files:
        logger.info(f"File {output_file_name} already exists in {dest_dir}")
        
        # Check if the existing file is valid
        num_faulty_ncfiles = scan_ncfiles(config['codes_dir'])
        
        if num_faulty_ncfiles:
            logger.info(f"Found {num_faulty_ncfiles} faulty files, re-downloading...")
            # Download the data
            try:
                logger.info(f"Downloading CORDEX data to {output_file}")
                download_data(
                    config['product_name'],
                    str(output_file),
                    **request_params
                )
                logger.info("Download completed successfully")
                
                # Move the downloaded file to the raw_input_data_dir
                logger.info(f"Moving downloaded files to {config['raw_input_data_dir']}")
                move_files(config['file_format'], 
                          input_directories=str(temp_output_dir), 
                          destination_directories=config['raw_input_data_dir'],
                          match_type='ext')
            except Exception as e:
                logger.error(f"Error downloading data: {e}")
                sys.exit(1)
        else:
            logger.info("Existing files are valid, skipping download")
    else:
        # File doesn't exist, download it
        try:
            logger.info(f"Downloading CORDEX data to {output_file}")
            download_data(
                config['product_name'],
                str(output_file),
                **request_params
            )
            logger.info("Download completed successfully")
            
            # Move the downloaded file to the raw_input_data_dir
            logger.info(f"Moving downloaded files to {config['raw_input_data_dir']}")
            move_files(config['file_format'], 
                      input_directories=str(temp_output_dir), 
                      destination_directories=config['raw_input_data_dir'],
                      match_type='ext')
        except Exception as e:
            logger.error(f"Error downloading data: {e}")
            sys.exit(1)
    
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
    Main function to orchestrate the CORDEX data download process.
    
    Loads configuration, validates parameters, and initiates the download
    process for CORDEX climate projection data from the CDS.
    
    Returns
    -------
    None
    """
    # Get the configuration file path
    script_dir = Path(__file__).parent.parent.parent
    config_path = script_dir / 'config' / 'cordex_config.yaml'
    
    # Load and validate configuration
    config = load_config(config_path)
    validate_config(config)
    
    # Download data
    download_cordex_data(config)

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

