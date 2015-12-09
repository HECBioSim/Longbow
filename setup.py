#!/usr/bin/env python

# Longbow is Copyright (C) of James T Gebbie-Rayet and Gareth B Shannon 2015.
#
# This file is part of the Longbow software which was developed as part of
# the HECBioSim project (http://www.hecbiosim.ac.uk/).
#
# HECBioSim facilitates and supports high-end computing within the
# UK biomolecular simulation community on resources such as ARCHER.
#
# Longbow is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# Longbow is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Longbow.  If not, see <http://www.gnu.org/licenses/>.

""" Setup script. Used by easy_install and pip. """

import os

from distutils.core import setup
import sys
import subprocess

# check python version
print "Checking python version!"

if not (sys.version_info[0] >= 2 and sys.version_info[1] >= 7):
    print ("The Python version on your system has been detected to be prior "
           "to version 2.7. Whilst Longbow should work for version 2.6, "
           "it is recommended you upgrade to at least version 2.7.")

# download hosts.conf
print "Downloading hosts.conf"

if not os.path.isdir(os.path.expanduser("~/.Longbow")):
    try:
        subprocess.check_output(["wget",
            "http://www.hecbiosim.ac.uk/longbow/send/5-longbow/5-longbow-hosts",
            "-O", os.path.expanduser("~/LongbowHosts.zip")])
    except subprocess.CalledProcessError:
        subprocess.call(["curl", "-L",
            "http://www.hecbiosim.ac.uk/longbow/send/5-longbow/5-longbow-hosts",
            "-o", os.path.join(os.path.expanduser("~"), "LongbowHosts.zip")])

    subprocess.call(["unzip", "-d", os.path.expanduser("~"),
                     os.path.expanduser("~/LongbowHosts.zip")])

# setup args
setup_args = {
    'name': "Longbow",
    'version': "1.01.004",
    'description': "Biomolecular simulation remote job submission "
                   "utility.",
    'long_description': "Longbow sends jobs submitted to your desktop to a "
                        "high-end resource. The results are automatically"
                        " brought back bringing the power of an HPC to "
                        "your desktop",
    'author': "James T Gebbie-Rayet, Gareth B Shannon",
    'author_email': "james.gebbie@stfc.ac.uk, "
                    "gareth.shannon@nottingham.ac.uk",
    'url': "www.hecbiosim.ac.uk",
    'license': "GNU General Public License.",
    'classifiers': [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: Unix'
    ],
    'packages': ["Longbow", "Longbow.plugins",
                 "Longbow.plugins.schedulers", "Longbow.plugins.apps",
                 "Longbow.corelibs"],
    'scripts': ['Longbow/longbow'],

}

setup(**setup_args)
