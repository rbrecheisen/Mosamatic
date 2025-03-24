@echo off

setlocal

if "%*"=="" (
    set START_DIR=%CD%
    cd mosamatic
    del /q "build" "dist"
    call briefcase create
    call briefcase build
    cd %START_DIR%
)

for %%A in (%*) do (
    if /I "%%A"=="--docker" (
        set /p VERSION=<VERSION
        call scripts\shutdown.bat
        docker-compose build --no-cache
        docker system prune -f
    ) else if /I "%%A"=="--help" (
        echo "Usage: build.bat [--help|--docker]"
    )
)

endlocal