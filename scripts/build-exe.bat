@echo off

setlocal

set /p VERSION=<VERSION

set START_DIR=%CD%
cd mosamatic
del /q "build" "dist"
call briefcase create
call briefcase build
cd %START_DIR%

endlocal