#!/usr/bin/env python
from setuptools import setup, find_packages
import os

README_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README')

description = '''Presents video files stored in mediafiles in youtube like channel.'''

if os.path.exists(README_PATH):
    long_description = open(README_PATH).read()
else:
    long_description = description

setup(name='feincms-video-channel',
    version='0.1',
    description=description,
    license='BSD',
    url='www.vxk.cz',
    author='vencax',
    author_email='vencax@centrum.cz',
    packages=find_packages(),
    install_requires=[
        'django>=1.3',
        'south',
        'setuptools',
    ],
    keywords="feincms video channel",
    include_package_data=True,
)
