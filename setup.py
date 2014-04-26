# -*- coding: utf-8 -*-
import sys
from os import path
from distutils.core import setup

if sys.version_info < (2, 7):
    sys.exit('monad requires Python 2.7 or higher')

ROOT_DIR = path.abspath(path.dirname(__file__))
sys.path.insert(0, ROOT_DIR)

from monad import VERSION
from monad import __doc__ as DESCRIPTION
LONG_DESCRIPTION = open(path.join(ROOT_DIR, 'README.rst')).read()

setup(
    name='monad',
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    author='Philip Xu',
    author_email='pyx@xrefactor.com',
    url='https://bitbucket.org/pyx/monad/',
    download_url=(
        'https://bitbucket.org/pyx/monad/get/%s.tar.bz2' % VERSION),
    packages=['monad', 'monad.types'],
    license='BSD-New',
)
