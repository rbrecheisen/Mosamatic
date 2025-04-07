@echo off

setlocal

set /p VERSION=<VERSION

set START_DIR=%CD%
cd mosamatic
call briefcase dev
cd %START_DIR%

endlocal