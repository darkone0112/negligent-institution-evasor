@echo off
echo Installing required packages...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install cx_Freeze wheel

echo Building executable...
python setup.py build_exe

echo Done! The executable will be in the "build/exe.win-amd64-3.13" directory.
pause
