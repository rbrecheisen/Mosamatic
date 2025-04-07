#!/bin/bash

export VERSION=$(cat VERSION)

echo "Deploying Mosamatic version ${VERSION} to DockerHub"
read -n 1 -s -r -p "Press any key to continue..."

docker logout
cat /Users/ralph/dockerhub.txt | docker login --username brecheisen --password-stdin
# docker push brecheisen/mosamatic-nginx-intel:${VERSION}
docker push brecheisen/mosamatic-web-intel:${VERSION}

endlocal