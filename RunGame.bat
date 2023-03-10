ECHO ON
pushd %~dp0

Set "VIRTUAL_ENV=pyenv"

IF NOT EXIST "%VIRTUAL_ENV%\Scripts\activate.bat" (
	pip.exe install virtualenv
    	python -m venv %VIRTUAL_ENV%
)

CALL %VIRTUAL_ENV%\Scripts\activate.bat
CALL python -m pip install --upgrade pip
CALL pip install pygame
CALL python basegame.py
