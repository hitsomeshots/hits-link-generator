@echo off
pip install requests

if %errorlevel% equ 0 (
    echo Installation successful.
    echo Deleting this script...
    del "%~f0"
) else (
    echo Installation failed. Please check for errors.
)

pause