# Open Hotel Management System.

## How to install on windows
1. Download the installer package.
2. Double click on it to install.

## How to compile from source code.
1. Clone the repository with the code: 
2. cd hotel_management_system 
3. Make sure that you are in the root directory of the project.
4. Run this code on the cmd or power shell 
pyinstaller --onefile --noconsole --hidden-import babel.numbers --icon=src/resources/icons/logo.ico src/main.py
5. Open the folder dist
6. You will find an application name main.exe Clikc on it to run.

If you want to convert it into an executable file that can be installed on your computer, use inno setup tools.

Shared with love.

