@echo off

setlocal

call scripts\shutdown.bat
docker-compose build --no-cache
docker system prune -f

endlocal