# --- Imports

import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


# --- Package requirements

INSTALL_REQUIREMENTS = [
    'click',
    'numpy',
    ]

TESTING_REQUIREMENTS = [
    'coverage',
    'pycodestyle',
    'pylint',
    'psutil',
    'pytest',
    'pytest-cov',
    'pytest-pycodestyle',
    'pytest-pylint',
    'pytest-xdist',
    ]
DEV_REQUIREMENTS = TESTING_REQUIREMENTS + [
    'ipython',
    'radon',
    'sphinx',
    # TODO: review following packages
    # 'numba',
    ]


# --- pytest class

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


# --- Package information

# Package root directory
pkg_root_dir = os.path.dirname(os.path.normcase(__file__))

# Version
version_file = open(os.path.join(pkg_root_dir, 'VERSION'))
version = version_file.read().strip()

# Authors and author email
authors_file = open(os.path.join(pkg_root_dir, 'AUTHORS'))
author_lines = authors_file.readlines()
authors = ', '.join([line.split('<')[0].strip() for line in author_lines])
first_author_split = author_lines[0].split('<')
if len(first_author_split) > 1:
    author_email = first_author_split[1].split('>')[0].strip()
else:
    author_email = ''


# --- setup()

setup(
    # Package information
    name='PySAMR',
    version=version,
    license='Apache Software License',
    author=authors,
    author_email=author_email,
    description='TODO',
    long_description=open('README.markdown').read(),
    keywords='TODO',
    url='TODO',

    # Package construction
    packages=find_packages(),
    scripts=[],

    # Package requirements
    install_requires=INSTALL_REQUIREMENTS,
    tests_require=TESTING_REQUIREMENTS,
    extras_require={
        'dev': DEV_REQUIREMENTS,
        'testing': TESTING_REQUIREMENTS,
    }
)
