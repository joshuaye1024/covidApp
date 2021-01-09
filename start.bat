@echo off & title Trileaf Technologies covidApp CLI

Rem check if python exists before proceeding
echo [46mWelcome to Trileaf Technologies' covidApp![0m
echo (C) Josh Ye 2021
echo.
echo [covidApp] Checking if python is installed...
goto :DOES_PYTHON_EXIST

:DOES_PYTHON_EXIST
python -V | find /v "Python" >NUL 2>NUL && (goto :PYTHON_DOES_NOT_EXIST)
python -V | find "Python"    >NUL 2>NUL && (goto :PYTHON_DOES_EXIST)
goto :EOF

:PYTHON_DOES_NOT_EXIST
echo Python is not installed on your system.
echo Now opeing the download URL.
start "" "https://www.python.org/downloads/windows/"
goto :EOF

:PYTHON_DOES_EXIST
:: This will retrieve Python 3.8.0 for example.
for /f "delims=" %%V in ('python -V') do @set ver=%%V
echo [covidApp] %ver% is installed, continuing...

echo.
echo [covidApp] Checking if database connection key is present in secure folder...

if exist %~dp0\res\secrets\db_credentials.txt (
    echo [covidApp] db_credentials.txt exists, server connection will be availible.
    set serverconnect=present
) else (
    echo [covidApp] db_credentials.txt does not exist, server connection will not be availible.
    set serverconnect=not present
    pause
    goto :EOF
)

echo.

CHOICE /T 5 /C YN /D Y /M "[covidApp] Welcome to covidApp cli. Server Connection is %serverconnect%. Continue? "
set _e=%ERRORLEVEL%
if %_e%==1 goto :taskselect
if %_e%==2 goto :EOF

echo Error
echo %_e%

goto :taskselect

:taskselect
echo.
echo Select a task:
echo =============
echo 1) Update server
echo 2) Grab current data (Online, Json source)
echo 3) Check API status (Online)
echo 4) Get latest covid Data Summary (text)

echo.
set /p op=Type option:
if "%op%"=="1" goto op1
if "%op%"=="2" goto op2
if "%op%"=="3" goto op3
if "%op%"=="4" goto op4

echo.
echo Nothing selected, ending.
pause
goto :EOF

:op1
echo.
set /p reg= [covidApp] Enter a region key (use 'all' to update all regions in the US):
echo.
echo Updating database with region %reg%...

echo.
python Import.py %reg% %op%
echo.
goto :checkIfRepeat
goto :EOF

:op2
echo.
set /p reg=[covidApp] Enter a region key (use 'all' to update all regions in the US):
echo.
echo Grabbing data for region %reg% from online API...
echo.

python Import.py %reg% %op%
echo.
goto :checkIfRepeat
goto :EOF

:op3
echo.
echo Checking status for online API...
echo.

python Import.py none %op%
echo.
goto :checkIfRepeat

goto :EOF

:op4
echo.
set /p reg=[covidApp] Enter a region key:
echo.
echo Getting summary for region %reg%...
echo.
python Import.py %reg% %op%

echo.
goto :checkIfRepeat
goto :EOF

:checkIfRepeat

CHOICE /T 5 /C YN /D N /M "[covidApp] Return to options list?"
set _e=%ERRORLEVEL%
if %_e%==1 goto :taskselect
if %_e%==2 goto :repeatexit

echo Error
echo %_e%

:repeatexit
echo.
echo [covidApp] exiting...
ping -n 2 127.0.0.1 > nul

goto :EOF
