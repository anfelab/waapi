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

:: Copy the Commands folder
if exist "%COMMANDS_SRC%" (
    xcopy "%COMMANDS_SRC%" "%TARGET_DIR%\%COMMANDS_SRC%" /E /I /Y
    echo Copied "%COMMANDS_SRC%" to "%TARGET_DIR%\%COMMANDS_SRC%"
) else (
    echo Source folder "%COMMANDS_SRC%" not found.
)

:: Copy the waapi-scripts folder
if exist "%WAAPI_SCRIPTS_SRC%" (
    xcopy "%WAAPI_SCRIPTS_SRC%" "%TARGET_DIR%\%WAAPI_SCRIPTS_SRC%" /E /I /Y
    echo Copied "%WAAPI_SCRIPTS_SRC%" to "%TARGET_DIR%\%WAAPI_SCRIPTS_SRC%"
) else (
    echo Source folder "%WAAPI_SCRIPTS_SRC%" not found.
)

endlocal


pause