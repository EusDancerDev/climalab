#!/bin/bash
# Interdependent PyPI packages (aligned with pyproject.toml and climarraykit>=0.2.1)
"${PREFIX}/bin/pip" install -v \
  "climarraykit>=0.2.1" \
  "filewise>=3.14.0" \
  "pygenutils>=17.1.0" \
  "paramlib>=3.5.0"
