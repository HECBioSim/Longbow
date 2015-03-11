#!/usr/bin/env python

""" Setup script. Used by easy_install and pip. """

import os

from distutils.core import setup
import sys
import subprocess

# check python version
print "Checking python version!"
if not (sys.version_info[0] >= 2 and sys.version_info[1] >= 7):
    exit_with_error("You should install Python 2.7 or greater to install "
                    "Longbow")
print "Python version checked."

# download examples
subprocess.call(["wget", "-P", os.path.expanduser("~"), 
                 "http://www.hecbiosim.ac.uk/longbow-extras.zip"])
subprocess.call(["unzip", "-d", os.path.expanduser("~"), 
                 os.path.expanduser("~/longbow-extras.zip")])

# setup args
setup_args = {
    'name'             : "Longbow",
    'version'          : "0.9.9",
    'description'      : "Biomolecular simulation remote job submission "
                            "utility.",
    'long_description' : "Longbow sends jobs submitted to your desktop to a "
                            "high-end resource. The results are automatically"
                            " brought back bringing the power of an HPC to "
                            "your desktop",
    'author'           : "James T Gebbie-Rayet and Gareth B Shannon",
    'license'          : "GNU General Public License.",
    'classifiers'      : [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Beta-testers',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: Unix'
    ],

    'packages'    : ["Longbow", "Longbow.plugins", 
                     "Longbow.plugins.schedulers", "Longbow.corelibs"],
    'scripts' : ['Longbow/longbow'],

}

setup(**setup_args)