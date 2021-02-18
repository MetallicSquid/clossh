#!/usr/bin/env/python

import setuptools

setuptools.setup(
      name="clossh-MetallicSquid",
      version="0.1.0",
      description="A simple and lightweight clustering library based on the ssh protocol.",
      author="Guillaume Macneil",
      url="https://github.com/MetallicSquid/clossh",
      packages=setuptools.find_packages(),
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
            "Operating System :: Unix",
      ],
)
