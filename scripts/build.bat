@echo off

setlocal

set /p VERSION=<VERSION

call scripts\shutdown.bat
docker-compose build --no-cache
docker system prune -f

endlocal