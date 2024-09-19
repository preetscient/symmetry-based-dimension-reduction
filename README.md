dsdp_lumping
==============================

Installation
------------

## 1. Install GAP
Make sure GAP is installed on your system. Instructions can be found [here](https://www.gap-system.org/install/).

## 2. Install Conda
If Conda is not installed, download and install Miniconda or Anaconda from [here](https://docs.conda.io/en/latest/miniconda.html).

## 3. Download Files
Download the necessary files for your application, including the setup script and `environment.yml`.

## macOS and Linux

**Run the Setup Script**: Open a terminal and execute the setup script to create and activate the Conda environment. Make sure you have execution permissions for the script.

```bash
chmod +x setup_environment.sh
./setup_environment.sh

```
## Windows
Run the Setup Script: Open Command Prompt or PowerShell and execute the setup script `setup_environment.bat`.

If using a Bash script in a Windows environment, such as Git Bash or WSL (Windows Subsystem for Linux), use:

`bash setup_environment.sh`

## 4. Load your network data
Save your network data as any delimited file in /data/external/5_user_data. 

This should include source nodes in the first column and target nodes in the second column.
Any subsequent columns are ignored by the processing script.

## 5. Run the code.
After setting up the environment, you can run the Python script main.py directly. Follow the instructions below:


### For Windows Users
1. Open Command Prompt or PowerShell.
2. Navigate to the directory containing main.py.
3. Run the script using the command:
`python main.py`

### For macOS and Linux Users
1. Open a terminal.
2. Navigate to the directory containing main.py.
3. Run the script with:
`python main.py`


