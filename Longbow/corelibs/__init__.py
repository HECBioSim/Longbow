# Longbow is Copyright (C) of James T Gebbie-Rayet 2015.
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

"""Import main classes so that we can just use imports of the style:

import core

"""

from .shellwrappers import (testconnections, sendtoshell, sendtossh, sendtoscp,
                            sendtorsync, localcopy, localdelete, locallist,
                            remotecopy, remotedelete, remotelist, upload,
                            download)
from .configuration import loadhosts, loadjobs, loadconfigs, saveconfigs
from .applications import testapp, processjobs
from .sheduling import testenv, prepare, submit, delete, monitor
from .staging import stage_upstream, stage_downstream, cleanup
from .logger import setuplogger
