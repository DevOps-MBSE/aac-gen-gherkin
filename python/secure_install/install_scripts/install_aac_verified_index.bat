REM This script will install AaC Gen-Gherkin and its dependencies via PyPI.

@echo off

cd /D "%~dp0"

python -m pip "install" "--require-hashes" "--no-deps" "-r" "requirements.txt"
