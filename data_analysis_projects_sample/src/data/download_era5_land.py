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
def set_up_logging():
    """Set up logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
logger = logging.getLogger(__name__)

# Load configuration #
def load_config(config_path):
    """Load the configuration file."""
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        logger.error(f"Error loading configuration file: {e}")
        sys.exit(1)

# Validate configuration #
def validate_config(config):
    """Validate the configuration parameters."""
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
def return_file_extension(config):
    """Return the file extension based on the file format."""
    extension_idx = find_substring_index(config['available_formats'], config['file_format'])
    
    if extension_idx == -1:
        raise ValueError(f"Unsupported file format. Choose from '{config['available_formats']}'.")
    else:
        extension = config['available_extensions'][extension_idx]
        return extension

# Download data #
#---------------#

def download_era5_land_data(config):
    """Download the ERA5-Land data using the CDS API."""
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

def main():
    """Main function."""
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