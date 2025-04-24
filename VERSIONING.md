# Versioning Scheme

This document explains the versioning scheme used in the climalab project.

## Overview

The climalab project follows the [Semantic Versioning](https://semver.org/) (SemVer) scheme with version numbers in the format `MAJOR.MINOR.PATCH`:

- **MAJOR** version: Incremented when making incompatible API changes
- **MINOR** version: Incremented when adding functionality in a backward-compatible manner
- **PATCH** version: Incremented when making backward-compatible bug fixes

## Starting Version

The project started at version 2.1.0 rather than 0.1.0 because:

1. Significant functionality was already developed before formal versioning began
2. The codebase had reached a level of maturity that warranted a "version 2" designation
3. This approach avoids the perception of "early development" that version 0.x might convey

## Version History

The project has evolved through the following major versions:

- **2.1.0**: Initial release with core functionality
- **3.0.0**: Major refactoring with package name relocation
- **3.2.0**: Added `__init__.py` files and removed deprecated imports
- **3.2.8**: Terminology refactoring for consistency and clarity
- **3.3.0**: Improved naming conventions across modules

## Version Increment Rules

- **MAJOR** version (e.g., 2.1.0 → 3.0.0): Incremented when making significant changes that might break backward compatibility
- **MINOR** version (e.g., 3.0.0 → 3.2.0): Incremented when adding new features that maintain backward compatibility
- **PATCH** version (e.g., 3.2.0 → 3.2.8): Incremented for bug fixes and minor improvements

## Future Versioning

As the project continues to evolve, we will maintain this semantic versioning approach to provide clear information about the nature of changes between versions.
