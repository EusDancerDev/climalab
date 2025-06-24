# climalab Changelog

All notable changes to this project will be documented in this file.

---

## [4.5.2] - 2025-06-25

### Changed (4.5.2)

#### **Supplementary Tools** (changing; 4.5.2)

- Module `auxiliary_functions.py`: remove spurious triple quotes at the end of the file (not a docstring).

---

## [4.5.1] - 2025-06-24

### Changed (4.5.1)

#### **General** (changing; 4.5.1)

- Update variable names:
  - Changes have been made in the original file `global_parameters.py` in the `paramlib` package.
  - These include abbreviation addressing.

| Module | Old variable name | New variable name |
|:------:|:-----------------:|:-----------------:|
| `netcdf_tools/cdo_tools.py` | `COMMON_DELIM_LIST` | `COMMON_DELIMITER_LIST` |
| `netcdf_tools/cdo_tools.py` | `TIME_FREQUENCIES_SHORT_1` | `TIME_FREQUENCIES_ABBREVIATED` |
| `netcdf_tools/cdo_tools.py` | `TIME_FREQUENCIES_SHORTER_1` | `TIME_FREQUENCIES_BRIEF` |
| `netcdf_tools/cdo_tools.py` | `BASIC_FOUR_RULES` | `BASIC_ARITHMETIC_OPERATORS` |
| `netcdf_tools/nco_tools.py` | `BASIC_FOUR_RULES` | `BASIC_ARITHMETIC_OPERATORS` |

---

## [4.5.0] - 2025-06-23

### Fixed (4.5.0)

#### **NetCDF Tools** (fixing; 4.5.0)

- Module `detect_faulty.py`:
  - **Docstring Corrections**:
    - Fix major inaccuracies in module docstring by correcting function descriptions to match actual implementations
  - **Function Descriptions**:
    - Correct `scan_ncfiles` description: function takes single path parameter, not "various configurations"
  - **Integrity Checking**:
    - Remove incorrect claims about optional integrity checking (it's automatic)
  - **Reference Fixes**:
    - Fix misleading reference to non-existent `ncfile_integrity_status` function
  - **Output Documentation**:
    - Add accurate "Output" section describing `faulty_netcdf_file_report.txt` generation

- Module `extract_basics.py`:
  - **Docstring Updates**:
    - Comprehensively update module docstring to accurately reflect imported function behaviour and program capabilities
  - **Documentation Corrections**:
    - Fix typos in documentation text
  - **Output File Names**:
    - Add specific output file names (latlon_bounds.txt, period_bounds.txt, time_formats.txt)
  - **Function Requirements**:
    - Clarify `extract_latlon_bounds` requires two rounding precision parameters
  - **Function Descriptions**:
    - Correct `program_exec_timer` description: returns formatted elapsed time string
  - **Integrity and Error Handling**:
    - Document automatic file integrity checking with error handling
    - Add "File Integrity and Error Handling" section explaining fault tolerance

### Added (4.5.0)

#### **NetCDF Tools** (adding; 4.5.0)

- **Comprehensive Nested List Support**: Enhanced defensive programming across NetCDF processing modules
  - Modules `cdo_tools.py` and `nco_tools.py`: **Already implemented**
    - Import `flatten_list` from `pygenutils.arrays_and_lists.data_manipulation` for robust nested list handling
    - Enhanced functions to handle arbitrarily deep nested list structures in file processing
    - Maintains backward compatibility with existing file list processing

### Changed (4.5.0)

#### **General** (changing; 4.5.0)

- **Modernisation Requirements Analysis**: Systematic assessment of type annotation and nested list support needs across modules

**Files Requiring Both `flatten_list` and PEP-604 Modernisation:**
- No additional files identified (NetCDF tools already modernised)

**Files Requiring PEP-604 Modernisation Only:**
- `meteorological/variables.py`: Already uses modern `float | np.ndarray` syntax - **No changes needed**
- `meteorological/weather_software.py`: Already uses modern type hints - **No changes needed**  
- `supplementary_tools/*.py`: Simple analysis modules - **Assessment needed**
  - Functions primarily use basic data types without complex list processing
  - May benefit from type hint improvements for consistency

**Files Already Modernised (No Changes Required):**
- `netcdf_tools/cdo_tools.py`: Modern `str | list[str]` syntax with `flatten_list` defensive programming
- `netcdf_tools/nco_tools.py`: Modern type hints with proper list handling
- `netcdf_tools/detect_faulty.py`: Simple program with basic types
- `netcdf_tools/extract_basics.py`: Simple program with basic types
- `data_analysis_projects_sample/src/data/*.py`: Download scripts with specific data handling, no nested list requirements

#### **NetCDF Tools** (changing; 4.5.0)

- **Already Completed**: Both `cdo_tools.py` and `nco_tools.py` modules have been modernised with:
  - PEP-604 union syntax: `str | list[str]` for file parameters
  - Defensive programming with `flatten_list` for nested list handling
  - Enhanced type safety and robustness for file processing operations

---

## [4.4.0] - 2025-05-09

### Fixed

#### **NetCDF Tools** (fixing; 4.4.0)

- Modules `cdo_tools.py` and `nco_tools.py`:
  - Improved system command execution to properly handle cases where command output isn't captured.

---

## [4.3.1] - 2025-05-02

### Changed (4.3.1)

#### **General** (changing; 4.3.1)

- Replace the deprecated `find_time_key` function with the new `find_dt_key` function in the following modules:
  - `netcdf_tools/cdo_tools.py`

---

## [4.3.0] - 2025-04-27

### Changed (4.3.0)

#### **General** (changing; 4.3.0)

- Modify the comment header `Import custom modules` to `Import project modules` in all modules having it.

#### **Data Analysis Projects Sample** (changing; 4.3.0)

For the following modules to download data from the CDS databases:

- `download_cordex.py`
- `download_eobs.py`
- `download_era5.py`
- `download_era5_land.py`

- Refactor all modules to download data from the CDS databases:
  - Reorganise import structure to be more direct, instead of using aliases.
  - Correct the import path to the `scan_ncfiles` function.

#### **NetCDF Tools** (changing; 4.3.0)

- Module `cdo_tools.py`: modify the constant `splitdelim` to `SPLIT_DELIM`.
- Module `detect_faulty.py`:
  - Convert all **constant names** under the header `Define parameters` to uppercase following Python naming conventions.
  - Reorganise imports to be more direct, instead of using aliases.

---

## [4.2.0] - 2025-04-25

### Changed (4.2.0)

#### **Meteorological** (changing; 4.2.0)

- Module `variables.py`:
  - Convert configuration constants to uppercase (e.g., `UNIT_CONVERSIONS_LIST`, `UNIT_CONVERTER_DICT`)
  - Formula constants remain in lowercase as implementation details

#### **NetCDF Tools** (changing; 4.2.0)

- Module `nco_tools.py`:
  - Convert all configuration constants to uppercase, including:
    - Command and progress message templates
    - Error message templates
    - Configuration lists and dictionaries
    - Command template dictionaries
    - The import of the constant `BASIC_FOUR_RULES` from `global_parameters.py` in the package `paramlib`,
      as the latter has recently been converted to uppercase.

- Module `cdo_tools.py`:
  - Convert all configuration constants to uppercase
  - Reorganise imports to be more direct by removing unnecessary aliases
  - Import constants and functions directly from their respective modules

---

## [4.1.0] - 2025-04-24

### Changed (4.1.0)

#### **General** (changing; 4.1.0)

- Refactored package import structure:
  - Replace direct imports with `__all__` definitions in package initiator files:
    - `climalab/__init__.py`
    - `climalab/data_analysis_projects_sample/src/__init__.py`
    - `climalab/data_analysis_projects_sample/src/data/__init__.py`
    - `climalab/netcdf_tools/__init__.py`
    - `climalab/meteorological/__init__.py`
    - `climalab/supplementary_tools/__init__.py`
  - Improved control over exported symbols when using 'from package import *'
  - Maintained consistent public API while following Python best practices

### Fixed (4.1.0)

#### **Meteorological** (fixing; 4.1.0)

- Module `weather_software.py`:
  - Correct the import paths for the functions `approach_value` and `week_range`.

---

## [4.0.0] - 2025-04-06

### Added (4.0.0)

#### **Data Analysis Projects Sample** (adding; 4.0.0)

- Created a new sample project structure for data analysis projects:
  - Added configuration-based approach for data downloads
  - Created YAML configuration files for different datasets:
    - `cordex_config.yaml`: configuration for CORDEX data
    - `eobs_config.yaml`: configuration for E-OBS data
    - `era5_config.yaml`: configuration for ERA5 data
    - `era5_land_config.yaml`: configuration for ERA5-Land data
  - Implemented Python scripts for downloading data:
    - `download_cordex.py`: script to download CORDEX data
    - `download_eobs.py`: script to download E-OBS data
    - `download_era5.py`: script to download ERA5 data
    - `download_era5_land.py`: script to download ERA5-Land data
  - Added file existence checking and validation in all download scripts
  - Implemented temporary directory for downloads and proper cleanup
  - Added comprehensive logging for tracking download progress

### Changed (4.0.0)

#### **General** (changing; 4.0.0)

- In order to improve the overall structure and readability of the codebase, the following new directories have been created:
  - `netcdf_tools/`
  - `meteorological/`

- Next, some modules originally in the top-level directory have been moved to new sub-packages:

| Module | Original Location | New Location | New module name |
|:------:|:-----------------:|:------------:|:---------------:|
| `cdo_tools.py` | `climalab/` | `climalab/netcdf_tools/` | `cdo_tools.py` |
| `nco_tools.py` | `climalab/` | `climalab/netcdf_tools/` | `nco_tools.py` |
| `extract_netcdf_basics.py` | `climalab/` | `climalab/netcdf_tools/` | `extract_basics.py` |
| `detect_faulty_ncfiles.py` | `climalab/` | `climalab/netcdf_tools/` | `detect_faulty.py` |
| `meteorological_variables.py` | `climalab/` | `climalab/meteorological/` | `variables.py` |
| `weather_software_file_creator.py` | `climalab/` | `climalab/meteorological/` | `weather_software.py` |
| `cds_tools.py` | `climalab/` | `climalab/data_analysis_projects_sample/src/data/` | `cds_tools.py` |

After these changes, absolute imports in all affected files have been updated accordingly.

---

## [3.3.0] - 2025-04-05

### Changed (3.3.0)

#### **General** (changing; 3.3.0)

- For the rest of the modules, perform several term replacements:
  - Update terminology from `Preformatted Strings` to `Template Strings` in headers and variables.
  - On that basis, rename name 'preformatted' to 'template' in headers and variables wherever necessary.
  - Update comments and variable names to replace `command` with `template` for better clarity in describing variables and constants that use empty `{}` for formatting.

### Fixed (3.3.0)

#### **CDO Tools** (fixing; 3.3.0)

- Rename the wrongly named function `cdo_periodic_statkit` to `cdo_periodic_statistics`.

#### **NCO Tools** (fixing; 3.3.0)

- Refactor it to improve command string naming conventions, based on the principles established in the `General` aspect.

---

## [3.2.8] - 2025-02-18

### Changed (3.2.8)

#### **CDO Tools** (changing; 3.2.8)

- Refactored terminology for consistency and clarity:
  - Renamed variable `calc_method` to `calc_proc` to align with the term "Calculation procedure" used in docstrings, ensuring consistency between code and documentation.
  - Renamed variable `remap_method` to `remap_proc` to match the terminology "Remapping procedure" in the docstring, enhancing clarity.
  - Substituted the word `method` with `procedure` in docstrings and variable names where it more accurately describes the approach or technique used.
  - Updated docstrings to consistently use "procedure" when referring to specific techniques or approaches within functions.
  - Ensured that the term "method" is retained only when referring to class method calls, maintaining accurate terminology.
  - Improved overall code readability and maintainability by aligning variable names with their documented purposes.

#### **General** (changing; 3.2.8)

- For the rest of the modules, perform several term replacements:
  - Replace `method` with `procedure` to more accurately describe the approach or technique used in functions, except when referring to class method calls.
  - Replace `action` with `procedure` to align with the context of operations being performed.

---

## [3.2.0] - 2024-11-03

### Added (3.2.0)

#### **General** (adding; 3.2.0)

- Added `__init__.py` files to all first-level and deeper sub-packages for enhanced import access

### Removed (3.2.0)

#### **General** (removing; 3.2.0)

- Remove the redundant import of the deprecated and removed `parameters_and_constants` module in all affected modules.

---

## [3.0.0] - 2024-11-01

### Changed (3.0.0)

#### **General** (changing; 3.0.0)

- For all files contained in this package, package names in the absolute imports have been relocated

---

## [2.1.0] - Initial Release - 2024-10-28

### Added (2.1.0)

#### **General** (adding; 2.1.0)

- The following **sub-packages** and `modules` were added:
  - **data_downloads**: includes scripts for automated downloads from CORDEX, EOBS, and ERA5 repositories.
  - **supplementary_tools**: additional tools for visualisations, bias correction, and statistical analysis in climate data.
  - `cdo_tools`: provides climate data operators for processing and analyzing climate datasets.
  - `cds_tools`: facilitates data downloads from the Copernicus Climate Data Store (CDS).
  - `detect_faulty_ncfiles`: detects and reports issues in netCDF files.
  - `extract_netcdf_basics`: extracts essential data from netCDF files for further processing.
  - `nco_tools`: utilities for interacting with the NCO climate tools.
