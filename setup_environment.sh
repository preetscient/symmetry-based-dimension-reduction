#!/bin/bash

if ! command -v gap &> /dev/null
then
    echo "GAP is not installed. Please install it from https://www.gap-system.org/"
    exit 1
fi

# Check if Conda is installed
if ! command -v conda &> /dev/null; then
    echo "Conda is not installed. Please install Miniconda or Anaconda from https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

# Create and activate the Conda environment
ENV_NAME="myenv"

if ! conda env list | grep -q "^${ENV_NAME} "; then
    echo "Creating Conda environment..."
    conda env create -f environment.yml
fi

echo "Activating Conda environment..."
conda activate ${ENV_NAME}

# Optionally, you can run your application or additional setup steps here
# ./your_application

echo "Setup complete. You can now run your application."

