#*******************************************************************************
# Filename: setup.py
# Language: Python
# Author: nathantoner
# Created: 2022-03-08
#
# Description:
# Script for installing enigma as a package.
#
#*******************************************************************************


from setuptools import setup
from distutils.util import convert_path
from os import path


here = path.abspath(path.dirname(__file__))
version_dict = {}
version_path = convert_path('enigma/_version.py')

# Get the version number from the version path.
with open(version_path, 'r') as ver_file:
    exec(ver_file.read(), version_dict)

# Get the long description from the README file.
with open(path.join(here, 'README.md')) as a_file:
    long_description = a_file.read()

# TODO: update classifiers
CLASSIFIERS = ['Development Status :: 4 - Beta',
               'Environment :: Console',
               'Intended Audience :: Education',
               'License :: OSI Approved :: MIT License',
               'Natural Language :: English',
               'Operating System :: OS Independent',
               'Programming Language :: Python',
               'Programming Language :: Python :: 3',
               'Topic :: Education',
               'Topic :: Scientific/Engineering',
               'Topic :: Security :: Cryptography']
PROJECT_URLS = {'Documentation': 'https://github.com/Engineero/enigma',
                'Source': 'https://github.com/Engineero/enigma',
                'Tracker': 'https://github.com/Engineero/enigma/issues'}

setup(name='enigma',
      packages=['enigma'],
      version=version_dict['__version__'],
      description='An implementation of a WWII Enigma Machine.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Engineero',
      author_email='engineerolabs@gmail.com',
      url='https://github.com/Engineero/enigma',
      project_urls=PROJECT_URLS,
      classifiers=CLASSIFIERS)



#*******************************************************************************
#                                END OF FILE
#*******************************************************************************
