# Longbow is Copyright (C) of James T Gebbie-Rayet and Gareth B Shannon 2015.
#
# This file is part of Longbow.
#
# Longbow is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Longbow is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Longbow.  If not, see <http://www.gnu.org/licenses/>.

"""Simple plug-ins framework making use of the python package system, upon
including plugins this will import all sub packages as plugins. You can then
provide "hooks" using a try/except wrapped around:

getattr("plugin name", "thing you want")

"""

import pkgutil
import os
import sys

PATH = os.path.dirname(__file__)
PACKAGES = pkgutil.walk_packages(path=[PATH])
PLUGINS = {}

for packageloader, packagename, ispkg in PACKAGES:
    package = __import__("plugins." + packagename)
    PLUGINS[packagename] = "plugins." + packagename
