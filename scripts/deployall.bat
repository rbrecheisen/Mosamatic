@echo off

setlocal

echo "Building MSI installer and deploying Mosamatic (%VERSION%) to DockerHub."
echo "Is this version correct?"
pause

call scripts\package.bat
call scripts\deploy2dockerhub.bat

echo ""
echo "Don't forget to update GitHub Releases!!!"

endlocal