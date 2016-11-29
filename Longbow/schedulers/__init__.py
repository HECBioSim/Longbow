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

"""This module contains the import logic for the scheduler plugins.

All code for a new plugin should be placed inside the plugin module itself
and not here, follow the template for constructing new app plugins.
"""

import sys
import os
import pkgutil

QUERY = {}

PATH = os.path.dirname(__file__)
MODULES = pkgutil.iter_modules(path=[PATH])

for loader, modulename, ispkg in MODULES:

    if modulename not in sys.modules:

        mod = __import__("Longbow.schedulers." + modulename,
                         fromlist=[""])

        QUERY[modulename] = [getattr(mod, "QUERY_STRING")]
