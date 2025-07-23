@echo off
echo Installing required packages...
pip install cx_Freeze

echo Building executable...
python setup.py build

echo Done! The executable will be in the "build" directory.
pause
