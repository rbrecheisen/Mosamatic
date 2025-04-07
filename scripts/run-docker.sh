#!/bin/bash

export VERSION=$(cat VERSION)

scripts/shutdown.sh
docker-compose -f docker-compose-${VERSION}.yml up -d
docker-compose -f docker-compose-${VERSION}.yml logs -f