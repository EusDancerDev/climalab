# climalab Changelog

All notable changes to this project will be documented in this file.

---

## [v3.2.8] - 2025-02-18

### Changed

**CDO tools**

- Refactored terminology for consistency and clarity:
  - Renamed variable `calc_method` to `calc_proc` to align with the term "Calculation procedure" used in docstrings, ensuring consistency between code and documentation.
  - Renamed variable `remap_method` to `remap_proc` to match the terminology "Remapping procedure" in the docstring, enhancing clarity.
  - Substituted the word `method` with `procedure` in docstrings and variable names where it more accurately describes the approach or technique used.
  - Updated docstrings to consistently use "procedure" when referring to specific techniques or approaches within functions.
  - Ensured that the term "method" is retained only when referring to class method calls, maintaining accurate terminology.
  - Improved overall code readability and maintainability by aligning variable names with their documented purposes.

**General**
- For the rest of the modules, perform several term replacements:
  - Replace `method` with `procedure` to more accurately describe the approach or technique used in functions, except when referring to class method calls.
  - Replace `action` with `procedure` to align with the context of operations being performed.

---

## [v3.2.0] - 2024-11-03

### Added

- Added `__init__.py` files to all first-level and deeper sub-packages for enhanced import access

### Changed

- Remove the redundant import of the deprecated and removed `parameters_and_constants` module in all affected modules.

---

## [v3.0.0] - 2024-11-01

### Changed
- For all files contained in this package, package names in the absolute imports have been relocated

---

## [2.1.0] - Initial Release - 2024-10-28

### Added
- The following **sub-packages** and `modules` were added:
	- **data_downloads**: includes scripts for automated downloads from CORDEX, EOBS, and ERA5 repositories.
	- **supplementary_tools**: additional tools for visualizations, bias correction, and statistical analysis in climate data.
	- `cdo_tools`: provides climate data operators for processing and analyzing climate datasets.
	- `cds_tools`: facilitates data downloads from the Copernicus Climate Data Store (CDS).
	- `detect_faulty_ncfiles`: detects and reports issues in netCDF files.
	- `extract_netcdf_basics`: extracts essential data from netCDF files for further processing.
	- `nco_tools`: utilities for interacting with the NCO climate tools.
