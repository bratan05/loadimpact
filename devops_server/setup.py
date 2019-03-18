#!/usr/bin/env python
import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

setup(
    name='devops',
    version='0.2',
    include_package_data=True,
    description="Logic to compute distribution of DM and DE's over data centers",
    long_description=README,
    author="Andrei Zimin",
    author_email='reyenka@gmail.com',
    url='',
    packages=find_packages(),
    scripts=['manage.py'],
    install_requires=['django'],
    classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Environment :: Web Environment",
            "Framework :: Django",
            "Intended Audience :: Developers"
      ]
)
