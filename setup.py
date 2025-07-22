from setuptools import setup, find_packages

setup(
    name="glpi_async",
    version="0.2.1",
    author='Cooper',
    packages=find_packages(),
    install_requires=[
        "httpx>=0.27.0",
        "python-dotenv"
    ],
    python_requires=">=3.7",
)
