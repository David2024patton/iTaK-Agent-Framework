@echo off
REM iTaK CLI shim for Windows
REM This script is added to PATH and launches the bundled CLI

setlocal

set "ITAK_APP_DIR=%LOCALAPPDATA%\Programs\itak-agent"
if exist "%ProgramFiles%\iTaK Agent" (
    set "ITAK_APP_DIR=%ProgramFiles%\iTaK Agent"
)

set "RESOURCES_DIR=%ITAK_APP_DIR%\resources"

REM Check if app is installed
if not exist "%ITAK_APP_DIR%" (
    echo Error: iTaK Agent not found at %ITAK_APP_DIR%
    echo Please install iTaK Agent first.
    exit /b 1
)

REM Find Python
where python3 >nul 2>&1
if %ERRORLEVEL% == 0 (
    set "PYTHON_CMD=python3"
) else (
    where python >nul 2>&1
    if %ERRORLEVEL% == 0 (
        set "PYTHON_CMD=python"
    ) else (
        where py >nul 2>&1
        if %ERRORLEVEL% == 0 (
            set "PYTHON_CMD=py"
        ) else (
            echo Error: Python not found. Please install Python 3.10 or higher.
            exit /b 1
        )
    )
)

REM Set PYTHONPATH
set "PYTHONPATH=%RESOURCES_DIR%\python-src;%PYTHONPATH%"

REM Run the CLI
cd /d "%RESOURCES_DIR%\python-src"
"%PYTHON_CMD%" -m itak.cli.cli %*
