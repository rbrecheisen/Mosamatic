#!/bin/bash

cp VERSION mosamatic/src/mosamatic/resources

export VERSION=$(cat VERSION)

echo "Packaging Mosmatic version ${VERSION}"
read -n 1 -s -r -p "Press any key to continue..."

python scripts/python/updatetomlversion.py ${VERSION}

cd mosamatic

rm -rf build/ dist/

briefcase create
briefcase build

echo "Removing TensorFlow includes, db.sqlite3 and migrations..."
rm -rf build/mosamatic/windows/app/src/app_packages/tensorflow/include
rm -f build/mosamatic/windows/app/src/app/mosamatic/backend/db.sqlite3
rm -f build/mosamatic/windows/app/src/app/mosamatic/backend/app/migrations/*.py

briefcase package --adhoc-sign