@echo off

setlocal

set /p VERSION=<VERSION

call scripts\build-docker.bat

docker logout
type C:\\Users\\r.brecheisen\\dockerhub.txt | docker login --username brecheisen --password-stdin
docker push brecheisen/mosamatic-web-intel:%VERSION%

endlocal