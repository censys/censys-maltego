#!/usr/bin/env bash

PYTHON=$(which python3)

virtualenv censys_transforms -p "$PYTHON"
. censys_transforms/bin/active
censys_transforms/bin/pip install censys/censys_maltego