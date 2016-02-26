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
This module provides the basic import framwork for Longbow plug-ins. On import,
this module will import an plug-in packages that are contained within the
plug-ins directory. This gives direct access to any new plug-ins that are added
to the directory for use within the core library.
"""

import pkgutil
import os
import sys

PATH = os.path.dirname(__file__)
PACKAGES = pkgutil.walk_packages(path=[PATH])
PLUGINS = {}

for packageloader, packagename, ispkg in PACKAGES:
    try:
        package = __import__("Longbow.plugins." + packagename)

    except ImportError:
        package = __import__("plugins." + packagename)

    PLUGINS[packagename] = "plugins." + packagename
