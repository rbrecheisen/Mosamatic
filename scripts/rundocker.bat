@echo off

setlocal

set /p VERSION=<VERSION

docker-compose -f docker-compose-%VERSION%.yml up -d
docker-compose -f docker-compose-%VERSION%.yml logs -f

endlocal