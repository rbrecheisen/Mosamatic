@echo off

setlocal

set /p VERSION=<VERSION

call scripts\shutdown.bat

del /f /q mosamatic\src\mosamatic\backend\app\migrations\0*.py

docker-compose build --no-cache --progress=plain
docker system prune -f

endlocal