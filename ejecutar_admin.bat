@echo off
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process python -ArgumentList 'main.py' -Verb RunAs"
