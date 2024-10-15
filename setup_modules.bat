python -m pip install --upgrade pip
python -m pip install waapi-client
python -m pip install pyperclip
python -m pip install tk
python -m pip install soundfile
python -m pip install pyloudnorm
python -m pip install pydub
@echo off
setlocal

:: Define the source folders (adjust paths as necessary if they're not in the same directory as the batch file)
set COMMANDS_SRC=Commands
set WAAPI_SCRIPTS_SRC=waapi-scripts

:: The %APPDATA% environment variable points to the AppData\Roaming folder of the current user
set TARGET_DIR=%APPDATA%\Audiokinetic\Wwise\Add-ons

:: Check if the target directory exists, create if it doesn't
if not exist "%TARGET_DIR%" (
    mkdir "%TARGET_DIR%"
    echo Folder created: %TARGET_DIR%
) else (
    echo Folder already exists: %TARGET_DIR%
)

:: Create a symbolic link for the Commands folder
if exist "%COMMANDS_SRC%" (
    mklink /D "%TARGET_DIR%\%COMMANDS_SRC%" "%COMMANDS_SRC%"
    echo Created symbolic link for "%COMMANDS_SRC%" in "%TARGET_DIR%"
) else (
    echo Source folder "%COMMANDS_SRC%" not found.
)

:: Create a symbolic link for the waapi-scripts folder
if exist "%WAAPI_SCRIPTS_SRC%" (
    mklink /D "%TARGET_DIR%\%WAAPI_SCRIPTS_SRC%" "%WAAPI_SCRIPTS_SRC%"
    echo Created symbolic link for "%WAAPI_SCRIPTS_SRC%" in "%TARGET_DIR%"
) else (
    echo Source folder "%WAAPI_SCRIPTS_SRC%" not found.
)

endlocal

pause
