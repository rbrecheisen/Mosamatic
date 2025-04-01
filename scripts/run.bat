@echo off

setlocal

if "%*"=="" (
    echo "Runs Mosamatic"
    echo "Usage: run.bat [--dev|--build|--test|--docker|--docker-prod]"
    exit /b 1
)

set /p VERSION=<VERSION

for %%A in (%*) do (
    if /I "%%A"=="--dev" (
        set START_DIR=%CD%
        cd mosamatic
        call briefcase dev
        cd %START_DIR%

    ) else if /I "%%A"=="--build" (
        set START_DIR=%CD%
        cd mosamatic
        del /q "build" "dist"
        call briefcase create --no-input
        call briefcase build
        call briefcase run
        cd %START_DIR%

    ) else if /I "%%A"=="--test" (
        set START_DIR=%CD%
        cd mosamatic
        call briefcase dev --test
        cd %START_DIR%

    ) else if /I "%%A"=="--docker" (
        set /p VERSION=<VERSION
        call scripts\shutdown.bat
        docker-compose build --no-cache
        docker system prune -f
        docker-compose up -d && docker-compose logs -f

    ) else if /I "%%A"=="--docker-prod" (
        set /p VERSION=<VERSION
        call scripts\shutdown.bat --docker-prod
        docker-compose -f docker-compose-prod.yml build --no-cache
        docker system prune -f
        docker-compose -f docker-compose-prod.yml up -d
        docker-compose -f docker-compose-prod.yml logs -f

    )
)

endlocal