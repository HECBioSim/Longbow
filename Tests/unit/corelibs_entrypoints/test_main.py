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
This testing module contains the tests for the main method within the
entrypoint module.
"""

import os

try:

    from unittest import mock

except ImportError:

    import mock

import Longbow.corelibs.exceptions as exceptions
import Longbow.corelibs.entrypoints as mains


@mock.patch('Longbow.corelibs.entrypoints.longbowmain')
@mock.patch('os.path.isfile')
def test_main_test1(m_isfile, m_longbowmain):

    """
    Check that the longbow main method gets called, and that the parameters
    structure is being setup, this is a rudimentary test.
    """

    m_isfile.return_value = True

    args = ["longbow", "--jobname", "testjob", "--verbose", "pmemd.MPI", "-O",
            "-i", "ex.in", "-c", "ex.min", "-p", "ex.top", "-o", "ex.out"]

    with mock.patch('sys.argv', args):

        mains.main()

    params = m_longbowmain.call_args[0][0]

    assert m_longbowmain.call_count == 1
    assert params["debug"] is False
    assert params["disconnect"] is False
    assert params["executable"] == "pmemd.MPI"
    assert params["executableargs"] == ["-O", "-i", "ex.in", "-c", "ex.min",
                                        "-p", "ex.top", "-o", "ex.out"]
    assert params["hosts"] == os.path.join(os.getcwd(), "hosts.conf")
    assert params["job"] == ""
    assert params["jobname"] == "testjob"
    assert params["log"] == os.path.join(os.getcwd(), "log")
    assert params["recover"] == ""
    assert params["resource"] == ""
    assert params["replicates"] == ""
    assert params["verbose"] is True


@mock.patch('Longbow.corelibs.entrypoints.longbowmain')
@mock.patch('os.path.isfile')
def test_main_test2(m_isfile, m_longbowmain):

    """
    Check that the longbow main method gets called, and that the parameters
    structure is being setup, this is a rudimentary test.
    """

    m_isfile.return_value = True

    args = ["longbow", "--jobname", "testjob", "--resource", "big-machine",
            "--verbose", "pmemd.MPI", "-O", "-i", "ex.in", "-c", "ex.min",
            "-p", "ex.top", "-o", "ex.out"]

    with mock.patch('sys.argv', args):

        mains.main()

    params = m_longbowmain.call_args[0][0]

    assert m_longbowmain.call_count == 1
    assert params["debug"] is False
    assert params["disconnect"] is False
    assert params["executable"] == "pmemd.MPI"
    assert params["executableargs"] == ["-O", "-i", "ex.in", "-c", "ex.min",
                                        "-p", "ex.top", "-o", "ex.out"]
    assert params["hosts"] == os.path.join(os.getcwd(), "hosts.conf")
    assert params["job"] == ""
    assert params["jobname"] == "testjob"
    assert params["log"] == os.path.join(os.getcwd(), "log")
    assert params["recover"] == ""
    assert params["resource"] == "big-machine"
    assert params["replicates"] == ""
    assert params["verbose"] is True


@mock.patch('Longbow.corelibs.entrypoints.recovery')
@mock.patch('os.path.isfile')
def test_main_test3(m_isfile, m_recovery):

    """
    Check that the recovery method gets called, this is a rudimentary test.
    """

    m_isfile.return_value = True

    args = ["longbow", "--recover", "recovery.file", "--log", "new-log.file",
            "--verbose"]

    with mock.patch('sys.argv', args):

        mains.main()

    params = m_recovery.call_args[0][0]

    assert m_recovery.call_count == 1
    assert params == "recovery.file"


@mock.patch('Longbow.corelibs.entrypoints.longbowmain')
@mock.patch('os.path.isfile')
def test_main_test4(m_isfile, m_longbowmain):

    """
    Test that exception handling happens properly.
    """

    m_isfile.return_value = True

    args = ["longbow", "--jobname", "testjob", "--resource", "big-machine",
            "pmemd.MPI", "-O", "-i", "ex.in", "-c", "ex.min", "-p", "ex.top",
            "-o", "ex.out"]

    m_longbowmain.side_effect = exceptions.PluginattributeError

    with mock.patch('sys.argv', args):

        mains.main()

    params = m_longbowmain.call_args[0][0]

    assert m_longbowmain.call_count == 1
    assert params["debug"] is False
    assert params["disconnect"] is False
    assert params["executable"] == "pmemd.MPI"
    assert params["executableargs"] == ["-O", "-i", "ex.in", "-c", "ex.min",
                                        "-p", "ex.top", "-o", "ex.out"]
    assert params["hosts"] == os.path.join(os.getcwd(), "hosts.conf")
    assert params["job"] == ""
    assert params["jobname"] == "testjob"
    assert params["log"] == os.path.join(os.getcwd(), "log")
    assert params["recover"] == ""
    assert params["resource"] == "big-machine"
    assert params["replicates"] == ""
    assert params["verbose"] is False


@mock.patch('Longbow.corelibs.entrypoints.longbowmain')
@mock.patch('os.path.isfile')
def test_main_test5(m_isfile, m_longbowmain):

    """
    Test that exception handling happens properly.
    """

    m_isfile.return_value = True

    args = ["longbow", "--jobname", "testjob", "--resource", "big-machine",
            "--debug", "pmemd.MPI", "-O", "-i", "ex.in", "-c", "ex.min", "-p",
            "ex.top", "-o", "ex.out"]

    m_longbowmain.side_effect = exceptions.PluginattributeError

    with mock.patch('sys.argv', args):

        mains.main()

    params = m_longbowmain.call_args[0][0]

    assert m_longbowmain.call_count == 1
    assert params["debug"] is True
    assert params["disconnect"] is False
    assert params["executable"] == "pmemd.MPI"
    assert params["executableargs"] == ["-O", "-i", "ex.in", "-c", "ex.min",
                                        "-p", "ex.top", "-o", "ex.out"]
    assert params["hosts"] == os.path.join(os.getcwd(), "hosts.conf")
    assert params["job"] == ""
    assert params["jobname"] == "testjob"
    assert params["log"] == os.path.join(os.getcwd(), "log")
    assert params["recover"] == ""
    assert params["resource"] == "big-machine"
    assert params["replicates"] == ""
    assert params["verbose"] is False


@mock.patch('Longbow.corelibs.entrypoints.recovery')
@mock.patch('Longbow.corelibs.entrypoints.longbowmain')
@mock.patch('os.path.isfile')
def test_main_test6(m_isfile, m_longbowmain, m_recovery):

    """
    Test that exception handling happens properly.
    """

    m_isfile.return_value = True

    args = ["longbow", "--jobname", "testjob", "--resource", "big-machine",
            "--debug"]

    with mock.patch('sys.argv', args):

        mains.main()

    assert m_longbowmain.call_count == 0
    assert m_recovery.call_count == 0
