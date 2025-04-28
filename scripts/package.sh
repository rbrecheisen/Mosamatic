#!/bin/bash

cp VERSION mosamatic/src/mosamatic/resources

export VERSION=$(cat VERSION)

python scripts/python/updatetomlversion.py ${VERSION}

cd mosamatic

rm -rf build/ dist/

briefcase create
briefcase build

rm -rf build/mosamatic/windows/app/src/app_packages/tensorflow/include
rm -f build/mosamatic/windows/app/src/app/mosamatic/backend/db.sqlite3
rm -f build/mosamatic/windows/app/src/app/mosamatic/backend/app/migrations/*.py

briefcase package --adhoc-sign