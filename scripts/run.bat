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
    ) else if /I "%%A"=="--build" (
        set START_DIR=%CD%
        cd mosamatic
        call briefcase run
        cd %START_DIR%
    ) else if /I "%%A"=="--usage" (
        echo "Usage: run.bat [--build|--test|--docker|--delete-db]"
    ) else if /I "%%A"=="--delete-db" (
        del /q mosamatic\src\mosamatic\backend\db.sqlite3
        set START_DIR=%CD%
        cd mosamatic
        call briefcase dev
        cd %START_DIR%
    )
)

endlocal