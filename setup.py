from setuptools import setup, find_packages

setup(
    name="httpquest",
    version="0.1",
    packages=find_packages(),  # auto-detects all packages like `app/`
    install_requires=[],  # you can list Flask, SQLAlchemy etc. here
)
