@echo off

setlocal

set /p VERSION=<VERSION

set START_DIR=%CD%
cd mosamatic
call briefcase run
cd %START_DIR%

endlocal