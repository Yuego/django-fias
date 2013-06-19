#!/usr/bin/env python
from setuptools import setup, find_packages
import sys
sys.path.insert(0, '..')

setup(
    name='fias',
    version='0.1',
    author= 'Artem Vlasov',
    author_email='root@proscript.ru',
    url='',
    download_url='',

    description='FIAS',
    long_description=open('README.rst').read(),

    license='MIT license',
    requires=[
        'Django>=1.4',
        'django_select2',
        'pysimplesoap',
        'rarfile',
        'six',
    ],
    packages=find_packages(),
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Russian',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
