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

"""."""

import os

EXECDATA = {
    "mdrun": ["-s || -deffnm"],
    "mdrun_d": ["-s || -deffnm"],
    "mdrun_mpi": ["-s || -deffnm"],
    "mdrun_mpi_d": ["-s || -deffnm"]
    }


def defaultfilename(path, item):

    """Method for dealing with input files that are provided by the -deffnm
    flag. The reason this needs a special message is due to the fact that
    users will supply the name as -deffnm test but the file name might be
    test.tpr which would make our code miss the file from the upload list
    """

    filename = ""

    if os.path.isfile(os.path.join(path, item + ".tpr")):

        filename = item + ".tpr"

    return filename
