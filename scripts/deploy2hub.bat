@echo off

setlocal

set /p VERSION=<VERSION

echo "Deployment version will be %VERSION%. Is that correct?"
pause

@REM Pushing to Git and tagging
git add -A && git commit -m "Release %VERSION%" && git push origin main
git tag -a %VERSION% -m "Release %VERSION%"
git push origin %VERSION%

docker logout
type C:\\Users\\r.brecheisen\\dockerhub.txt | docker login --username brecheisen --password-stdin
docker push brecheisen/mosamatic-nginx-intel:%VERSION%
docker push brecheisen/mosamatic-backend-intel:%VERSION%

endlocal