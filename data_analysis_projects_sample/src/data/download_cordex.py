#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script to download CORDEX data using the configuration file.
"""

#----------------#
# Import modules #
#----------------#

import os
import sys
import yaml
import logging
from pathlib import Path

#-----------------------#
# Import custom modules #
#-----------------------#

from cds_tools import download_data
from filewise.file_operations import ops_handler
from filewise.file_operations import scan_ncfiles
from pygenutils.time_handling.program_snippet_exec_timers import program_exec_timer

# Create aliases #
#----------------#

make_directories = ops_handler.make_directories
move_files = ops_handler.move_files
find_files = ops_handler.find_files

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
def get_date_range(config):
    """Get the date range based on the RCP scenario."""
    if config['rcp'].lower() == 'evaluation':
        return config['eval_start_ys'][0], config['eval_end_ys'][-1]
    elif config['rcp'].lower() == 'historical':
        return config['hist_start_ys'][0], config['hist_end_ys'][-1]
    else:
        return config['rcp_all_start_ys'][0], config['rcp_all_end_ys'][-1]

# Download data #
#---------------#

def download_cordex_data(config):
    """Download the CORDEX data using the CDS API."""
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

def main():
    """Main function."""
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

