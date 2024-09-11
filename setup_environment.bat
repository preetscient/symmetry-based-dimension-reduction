@echo off

REM Check for GAP installation
where gap >nul 2>nul
if %errorlevel% neq 0 (
    echo GAP is not installed. Please install it from https://www.gap-system.org/
    exit /b 1
)

REM Check for Conda installation
where conda >nul 2>nul
if %errorlevel% neq 0 (
    echo Conda is not installed. Please install Miniconda or Anaconda from https://docs.conda.io/en/latest/miniconda.html
    exit /b 1
)

REM Create and activate Conda environment
conda env create -f environment.yml
call conda activate myenv

REM Optionally run application or additional steps here
REM start your_application.exe

echo Setup complete. You can now run your application.
