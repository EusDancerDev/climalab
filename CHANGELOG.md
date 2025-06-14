# climalab Changelog

All notable changes to this project will be documented in this file.

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
