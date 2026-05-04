from setuptools import setup, find_packages

setup(
    name="ddos_trastfactor",
    version="2.0.0",
    packages=find_packages(),
    install_requires=["aiohttp>=3.8.0"],
    python_requires=">=3.7",
)
