@echo off

setlocal

if "%*"=="" (
    echo "Runs Mosamatic"
    echo "Usage: run.bat [--dev|--exe|--test|--docker]"
    exit /b 1
)

set /p VERSION=<VERSION

for %%A in (%*) do (
    if /I "%%A"=="--dev" (
        set START_DIR=%CD%
        cd mosamatic
        call briefcase dev
        cd %START_DIR%

    ) else if /I "%%A"=="--exe" (
        set START_DIR=%CD%
        cd mosamatic
        del /q "build" "dist"
        call briefcase create
        call briefcase build
        call briefcase run
        cd %START_DIR%

    ) else if /I "%%A"=="--test" (
        set START_DIR=%CD%
        cd mosamatic
        call briefcase dev --test
        cd %START_DIR%

    ) else if /I "%%A"=="--docker" (
        call scripts\shutdown.bat
        docker-compose -f docker-compose-prod.yml up -d
        docker-compose -f docker-compose-prod.yml logs -f
    )
)

endlocal