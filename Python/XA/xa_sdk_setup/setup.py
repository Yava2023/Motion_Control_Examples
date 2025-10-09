from setuptools import setup, find_packages
import pathlib
import sys
import version as ver

# setting path
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name="xa_sdk",
    version=ver.version_number,
    author="Thorlabs LTD",
    author_email="techsupport@thorlabs.com",
    description="Python wrapper of the Thorlabs XA SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="BSD",
    packages=["xa_sdk", "xa_sdk.native_sdks", "xa_sdk.products", "xa_sdk.shared"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: BSD",
        "Operating System :: Windows"
    ],
    python_requires='>=3.10, <4',
    install_requires=[]
)
