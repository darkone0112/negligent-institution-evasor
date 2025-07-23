from setuptools import setup
from cx_Freeze import setup, Executable
import sys

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": [
        "selenium",
        "undetected_chromedriver",
        "requests",
        "datetime",
        "random",
        "time",
        "websockets",
        "asyncio",
        "concurrent",
        "queue",
        "http",
        "html",
        "xml",
        "urllib3",
        "certifi",
        "idna",
        "charset_normalizer"
    ],
    "excludes": [],
    "include_files": [],
    "includes": [
        "selenium.webdriver",
        "selenium.webdriver.common.by",
        "selenium.webdriver.common.keys",
        "selenium.webdriver.support.ui",
        "selenium.webdriver.support.expected_conditions",
        "selenium.webdriver.common.action_chains"
    ],
    "zip_include_packages": ["*"],
    "zip_exclude_packages": []
}

base = "Console" if sys.platform == "win32" else None

setup(
    name="AppointmentChecker",
    version="1.0",
    description="Appointment Checking Automation Tool",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            script="main.py",
            base=base,
            target_name="AppointmentChecker.exe"
        )
    ]
)
