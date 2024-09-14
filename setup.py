from cx_Freeze import setup, Executable
import sys

# Include additional modules or packages that your application uses
include_files = [
    # Include any additional non-Python files your application needs
]

# base="Win32GUI" should be used only for Windows GUI app
base = "Win32GUI" if sys.platform == "win32" else None


# Replace 'main.py' with the actual name of your main script
executables = [Executable("app.py", base=base)]

setup(
    name="GuestHouse",
    version="1.0",
    description=" Guest House Application",
    executables=executables,
    options={
        "build_exe": {
            "packages": [
                "tkcalendar",
                "reportlab",
                "PIL",  # Pillow's import name
            ],
            "include_files": include_files,
            # Additional build options as needed
        }
    }
)
