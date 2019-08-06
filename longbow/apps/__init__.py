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

"""This module contains the import logic for the application plugins.

All code for a new plugin should be placed inside the plugin module itself
and not here, follow the template for constructing new app plugins.
"""

import os
import pkgutil
import sys

PATH = os.path.dirname(__file__)
MODULES = pkgutil.iter_modules(path=[PATH])

EXECLIST = []
PLUGINEXECS = {}
MODNAMEOVERRIDES = {}

# Loop through all the modules in the plugin.
for loader, modulename, ispkg in MODULES:

    # Check for double loading in the namespace.
    if modulename not in sys.modules:

        mod = __import__("longbow.apps." + modulename, fromlist=[""])

        for executable, _ in getattr(mod, "EXECDATA").items():

            # Compile a list of executables across all plugins.
            EXECLIST.append(executable)

            # Compile a dictionary associating executable with plugins.
            PLUGINEXECS[executable] = modulename

        # Is the module named differently on HPC than the software is called.
        try:

            MODNAMEOVERRIDES[modulename] = getattr(mod, "MODULENAME").items()

        except AttributeError:

            pass
