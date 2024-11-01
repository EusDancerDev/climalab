#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
**Program Note**

- This program is an application of the `scan_ncfiles` method from the 
  `file_utils` module within the `xarray_utils` subpackage.
- It is designed to scan specified directories for netCDF (`.nc`) files,
  check their integrity if necessary, and generate a report of faulty files.
- The `scan_ncfiles` method offers various configurations for returning 
  file paths, directory paths, and integrity checks.

**Redistribution Notice**
- You may redistribute this program in any other directory as needed.
- However, keep in mind that it is designed to operate with absolute paths,
  so ensure that any paths provided are properly configured to reflect your system's directory structure.

**Main Functions and Subpackages Used**
- `scan_ncfiles` (from `file_utils`, part of the `xarray_utils` subpackage):
   The core function used to scan directories and check for `.nc` file integrity.
- `ncfile_integrity_status` (from `file_utils`, part of the `xarray_utils` subpackage):
   This function checks the integrity of `.nc` files and flags any issues.

The execution of the program is timed using the `program_exec_timer` method 
from the `time_handling` subpackage, which calculates the elapsed time of 
the execution of the program for performance analysis.
"""

#-----------------------#
# Import custom modules #
#-----------------------#

from pygenutils.time_handling.program_snippet_exec_timers import program_exec_timer
from filewise.xarray_utils.file_utils import scan_ncfiles

#-------------------#
# Define parameters #
#-------------------#

# Paths to be scanned #
path_obj = "/media/jonander/My_Basic/Dokumentuak"

# path_obj = [
#     "/media/jonander/My_Basic/Dokumentuak",
#     "/home/jonander/Documents/03-Ikasketak"
#     ]

#------------#
# Operations #
#------------#

# Initialise stopwatch #
program_exec_timer('start')

# Run program #
scan_ncfiles(path_obj)

# Stop the stopwatch and calculate full program execution time #
program_exec_timer('stop')
