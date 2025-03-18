@echo off

setlocal

if "%*"=="" (
    set START_DIR=%CD%
    cd mosamatic
    call briefcase dev
    cd %START_DIR%
)

for %%A in (%*) do (
    if /I "%%A"=="--docker" (
        set /p VERSION=<VERSION
        docker-compose up -d && docker-compose logs -f
    ) else if /I "%%A"=="--test" (
        set START_DIR=%CD%
        cd mosamatic
        call briefcase dev --test
        cd %START_DIR%
    ) else if /I "%%A"=="--usage" (
        echo "Usage: run.bat [--test|--docker]"
    )
)

endlocal