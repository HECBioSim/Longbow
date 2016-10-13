#!/usr/bin/env python

# Longbow is Copyright (C) of James T Gebbie-Rayet and Gareth B Shannon 2015.
#
# This file is part of the Longbow software which was developed as part of the
# HECBioSim project (http://www.hecbiosim.ac.uk/).
#
# HECBioSim facilitates and supports high-end computing within the UK
# biomolecular simulation community on resources such as ARCHER.
#
# Longbow is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 2 of the License, or (at your option) any later
# version.
#
# Longbow is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Longbow.  If not, see <http://www.gnu.org/licenses/>.

"""Setup script. Used by easy_install and pip."""

from distutils.core import setup
import os
import sys

# Check for unsupported Python versions.
MAJOR = sys.version_info[0]
MINOR = sys.version_info[1]

if not (MAJOR >= 2 and MINOR >= 6):

    print('The Python version installed is "{0}.{1}", Longbow does not support'
          ' this version. We recommend that you install at least version 2.7'
          .format(MAJOR, MINOR))

else:

    print('The Python version installed "{0}.{1}" is supported by Longbow.'
          .format(MAJOR, MINOR))

# Setup
setup(name='Longbow',
      version='1.3.2',
      description='Biomolecular simulation remote job submission tool.',
      long_description=open('README.rst').read(),
      author='James T Gebbie-Rayet, Gareth B Shannon',
      author_email=('james.gebbie@stfc.ac.uk, '
                    'gareth.shannon@nottingham.ac.uk'),
      url='http://www.hecbiosim.ac.uk',
      license='OSI Approved :: GNU General Public License v2 (GPLv2)',
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Environment :: Console',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Topic :: Scientific/Engineering',
                   'Topic :: Utilities',
                   'Operating System :: MacOS :: MacOS X',
                   'Operating System :: POSIX',
                   'Operating System :: Unix'
                   ],
      packages=['Longbow', 'Longbow.plugins', 'Longbow.plugins.schedulers',
                  'Longbow.plugins.apps', 'Longbow.corelibs'],
      scripts=['Longbow/longbow'],
      )

# Try and create the .Longbow directory and a basic hosts.conf
try:

    print('Checking if Longbow needs to create the ~/.Longbow directory...')

    # Setting up the .Longbow directory.
    if not os.path.isdir(os.path.expanduser('~/.Longbow')):

        print('Longbow will create a hidden directory in your $HOME directory '
              'in which it will create the hosts configuration file. You will '
              'need to edit this file with your account information on the '
              'HPC machines you wish to use. See documentation for more '
              'information - www.hecbiosim.ac.uk/longbow-docs')

        os.mkdir(os.path.expanduser('~/.Longbow'))

        HOSTFILE = open(os.path.expanduser('~/.Longbow/hosts.conf'), 'w+')

        HOSTFILE.write('[QuickStart]\n')
        HOSTFILE.write('host = login.hpc.ac.uk\n')
        HOSTFILE.write('user = myusername\n')
        HOSTFILE.write('corespernode = 24\n')
        HOSTFILE.write('cores = 24\n')
        HOSTFILE.write('remoteworkdir = /work/myusername/\n')
        HOSTFILE.write('account = myaccount\n')
        HOSTFILE.write('modules = mymodules\n')

        HOSTFILE.close()

    else:

        print('Directory already exists - skipping.')


except IOError:

    print('Longbow failed to create the host configuration file in '
          '"~/.Longbow/hosts.conf", you will have to do this manually. The '
          'user documentation details the information that should be in this '
          'file.')
