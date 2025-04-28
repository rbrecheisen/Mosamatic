#!/bin/bash

export VERSION=$(cat VERSION)

PWD=$(pwd)

cd mosamatic
rm -rf ./build ./dist
briefcase create
briefcase build

cd ${PWD}