#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

from pathlib import Path
from typing import Any

import cdsapi
import urllib3

#------------------------------------#
# Turn of insecure download warnings #
#------------------------------------#

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#-----------------------#
# Define main parameter #
#-----------------------#

c = cdsapi.Client()

#-------------------------#
# Define custom functions #
#-------------------------#

def download_data(product: str, output_file: str | Path, **kwargs: Any) -> None:
    """
    Download data from the Copernicus Climate Data Store (CDS).

    This function provides a simple interface to the CDS API for downloading
    climate data products. It handles the authentication, request formation,
    and file download process automatically.

    Parameters
    ----------
    product : str
        Name of the CDS product to be downloaded. Must match exactly with
        the product names available in the CDS catalogue (e.g., 
        'reanalysis-era5-single-levels', 'projections-cordex-domains-single-levels').
    output_file : str | Path
        Path to the file where the downloaded data will be stored. Can be
        a string path or a pathlib.Path object. The file extension should
        match the requested format.
    **kwargs : Any
        Additional parameters that define the specific data request. These
        vary by product but commonly include:
        - variable: List of variables to download
        - year: Year or list of years
        - month: Month or list of months
        - day: Day or list of days (for daily data)
        - time: Time or list of times (for sub-daily data)
        - area: Geographical area bounds [north, west, south, east]
        - format: Output format ('netcdf', 'grib', etc.)

    Returns
    -------
    None
        The function downloads the data to the specified file path and
        does not return any value.

    Raises
    ------
    cdsapi.api.DatasetError
        If the specified product name is not found in the CDS catalogue.
    cdsapi.api.RequestError  
        If the request parameters are invalid or incompatible.
    PermissionError
        If there are insufficient permissions to write to the output path.
    FileNotFoundError
        If the output directory does not exist.

    Examples
    --------
    >>> # Download ERA5 temperature data for a specific day
    >>> download_data(
    ...     product='reanalysis-era5-single-levels',
    ...     output_file='era5_temp_20200101.nc',
    ...     variable='2m_temperature',
    ...     year='2020',
    ...     month='01',
    ...     day='01',
    ...     time='12:00',
    ...     area=[60, -10, 50, 2],  # North, West, South, East
    ...     format='netcdf'
    ... )

    >>> # Download CORDEX climate projections
    >>> download_data(
    ...     product='projections-cordex-domains-single-levels',
    ...     output_file='cordex_projections.zip',
    ...     domain='europe',
    ...     experiment='rcp_8_5',
    ...     variable=['tas', 'pr'],
    ...     year=['2050', '2051'],
    ...     format='zip'
    ... )

    Notes
    -----
    - This function requires valid CDS API credentials to be configured
      (either via ~/.cdsapirc file or environment variables)
    - Large downloads may take considerable time and should be monitored
    - The CDS has usage limits and fair usage policies that should be respected
    - Some products may have restrictions on data availability periods
    """
    
    return c.retrieve(
        product,
        kwargs,
        output_file
    ).download()
