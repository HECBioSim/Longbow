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
VERSIONS = ['2.6', '2.7', '3.2', '3.3', '3.4', '3.5', '3.6']
VERSION = str(sys.version_info[0]) + '.' + str(sys.version_info[1])

if VERSION not in VERSIONS:

    sys.exit('The Python version installed is "{0}.{1}", Longbow does not '
             'support this version. We recommend that you install at least '
             'version 2.7 or a recent 3.x series'.format(sys.version_info[0],
                                                         sys.version_info[1]))

else:

    print('The Python version installed "{0}.{1}" is supported by Longbow.'
          .format(sys.version_info[0], sys.version_info[1]))

# Setup
setup(name='Longbow',
      version='1.5.0',
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
                   'Programming Language :: Python :: 3.2',
                   'Programming Language :: Python :: 3.3',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6',
                   'Topic :: Scientific/Engineering',
                   'Topic :: Scientific/Engineering :: Bio-Informatics',
                   'Topic :: Scientific/Engineering :: Chemistry',
                   'Topic :: System :: Distributed Computing',
                   'Topic :: Utilities',
                   'Topic :: Software Development :: Libraries',
                   'Operating System :: MacOS :: MacOS X',
                   'Operating System :: POSIX :: Linux',
                   'Operating System :: Unix'
                   ],
      keywords=('hpc hec supercomputer grid cloud batch jobs remote submission'
                ' submitter lsf pbs torque sge soge slurm automated staging '
                'longbow hecbiosim ccpbiosim'),
      packages=['longbow', 'longbow.schedulers', 'longbow.apps',
                'longbow.corelibs'],
      scripts=['longbow/longbow'],
      )

# Try and create the .Longbow directory and a basic hosts.conf
try:

    # Test for the old directory presence (IE updating).
    if os.path.isdir(os.path.expanduser('~/.Longbow')):

        print("Since version 1.5.0 '~/.Longbow' directory has been all lower"
              "case, moving '~/.Longbow' to '~/.longbow'.")

        os.rename(os.path.expanduser('~/.Longbow'),
                  os.path.expanduser('~/.longbow'))

    # Setting up the .Longbow directory.
    elif not os.path.isdir(os.path.expanduser('~/.longbow')):

        print('Longbow will create a hidden directory in your $HOME directory '
              'in which it will create the hosts configuration file. You will '
              'need to edit this file with your account information on the '
              'HPC machines you wish to use. See documentation for more '
              'information - www.hecbiosim.ac.uk/longbow-docs')

        os.mkdir(os.path.expanduser('~/.longbow'))

        HOSTFILE = open(os.path.expanduser('~/.longbow/hosts.conf'), 'w+')

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

        print("Directory already exists at '~/.longbow, Longbow is skipping "
              "creating a new one.")

except IOError:

    print('Longbow failed to create the host configuration file in '
          '"~/.longbow/hosts.conf", you will have to do this manually. The '
          'user documentation details the information that should be in this '
          'file.')

# Try to create the bash autocomplete file.
try:

    print('Longbow will try to setup bash autocomplete on this machine, this '
          'will enable the user to use the tab key as part of the longbow '
          'command-line to reveal/complete command-line args. This currently '
          'only works on some operating systems (mainly Linux based).')

    BASHFILE = open(os.path.expanduser('~/.longbow/bash_completion'), 'w+')

    BASHFILE.write('_longbow()\n')
    BASHFILE.write('{\n')
    BASHFILE.write('    local cur prev opts\n')
    BASHFILE.write('    COMPREPLY=()\n')
    BASHFILE.write('    cur="${COMP_WORDS[COMP_CWORD]}"\n')
    BASHFILE.write('    prev="${COMP_WORDS[COMP_CWORD-1]}"\n')
    BASHFILE.write('    opts="--about --debug --disconnect --examples --help '
                   '--hosts --job --jobname --log --recover --resource '
                   '--replicates --verbose --version"\n\n')
    BASHFILE.write('    if [[ ${cur} == -* ]] ; then\n')
    BASHFILE.write('        COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )\n')
    BASHFILE.write('        return 0"\n')
    BASHFILE.write('    fi"\n')
    BASHFILE.write('}"\n')
    BASHFILE.write('complete -F _longbow longbow"\n')

    BASHFILE.close()

    # Now add a source entry to the user .bashrc
    if os.path.isfile(os.path.expanduser('~/.bashrc')):

        BASHFILE = open(os.path.expanduser('~/.bashrc'), 'a+')

        if not any('source ~/.longbow/bash_completion'
                   in bashline for bashline in BASHFILE.readlines()):

            BASHFILE.write('source ~/.longbow/bash_completion')

except IOError:

    print('Longbow failed to create the bash autocomplete file on this '
          'machine. Longbow will still continue to function normally, however '
          'the bash autocomplete will not be available for longbow '
          'command-line parameters.')
