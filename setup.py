#!/usr/bin/env python3

import os
from setuptools import setup, find_packages

def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

setup(name='epy',
      version=read('epy/VERSION').splitlines()[0],
      description='Python package for epy auto instantiation',
      long_description=read('README.md'),
      long_description_content_type='text/markdown',
      keywords='Embedded, Python, epy',
      author='Yuliang Tao',
      author_email='nerotao@foxmail.com',
      license='MIT',
      url='https://github.com/taoyl/epy',
      packages=find_packages(),
      package_data={'epy': ['VERSION'],},
      install_requires=[]
     )