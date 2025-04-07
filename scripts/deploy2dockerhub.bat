@echo off

setlocal

set /p VERSION=<VERSION

echo "Deploying Mosamatic version %VERSION% to DockerHub."
echo "Is that correct?"
pause

docker logout
type C:\\Users\\r.brecheisen\\dockerhub.txt | docker login --username brecheisen --password-stdin
docker push brecheisen/mosamatic-web-intel:%VERSION%

endlocal