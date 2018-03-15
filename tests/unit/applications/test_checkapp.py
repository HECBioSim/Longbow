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

"""
This testing module contains the tests for the applications module methods.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

from longbow.applications import checkapp
import longbow.exceptions as ex


@mock.patch('longbow.shellwrappers.sendtossh')
def test_testapp_exectest(m_sendtossh):

    """
    Test that the executable query is formatted correctly.
    """

    jobs = {
        "jobone": {
            "resource": "res1",
            "executable": "exec1",
            "modules": "",
            "nochecks": "false"
        }
    }

    checkapp(jobs)

    assert m_sendtossh.call_count == 1
    assert m_sendtossh.call_args[0][1] == ["which exec1"]


@mock.patch('longbow.shellwrappers.sendtossh')
def test_testapp_moduletest(m_sendtossh):

    """
    Test that modules to be loaded are appended into the executable query
    string.
    """

    jobs = {
        "jobone": {
            "resource": "res1",
            "executable": "exec1",
            "modules": "intel, amber",
            "nochecks": "false"
        }
    }

    checkapp(jobs)

    assert m_sendtossh.call_count == 1
    assert "which exec1" in m_sendtossh.call_args[0][1]
    assert "module load intel\n" in m_sendtossh.call_args[0][1]
    assert "module load amber\n" in m_sendtossh.call_args[0][1]


@mock.patch('longbow.shellwrappers.sendtossh')
def test_testapp_except(m_sendtossh):

    """
    Test that modules to be loaded are appended into the executable query
    string.
    """

    jobs = {
        "jobone": {
            "resource": "res1",
            "executable": "exec1",
            "modules": "intel, amber",
            "nochecks": "false"
        }
    }

    m_sendtossh.side_effect = ex.SSHError("Error", ("stdout", "stderr", 1))

    with pytest.raises(ex.ExecutableError):

        checkapp(jobs)
