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

""" This module contains the 'custom' exception classes for the Longbow
corelibrary.
"""

# -----------------------------------------------------------------------------
# Exceptions for paths

class AbsolutepathError(Exception):
    def __init__(self, message, path):

        # Call the base class constructor.
        super(AbsolutepathError, self).__init__(message)

        # Bind the standard outputs.
        self.path = path

# -----------------------------------------------------------------------------
# Exceptions for shellwrappers.py

class LocalcopyError(Exception):
    def __init__(self, message, path):

        # Call the base class constructor.
        super(LocalcopyError, self).__init__(message)

        # Bind the standard outputs.
        self.path = path
        
class LocaldeleteError(Exception):
    def __init__(self, message, path):

        # Call the base class constructor.
        super(LocaldeleteError, self).__init__(message)

        # Bind the standard outputs.
        self.path = path

class LocallistError(Exception):
    def __init__(self, message, path):

        # Call the base class constructor.
        super(LocallistError, self).__init__(message)

        # Bind the standard outputs.
        self.path = path

class ProtocolError(Exception):
    def __init__(self, message, protocol):

        # Call the base class constructor.
        super(ProtocolError, self).__init__(message)

        # Bind the standard outputs.
        self.path = protocol

class RemotecopyError(Exception):
    def __init__(self, message, src, dst):

        # Call the base class constructor.
        super(RemotecopyError, self).__init__(message)

        # Bind the standard outputs.
        self.src = src
        self.dst = dst
        
class RemotedeleteError(Exception):
    def __init__(self, message, path):

        # Call the base class constructor.
        super(RemotedeleteError, self).__init__(message)

        # Bind the standard outputs.
        self.path = path

class RemotelistError(Exception):
    def __init__(self, message, path):

        # Call the base class constructor.
        super(RemotelistError, self).__init__(message)

        # Bind the standard outputs.
        self.path = path

class RsyncError(Exception):
    def __init__(self, message, shellout):

        # Call the base class constructor.
        super(RsyncError, self).__init__(message)

        # Bind the standard outputs.
        self.errorcode = shellout[2]
        self.stdout = shellout[0]
        self.stderr = shellout[1]

class SCPError(Exception):
    def __init__(self, message, shellout):

        # Call the base class constructor.
        super(SCPError, self).__init__(message)

        # Bind the standard outputs.
        self.errorcode = shellout[2]
        self.stdout = shellout[0]
        self.stderr = shellout[1]

class SSHError(Exception):
    def __init__(self, message, shellout):

        # Call the base class constructor.
        super(SSHError, self).__init__(message)

        # Bind the standard outputs.
        self.errorcode = shellout[2]
        self.stdout = shellout[0]
        self.stderr = shellout[1]
