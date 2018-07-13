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

"""This module contains exception class definitions for Longbow.

This module contains the 'custom' exception classes for the Longbow core
library. These exceptions are best used in methods that replace/override those
of the standard library, such that a error messages have more specific
functionality to Longbow.
"""

# -----------------------------------------------------------------------------
# Exceptions for paths


class AbsolutepathError(Exception):

    """Exception class for absolute path errors.

    Usage:
    AbsolutepathError(message, path)
    """

    def __init__(self, message, path):
        """Add the ability to pass the path back to the calling function."""
        # Call the base class constructor.
        super(AbsolutepathError, self).__init__(message)

        # Bind the standard outputs.
        self.path = path


class DirectorynotfoundError(Exception):

    """Directory not found exception."""

    pass


class DisconnectException(Exception):

    """Disconnect exception, for disconnect mode related errors."""

    pass


class UpdateExit(Exception):

    """Exception, to exit gracefully after update of job progress."""

    pass

# -----------------------------------------------------------------------------
# Exceptions for applications.py


class CommandlineargsError(Exception):

    """Command-line arguments exception."""

    pass


class ExecutableError(Exception):

    """Executable not found exception."""

    pass


class RequiredinputError(Exception):

    """Required input error exception."""

    pass

# -----------------------------------------------------------------------------
# Exceptions for configuration.py


class ConfigurationError(Exception):

    """Configuration error."""

    pass

# -----------------------------------------------------------------------------
# Exceptions for plugin.py


class PluginattributeError(Exception):

    """Missing plugin method exception."""

    pass


# -----------------------------------------------------------------------------
# Exceptions for scheduling.py


class SchedulercheckError(Exception):

    """Scheduler checking exception."""

    pass


class HandlercheckError(Exception):

    """Job handler checking exception."""

    pass


class JobdeleteError(Exception):

    """Job delete exception."""

    pass


class JobsubmitError(Exception):

    """Job submit exception."""

    pass


class QueuemaxError(Exception):

    """Job submit exception."""

    pass

# -----------------------------------------------------------------------------
# Exceptions for shellwrappers.py


class LocalcopyError(Exception):

    """Copy on local machine exception.

    Usage:
    LocalcopyError(message, path)
    """

    def __init__(self, message, path):
        """Add the ability to pass the path back to the calling function."""
        # Call the base class constructor.
        super(LocalcopyError, self).__init__(message)

        # Bind the standard outputs.
        self.path = path


class LocaldeleteError(Exception):

    """Delete on local machine exception.

    Usage:
    LocalcopyError(message, path)
    """

    def __init__(self, message, path):
        """Add the ability to pass the path back to the calling function."""
        # Call the base class constructor.
        super(LocaldeleteError, self).__init__(message)

        # Bind the standard outputs.
        self.path = path


class LocallistError(Exception):

    """List on local machine exception.

    Usage:
    LocallistError(message, path)
    """

    def __init__(self, message, path):
        """Add the ability to pass the path back to the calling function."""
        # Call the base class constructor.
        super(LocallistError, self).__init__(message)

        # Bind the standard outputs.
        self.path = path


class RemotecopyError(Exception):

    """Copy on remote machine exception.

    Usage:
    LocallistError(message, sourcepath, destinationpath)
    """

    def __init__(self, message, src, dst):
        """Add the ability to pass the paths back to the calling function."""
        # Call the base class constructor.
        super(RemotecopyError, self).__init__(message)

        # Bind the standard outputs.
        self.src = src
        self.dst = dst


class RemotedeleteError(Exception):

    """Delete on remote machine exception.

    Usage:
    RemotedeleteError(message, path)
    """

    def __init__(self, message, path):
        """Add the ability to pass the path back to the calling function."""
        # Call the base class constructor.
        super(RemotedeleteError, self).__init__(message)

        # Bind the standard outputs.
        self.path = path


class RemotelistError(Exception):

    """List on remote machine exception.

    Usage:
    RemotelistError(message, path)
    """

    def __init__(self, message, path):
        """Add the ability to pass the path back to the calling function."""
        # Call the base class constructor.
        super(RemotelistError, self).__init__(message)

        # Bind the standard outputs.
        self.path = path


class RsyncError(Exception):

    """Rsync exception.

    Usage:
    RemotelistError(message, (stdout, stderr, errcode))
    """

    def __init__(self, message, shellout):
        """Add the ability to pass the shelloutput to the calling function."""
        # Call the base class constructor.
        super(RsyncError, self).__init__(message)

        # Bind the standard outputs.
        self.errorcode = shellout[2]
        self.stdout = shellout[0]
        self.stderr = shellout[1]


class SSHError(Exception):

    """SSH exception.

    Usage:
    RemotelistError(message, (stdout, stderr, errcode))
    """

    def __init__(self, message, shellout):
        """Add the ability to pass the shelloutput to the calling function."""
        # Call the base class constructor.
        super(SSHError, self).__init__(message)

        # Bind the standard outputs.
        self.errorcode = shellout[2]
        self.stdout = shellout[0]
        self.stderr = shellout[1]

# -----------------------------------------------------------------------------
# Exceptions for staging.py


class StagingError(Exception):

    """Generic staging error exception."""

    pass


class RemoteworkdirError(Exception):

    """Remote working directory related generic exception."""

    pass
