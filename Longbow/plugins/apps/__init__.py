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

"""
This module contains the import logic for the applications plug-in. It makes
available all the methods. All code for a new plug-in should be placed inside
the plug-in module itself and not here, follow the template for constructing
new app plug-ins.
"""

import os
import pkgutil
import sys

PATH = os.path.dirname(__file__)
MODULES = pkgutil.iter_modules(path=[PATH])

# These structures make using the code lighter on the utilisation side
# devs can get the data they want using getattr without having to construct
# there own structures. This is at least true for basic lists and dicts.
APPDATA = {}
EXECLIST = []
DEFMODULES = {}
EXECFLAGS = {}

# Optional param for if the modules are named in a different way to simply
# that the modules are called the same as the software (rare).
MODULEOVERIDES = {}
# Loop through all the modules in the plugin.
for loader, modulename, ispkg in MODULES:

    # check for double loading in the namespace.
    if modulename not in sys.modules:
        # try to import using the pip package path.
        try:
            mod = __import__(
                "Longbow.plugins.apps." + modulename, fromlist=[""])

        except ImportError:
            # Else try to import using the non packaged path.
            try:
                mod = __import__(
                    "plugins.apps." + modulename, fromlist=[""])
            except ImportError:
                # Otherwise we've had it! Raise exception.
                raise

        # Now try and pull in attributes.
        try:
            APPDATA[modulename] = getattr(mod, "EXECDATA")

        except AttributeError:
            raise

        try:
            MODULEOVERIDES[modulename] = getattr(mod, "MODULEOVERIDE")

        except AttributeError:
            MODULEOVERIDES[modulename] = ""

# Construct common structures to make programmers lives easier.
for plugin in APPDATA:
    for executable, flags in APPDATA[plugin].items():
        # compile a list of executables.
        EXECLIST.append(executable)

        # compile dictionary of required input flags.
        EXECFLAGS[executable] = flags

        # Compile a list of default modules.
        if MODULEOVERIDES[plugin] == "":
            DEFMODULES[executable] = plugin
        else:
            DEFMODULES[executable] = MODULEOVERIDES[plugin]
