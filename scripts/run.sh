#!/bin/bash

if [ "${1}" == "" ]; then
    echo "Runs Mosamatic."
    echo "Usage: run.sh [--dev|--exe|--test|--docker]"
    exit 0
fi

export VERSION=$(cat VERSION)

if [ "${1}" == "--dev" ]; then
    cd mosamatic
    briefcase dev
elif [ "${1}" == "--exe" ]; then
    cd mosamatic
    rm -rf build/ dist/
    briefcase create
    briefcase build
    briefcase run
elif [ "${1}" == "--test" ]; then
    cd mosamatic
    briefcase dev --test
elif [ "${1}" == "--docker" ]; then
    scripts\shutdown.bat
    docker-compose -f docker-compose-prod.yml up -d
    docker-compose -f docker-compose-prod.yml logs -f
else
    echo "Unknown option ${1}"
fi