@echo off

setlocal

set /p VERSION=<VERSION

@REM call scripts\builddocker.bat

docker logout
type C:\\Users\\r.brecheisen\\dockerhub.txt | docker login --username brecheisen --password-stdin
docker push brecheisen/mosamatic-web-intel:%VERSION%

endlocal