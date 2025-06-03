@echo off

setlocal

copy /Y VERSION mosamatic\src\mosamatic\resources

set /p VERSION=<VERSION

python scripts\python\updatetomlversion.py %VERSION%

cd mosamatic

rmdir /s /q "build"

briefcase create
briefcase build

rmdir /s /q "build\mosamatic\windows\app\src\app_packages\tensorflow\include"
del /q "build\mosamatic\windows\app\src\app\mosamatic\backend\db.sqlite3"
del /q "build\mosamatic\windows\app\src\app\mosamatic\backend\app\migrations\*.py"

briefcase package --adhoc-sign

endlocal