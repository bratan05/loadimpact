import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(name='logic',
      version='0.2',
      packages=find_packages(),
      include_package_data=True,
      description="Logic to compute distribution of DM and DE's over data centers",
      long_description=README,
      url='',
      author="Andrei Zimin",
      author_email="reyenka@gmail.com",
      py_modules=[
          "tests",
          "views",
          "urls",
          "__init__"
      ],
      classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Environment :: Web Environment",
            "Framework :: Django",
            "Intended Audience :: Developers"
      ])

