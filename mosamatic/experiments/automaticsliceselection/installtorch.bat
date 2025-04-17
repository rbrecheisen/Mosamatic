@echo off

setlocal

call python -m pip uninstall torch torchvision -y
call python -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

endlocal