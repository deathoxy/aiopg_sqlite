#!/usr/bin/env python

import sys
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.version_info < (3, 6):
    raise NotImplementedError("Python 3.6 required")


install_requires = [
    'sqlalchemy',
    'pytest',
    'pytest-cov',
    'pytest-aiohttp'
]

setup(name='aiopg_sqlite',
      version='0.0.1a',
      description='Drop-in replacement for aiopg for various '
                  '(mostly test) purposes',
      author='Ilya Samartsev',
      author_email='deathoxy@gmail.com',
      url='https://github.com/deathoxy/aiopg_sqlite',
      py_modules=['aiopg_sqlite'],
      scripts=['aiopg_sqlite.py'],
      license='MIT',
      platforms='any',
      install_requires=install_requires,
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Topic :: Database :: Database Engines/Servers',
                   'Programming Language :: Python :: 3.6',
                   'Topic :: System :: Networking',
                   'Topic :: Software Development',
                   'Topic :: Software Development :: Libraries',
                   ],
      )
