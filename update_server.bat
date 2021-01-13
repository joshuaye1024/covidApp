@if (@CodeSection == @Batch) @then


@echo off

rem Use %SendKeys% to send keys to the keyboard buffer
set SendKeys=CScript //nologo //E:JScript "%~F0"

if exist %~dp0\res\secrets\db_credentials.txt (
    echo [profile] Server connection is available, proceeding.
    set serverconnect=present
) else (
    echo [profile] Server connection is not available, proceeding.
    pause 
    goto :EOF
)

start /B covidApp.bat

rem wait 7 seconds to get to the selection screen
ping -n 8 -w 1 127.0.0.1 > NUL

rem select option 1
%SendKeys% "1{ENTER}"

ping -n 16 -w 1 127.0.0.1 > NUL
%SendKeys% "all{ENTER}"

goto :EOF

@end

var WshShell = WScript.CreateObject("WScript.Shell");
WshShell.SendKeys(WScript.Arguments(0));