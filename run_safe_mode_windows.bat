@echo off
rem Safe mode: fixed-function renderer + short view distance. Use if anything looks wrong or runs slowly.
cd /d "%~dp0"
python main.py --safe
pause
