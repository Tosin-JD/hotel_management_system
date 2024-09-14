# Open Hotel Management System.

## How to install on windows
1. Download the installer package.
2. Double click on it to install.

## How to Run the Code
1. Clone the repository with the code:
2. Create a python environment with `python -m venv env` for Windows
`python3 -m venv env`
3. Activate the environment with the code
   `env\Scripts\activate` for windows
   `env/bin/activate` for Linux
4. Install pyinstaller `pip pyinstaller`
5. Install the requirements `pip install -r requirements.txt`
6. cd hotel_management_system
7. run this code `python src/main.py`

## How to compile from source code.
1. Clone the repository with the code:
2. Create a python environment
3. Install pyinstaller `pip pyinstaller`
4. Install the requirements `pip install -r requirements.txt`
5. cd hotel_management_system 
6. Make sure that you are in the root directory of the project.
7. Run this code on the cmd or power shell 
`pyinstaller --onefile --noconsole --hidden-import babel.numbers --icon=src/resources/icons/logo.ico src/main.py`
8. Open the folder dist
9. You will find an application name main.exe Clikc on it to run.

If you want to convert it into an executable file that can be installed on your computer, use Inno Setup tools.

Shared with love.

