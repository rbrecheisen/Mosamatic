@echo off

setlocal

set /p VERSION=<VERSION

call scripts\shutdown.bat

docker volume rm mosamatic_data mosamatic_postgres_data

docker-compose -f docker-compose-%VERSION%.yml up -d --force-recreate
docker-compose -f docker-compose-%VERSION%.yml logs -f

endlocal