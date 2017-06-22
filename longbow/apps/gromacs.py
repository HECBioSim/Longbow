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

"""This is the GROMACS plugin module.

This plugin is relatively simple in the fact that adding new executables is as
simple as modifying the EXECDATA structure below. See the documentation at
http://www.hecbiosim.ac.uk/longbow-devdocs for more information.
"""

import os

EXECDATA = {
    "gmx": {
        "subexecutables": ["mdrun", "mdrun_mpi"],
        "requiredfiles": ["-s || -deffnm"],
    },
    "gmx_d": {
        "subexecutables": ["mdrun", "mdrun_mpi"],
        "requiredfiles": ["-s || -deffnm"],
    },
    "mdrun": {
        "subexecutables": [],
        "requiredfiles": ["-s || -deffnm"],
    },
    "mdrun_d": {
        "subexecutables": [],
        "requiredfiles": ["-s || -deffnm"],
    },
    "mdrun_mpi": {
        "subexecutables": [],
        "requiredfiles": ["-s || -deffnm"],
    },
    "mdrun_mpi_d": {
        "subexecutables": [],
        "requiredfiles": ["-s || -deffnm"],
    }
}


def defaultfilename(path, item, initargs):
    """Process tpr files provided by the -deffnm flag.

    The reason this needs a special method is due to the fact that users will
    supply the name as -deffnm test but the file name might be test.tpr which
    would make our code miss the file from the upload list.

    """
    filename = ""

    if os.path.isfile(os.path.join(path, item + ".tpr")):

        filename = item + ".tpr"

        if initargs != "" and "-s" not in initargs and "-deffnm" in initargs:

            index = initargs.index("-deffnm")

            initargs.insert(index, os.path.join("../", filename))
            initargs.insert(index, "-s")

    return filename, initargs
