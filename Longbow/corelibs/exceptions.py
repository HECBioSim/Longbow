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
This module contains the 'custom' exception classes for the Longbow core
library. These exceptions are best used in methods that replace/override those
of the core library, such that a developer can make use of the error handling
framework more organically.
"""

# -----------------------------------------------------------------------------
# Exceptions for paths


class AbsolutepathError(Exception):

    """
    Exception class for absolute path errors, usage

    AbsolutepathError(message, path)
    """

    def __init__(self, message, path):

        # Call the base class constructor.
        super(AbsolutepathError, self).__init__(message)

        # Bind the standard outputs.
        self.path = path


class DirectorynotfoundError(Exception):

    """
    Directory not found exception, to provide informative exceptions
    of why a method has failed when directory cannot be found.
    """

    pass


class DisconnectException(Exception):

    """
    Directory not found exception, to provide informative exceptions
    of why a method has failed when directory cannot be found.
    """

    pass

# -----------------------------------------------------------------------------
# Exceptions for applications.py


class CommandlineargsError(Exception):

    """
    Command-line arguments error.
    """

    def __init__(self, message):

        # Call the base class constructor.
        super(CommandlineargsError, self).__init__(message)


class RequiredinputError(Exception):

    """
    Required input error exception.
    """

    def __init__(self, message):

        # Call the base class constructor.
        super(RequiredinputError, self).__init__(message)

# -----------------------------------------------------------------------------
# Exceptions for configuration.py


class ConfigurationError(Exception):

    """
    Configuration error.
    """

    pass

# -----------------------------------------------------------------------------
# Exceptions for plugin.py


class PluginattributeError(Exception):

    """
    Missing plugin method exception.
    """

    pass


# -----------------------------------------------------------------------------
# Exceptions for scheduling.py


class SchedulercheckError(Exception):

    """
    Scheduler checking exception.
    """

    pass


class HandlercheckError(Exception):

    """
    Job handler checking exception.
    """

    pass


class JobdeleteError(Exception):

    """
    Job delete exception.
    """

    pass


class JobsubmitError(Exception):

    """
    Job submit exception.
    """

    pass


class QueuemaxError(Exception):

    """
    Job submit exception.
    """

    pass

# -----------------------------------------------------------------------------
# Exceptions for shellwrappers.py


class LocalcopyError(Exception):

    """
    Copy on local machine exception.
    """

    def __init__(self, message, path):

        # Call the base class constructor.
        super(LocalcopyError, self).__init__(message)

        # Bind the standard outputs.
        self.path = path


class LocaldeleteError(Exception):

    """
    Delete on local machine exception.
    """

    def __init__(self, message, path):

        # Call the base class constructor.
        super(LocaldeleteError, self).__init__(message)

        # Bind the standard outputs.
        self.path = path


class LocallistError(Exception):

    """
    List on local machine exception.
    """

    def __init__(self, message, path):

        # Call the base class constructor.
        super(LocallistError, self).__init__(message)

        # Bind the standard outputs.
        self.path = path


class ProtocolError(Exception):

    """
    Unknown protocol exception.
    """

    def __init__(self, message, protocol):

        # Call the base class constructor.
        super(ProtocolError, self).__init__(message)

        # Bind the standard outputs.
        self.path = protocol


class RemotecopyError(Exception):

    """
    Copy on remote machine exception.
    """

    def __init__(self, message, src, dst):

        # Call the base class constructor.
        super(RemotecopyError, self).__init__(message)

        # Bind the standard outputs.
        self.src = src
        self.dst = dst


class RemotedeleteError(Exception):

    """
    Delete on remote machine exception.
    """

    def __init__(self, message, path):

        # Call the base class constructor.
        super(RemotedeleteError, self).__init__(message)

        # Bind the standard outputs.
        self.path = path


class RemotelistError(Exception):

    """
    List on remote machine exception.
    """

    def __init__(self, message, path):

        # Call the base class constructor.
        super(RemotelistError, self).__init__(message)

        # Bind the standard outputs.
        self.path = path


class RsyncError(Exception):

    """
    Rsync exception.
    """

    def __init__(self, message, shellout):

        # Call the base class constructor.
        super(RsyncError, self).__init__(message)

        # Bind the standard outputs.
        self.errorcode = shellout[2]
        self.stdout = shellout[0]
        self.stderr = shellout[1]


class SSHError(Exception):

    """
    SSH exception
    """

    def __init__(self, message, shellout):

        # Call the base class constructor.
        super(SSHError, self).__init__(message)

        # Bind the standard outputs.
        self.errorcode = shellout[2]
        self.stdout = shellout[0]
        self.stderr = shellout[1]

# -----------------------------------------------------------------------------
# Exceptions for staging.py


class StagingError(Exception):

    """
    Generic staging error exception
    """

    pass


class RemoteworkdirError(Exception):

    """
    Exception issued when destdir is the same path as remoteworkdir
    """

    pass
