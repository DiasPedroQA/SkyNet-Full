"""Módulo de configuração do setup para o backend do Skynet Mobile."""

from setuptools import find_packages, setup

setup(
    name="skynet-mobile-backend",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.115.0",
        "uvicorn[standard]>=0.30.0",
        "sqlalchemy>=2.0.0",
        "pydantic>=2.0.0",
        "click>=8.0.0",
        "colorama>=0.4.6",
        "tabulate>=0.9.0",
        "platformdirs>=3.0.0",
    ],
    entry_points={
        "console_scripts": [
            "skynet=app.cli:main",
        ],
    },
    python_requires=">=3.8",
)
