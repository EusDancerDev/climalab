#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

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

def download_data(product, output_file, **kwargs):
    
    """ Download data from the climate data store

    Parameters
    ----------
    product: str
        Name of the product to be downloaded.
    output_file: str or Path
        Path to the file where the data will be stored.
    kwargs:
        Parameters that define the request of the product (e.g. variable, year,
        month, etc.).

    Returns
    -------
    Data download procedure
    """

    return c.retrieve(
        product,
        kwargs,
        output_file
    )
