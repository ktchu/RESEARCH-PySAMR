"""
SAMR: a light-weight library for Structure Adaptive Mesh Refinement

TODO.

------------------------------------------------------------------------------
COPYRIGHT/LICENSE.  This file is part of the XYZ package.  It is subject
to the license terms in the LICENSE file found in the top-level directory of
this distribution.  No part of the XYZ package, including this file, may be
copied, modified, propagated, or distributed except according to the terms
contained in the LICENSE file.
------------------------------------------------------------------------------
"""
# --- Imports

# Standard library
import os.path
from pkg_resources import get_distribution, DistributionNotFound


# --- Package API

# Sub-packages
from . import mesh
from . import geometry


# --- Package information

_PKG_INFO = {
    'version': '',
    'author': '',
    'author_email': '',
    'license': 'Apache Software License',
    'copyright': 'Copyright (c) 2018 Kevin T. Chu',
}


# --- Helper functions

def _update_pkg_info(pkg_info):
    """
    Update package information attributes from distribution or package files.

    Parameters
    ----------
    pkg_info : dict
        original package info values

    Return values
    ----------
    pkg_info : dict
        updated package info values
    """
    # --- Preparations

    pkg_root_dir = os.path.dirname(os.path.normcase(__file__))
    pkg_parent_dir = os.path.dirname(pkg_root_dir)

    # Attempt to get package information from distribution
    try:
        dist = get_distribution(__name__)
    except DistributionNotFound:
        dist = None

    # Check that this __init__.py file is part of installed distribution
    # identified by get_distribution().
    if dist:
        # normalize case for Windows
        dist_loc = os.path.normcase(dist.location)

        if not pkg_root_dir.startswith(os.path.join(dist_loc, __name__)):
            dist = None

    # Update package information
    if dist:
        # Get package information from distribution
        metadata = {}
        for line in dist.get_metadata_lines(dist.PKG_INFO):
            try:
                split_line = line.split(':')
            except UnicodeDecodeError:
                # Ignore lines that cannot be decoded using ASCII encoding
                pass

            if len(split_line) > 1:
                key = split_line[0].strip()
                value = ':'.join(split_line[1:])
                metadata[key] = value.strip()

        pkg_info['version'] = dist.version
        pkg_info['author'] = metadata.get('Author', pkg_info['author'])
        pkg_info['author_email'] = metadata.get('Author-email',
                                                pkg_info['author_email'])
        pkg_info['license'] = metadata.get('License', pkg_info['license'])

    else:
        # --- distribution unavailable, so attempt to get package information
        #     from package files

        # Get version from VERSION file
        try:
            with open(os.path.join(pkg_parent_dir, 'VERSION')) as file_:
                pkg_info['version'] = file_.read().strip()
        except IOError:
            # Ignore errors opening VERSION file.
            pass

        # Get authors and author_email from AUTHORS file
        try:
            with open(os.path.join(pkg_parent_dir, 'AUTHORS')) as file_:
                lines = file_.readlines()
                pkg_info['author'] = \
                    ', '.join([line.split('<')[0].strip() for line in lines])

                first_author_split = lines[0].split('<')
                if len(first_author_split) > 1:
                    pkg_info['author_email'] = \
                        first_author_split[1].split('>')[0].strip()

        except IOError:
            # Ignore errors opening AUTHORS file.
            pass

    return pkg_info


# --- Standard package information attributes

# Update package info from distribution or files
_PKG_INFO = _update_pkg_info(_PKG_INFO)

# Set standard package info attributes
__version__ = _PKG_INFO['version']
__author__ = _PKG_INFO['author']
__author_email__ = _PKG_INFO['author_email']
__license__ = _PKG_INFO['license']
__copyright__ = _PKG_INFO['copyright']


# --- Cleanup

del _PKG_INFO
