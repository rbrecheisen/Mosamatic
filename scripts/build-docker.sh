#!/bin/bash

export VERSION=$(cat VERSION)

scripts/shutdown.sh

docker-compose build --no-cache
docker system prune -f