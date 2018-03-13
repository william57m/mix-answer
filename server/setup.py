import os

from setuptools import find_packages
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

requires = None

with open(os.path.join(here, 'requirements.txt')) as f:
    ignore_prefix = 'git+https'
    reqs = f.read().split('\n')
    requires = [r for r in reqs if not r.startswith(ignore_prefix)]

setup(
    name='mix-answer-server',
    version='0.0.0',
    description='Mix Answer Server',
    author='William Mura',
    author_email='william57m@gmail.com',
    url='https://github.com/william57m/mix-answer',
    packages=find_packages(exclude=('tests', 'tests.*'))
)
