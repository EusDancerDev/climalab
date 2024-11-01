# climalab Changelog

All notable changes to this project will be documented in this file.

---

## [v3.0.0] - 2024-11-01

### Changed
- For all files contained in this package, relocate package names in the absolute imports

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
