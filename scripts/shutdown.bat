@echo off

setlocal

set /p VERSION=<VERSION

if "%*"=="--production" (
    docker-compose -f docker-compose-prod.yml down --volumes --remove-orphans
) else (
    docker-compose down --volumes --remove-orphans
)

docker container prune -f
docker volume prune -f
docker system prune -f

endlocal