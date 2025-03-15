@echo off

setlocal

copy /Y VERSION mosamatic\src\mosamatic\resources

cd mosamatic

briefcase update
briefcase build --update-requirements
briefcase package --adhoc-sign

endlocal