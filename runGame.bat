@echo off
echo Installing requirements...
pip install -r requirements.txt
echo Done.

echo starting the script

python menu.py
pause