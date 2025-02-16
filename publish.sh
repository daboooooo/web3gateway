#!/bin/bash
# Clean previous builds
rm -rf build/ dist/ *.egg-info

# Build package
python -m build

# Check package
python -m twine check dist/*

# Upload to PyPI
python -m twine upload dist/*
