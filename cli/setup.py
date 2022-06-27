#!/usr/bin/env python

from setuptools import find_packages
from setuptools import setup

PROJECT = 'tre'
VERSION = '0.1'

try:
    long_description = open('README.md', 'rt').read()  # TODO: add long description
except IOError:
    long_description = ''

setup(
    name=PROJECT,
    version=VERSION,

    description='Demo TRE CLI for AzureTRE',
    long_description=long_description,

    author='Stuart Leeks',
    author_email='stuartle@microsoft.com',

    # url='',
    # download_url='',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Intended Audience :: Developers',
        'Environment :: Console',
    ],

    platforms=['Any'],

    scripts=[],

    provides=[],
    install_requires=['click'],

    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'tre = tre.main:cli'
        ],
    },

    zip_safe=False,
)
