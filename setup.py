from setuptools import setup

setup(
    name="gicom",
    version="0.1.0",
    py_modules=["main", "config"],
    install_requires=[
        "openai==1.58.1",
        "typer==0.12.5",
        "click==8.1.7",
        "rich==13.9.4",
        "python-dotenv==1.0.1",
        "pyperclip",
        "pwinput",
    ],
    entry_points={
        "console_scripts": [
            "gicom = main:app",
        ],
    },
)
