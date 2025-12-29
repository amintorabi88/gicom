from setuptools import setup, find_packages

setup(
    name="gicom",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "openai==1.58.1",
        "typer==0.12.5",
        "click==8.1.7",
        "rich==13.9.4",
        "python-dotenv==1.0.1",
        "pyperclip",
        # pwinput removed
    ],
    entry_points={
        "console_scripts": [
            "gicom = gicom.main:app",
        ],
    },
)