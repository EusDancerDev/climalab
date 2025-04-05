# climalab

**climalab*- is a Python toolkit designed to facilitate climate data analysis and manipulation, including tools for data extraction, processing, and visualization. It leverages external tools and standards like CDO and CDS to streamline workflows for climate-related research.

## Features

- **Data Downloads**:
  - Scripts for downloading data from climate data repositories (e.g., CORDEX, EOBS, ERA5).
- **Faulty NetCDF Detection**:
  - Tools to identify and report issues with netCDF files.
- **Data Extraction and Conversion**:
  - Utilities for extracting key information from netCDF files and converting between formats.
- **Supplementary Analysis Tools**:
  - Additional tools for plotting, bias correction, and statistical analysis.

---

## Installation Guide

### Dependency Notice

Before installing, please ensure the following dependencies are available on your system:

- **Required Third-Party Libraries**: common dependencies include the latest versions of the following:
  - numpy
  - pandas
  - scipy

  - You can install them via pip:

    ```bash
    pip3 install numpy pandas scipy
    ```

  - Alternatively, you can install them via Anaconda. Currenlty, the recommended channel from where to install for best practices is `conda-forge`:

    ```bash
    conda install -c conda-forge numpy pandas scipy
    ```

- **Other Internal Packages**: these are other packages created by the same author. To install them as well as the required third-party packages, refer to the README.md document of the corresponding package:
  - filewise
  - paramlib
  - pygenutils

**Note**: In the future, this package will be available via PyPI and Anaconda, where dependencies will be handled automatically.

### Unconventional Installation Instructions

Until this package is available on PyPI or Anaconda, please follow these steps:

1. **Clone the Repository**: Download the repository to your local machine by running:

   ```bash
   git clone https://github.com/EusDancerDev/climalab.git
   ```

2. **Check the Latest Version**: Open the `CHANGELOG.md` file in the repository to see the latest version information.

3. **Build the Package**: Navigate to the repository directory and run:

   ```bash
   python setup.py sdist
   ```

   This will create a `dist/` directory containing the package tarball.

4. **Install the Package**:
   - Navigate to the `dist/` directory.
   - Run the following command to install the package:

     ```bash
     pip3 install climalab-<latest_version>.tar.gz
     ```

     Replace `<latest_version>` with the version number from `CHANGELOG.md`.

**Note**: Once available on PyPI and Anaconda, installation will be simpler and more conventional.

---

### Package Updates

To stay up-to-date with the latest version of this package, follow these steps:

1. **Check the Latest Version**: Open the `CHANGELOG.md` file in this repository to see if a new version has been released.

2. **Pull the Latest Version**:
   - Navigate to the directory where you initially cloned the repository.
   - Run the following command to update your local copy:

     ```bash
     git pull origin main
     ```

This will download the latest changes from the main branch of the repository. After updating, you may need to rebuild and reinstall the package as described in the [Installation Guide](#installation-guide) above.
