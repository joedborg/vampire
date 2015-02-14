import sys
from distutils.core import setup

if sys.version_info[0] < 3:
    raise AssertionError('You must use Python 3 with Vampire.')


setup(
    name='vampire',
    version='0.1.4',
    packages=['vampire'],
    scripts=['vmp'],
    url='https://josephb.org/projects/vampire/',
    license='GPLv2',
    author='Joseph Borg',
    author_email='joe@josephb.org',
    description='Deploy Python'
)
