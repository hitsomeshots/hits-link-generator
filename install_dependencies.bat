@echo off
pip install aiohttp beautifulsoup4 pyperclip

if %errorlevel% equ 0 (
    echo Installation successful.
    echo Deleting this script...
    del "%~f0"
) else (
    echo Installation failed. Please check for errors.
)

pause
