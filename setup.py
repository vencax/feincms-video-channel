#!/usr/bin/env python
import os
import subprocess
from setuptools import setup, find_packages
from setuptools.command.install import install

README_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                           'README')

description = '''
Presents video files stored in mediafilesin youtube like channel.
'''


class MyInstall(install):
    def run(self):
        projpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                'videochannel')
        print 'Generating MO files in %s' % projpath
        subprocess.call(['django-admin.py', 'compilemessages'],
                        cwd=projpath)
        install.run(self)

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
    cmdclass={'install': MyInstall}
)
