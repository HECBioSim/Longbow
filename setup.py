#!/usr/bin/env python

# BSD 3-Clause License
#
# Copyright (c) 2017, Science and Technology Facilities Council and
# The University of Nottingham
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""Setup script. Used by easy_install and pip."""

from distutils.core import setup
import os
import sys

# Check for unsupported Python versions.
VERSIONS = ['2.7', '3.5', '3.6', '3.7']
VERSION = str(sys.version_info[0]) + '.' + str(sys.version_info[1])

# Do we want config directory with host.conf and bash completion.
HOMECFG = True

if '--no-home-cfg' in sys.argv:

    HOMECFG = False
    sys.argv.pop(sys.argv.index('--no-home-cfg'))

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
      version='1.5.3-dev',
      description='Biomolecular simulation remote job submission tool.',
      long_description=open('README.rst').read(),
      author='James T Gebbie-Rayet, Gareth B Shannon',
      author_email=('james.gebbie@stfc.ac.uk, '
                    'gareth.b.shannon@nasa.gov'),
      url='http://www.hecbiosim.ac.uk',
      license='OSI Approved :: BSD License',
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Environment :: Console',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
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
      packages=['longbow', 'longbow.schedulers', 'longbow.apps'],
      scripts=['longbow/longbow'],
      )

if HOMECFG is True:

    # Try and create the .Longbow directory and a basic hosts.conf
    try:

        # Setting up the .Longbow directory.
        if not os.path.isdir(os.path.expanduser('~/.longbow')):

            print('Longbow will create a hidden directory in your $HOME '
                  'directory in which it will create the hosts configuration '
                  'file. You will need to edit this file with your account '
                  'information on the HPC machines you wish to use. See '
                  'documentation for more information - '
                  'www.hecbiosim.ac.uk/longbow-docs')

            os.mkdir(os.path.expanduser('~/.longbow'))

            HOSTFILE = open(os.path.expanduser('~/.longbow/hosts.conf'), 'w+')

            HOSTFILE.write(
                '[QuickStart]\n'
                'host = login.hpc.ac.uk\n'
                'user = myusername\n'
                'corespernode = 24\n'
                'cores = 24\n'
                'remoteworkdir = /work/myusername/\n'
                'account = myaccount\n'
                'modules = mymodules\n')

            HOSTFILE.close()

        else:

            print('Directory already exists at "~/.longbow" - Longbow is '
                  'skipping creating a new one.')

    except IOError:

        print('Longbow failed to create the host configuration file in '
              '"~/.longbow/hosts.conf", you will have to do this manually.\n'
              'The user documentation details the information that should be '
              'in this file here \n https://longbow.readthedocs.io/en/latest/'
              'usr-getting-started.html#adding-a-hpc-machine-to-longbow')

    # Try to create the bash autocomplete file.
    try:

        print('Longbow will try to setup bash autocomplete on this machine, '
              'this will enable the user to use the tab key as part of the '
              'longbow command-line to reveal/complete command-line args.\n'
              'This currently only works on some operating systems.')

        BASHFILE = open(os.path.expanduser('~/.longbow/bash_completion'), 'w+')

        BASHFILE.write(
            '_longbow()\n'
            '{\n'
            '    local cur prev opts\n'
            '    COMPREPLY=()\n'
            '    cur="${COMP_WORDS[COMP_CWORD]}"\n'
            '    prev="${COMP_WORDS[COMP_CWORD-1]}"\n'
            '    opts="--about --debug --disconnect --examples '
            '--help --hosts --job --jobname --log -- maxtime '
            '--nochecks --recover --resource --replicates '
            '--verbose --version"\n\n'
            '    if [[ ${cur} == -* ]]; then\n'
            '        COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )\n'
            '        return 0\n'
            '    elif [[ ${prev} == --hosts ]] || '
            '[[ ${prev} == --job ]] || [[ ${prev} == --recover ]]; then\n'
            '        _filedir\n'
            '    fi\n'
            '}\n'
            'complete -F _longbow longbow\n')

        BASHFILE.close()

        # Now add a source entry to the user .bashrc
        if os.path.isfile(os.path.expanduser('~/.bashrc')):

            BASHFILE = open(os.path.expanduser('~/.bashrc'), 'a+')

            if not any('source ~/.longbow/bash_completion'
                       in bashline for bashline in BASHFILE.readlines()):

                BASHFILE.write('source ~/.longbow/bash_completion\n')

    except IOError:

        print('Longbow failed to create the bash autocomplete file on this '
              'machine. Longbow will still continue to function normally, '
              'however the bash autocomplete will not be available for '
              'longbow command-line parameters.')
