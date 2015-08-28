from setuptools import setup, find_packages

import os
import imp

version_file = os.path.abspath("pather/version.py")
version_mod = imp.load_source("version", version_file)
version = version_mod.version

setup(
    name="pather",
    version=version,
    description="Manage file system structure using patterns",
    author="Roy Nieterau",
    author_email="roy_nieterau@hotmail.com",
    url="https://github.com/bigroy/pather",
    license="LGPL",
    packages=find_packages(),
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ],
)
