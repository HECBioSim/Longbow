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
This testing module contains the tests for the prepare method within the
scheduling module.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import longbow.exceptions as exceptions
from longbow.scheduling import prepare


@mock.patch('longbow.schedulers.lsf.prepare')
def test_prepare_single(mock_prepare):

    """
    Test that a single job only tries to create a submit file once.
    """

    jobs = {
        "job-one": {
            "resource": "test-machine",
            "scheduler": "LSF",
            "jobid": "test456",
            "subfile": ""
        }
    }

    prepare(jobs)

    assert mock_prepare.call_count == 1, \
        "For a single job this method should only be called once"


@mock.patch('longbow.schedulers.lsf.prepare')
def test_prepare_multiple(mock_prepare):

    """
    Test that for multiple jobs the correct number of submit files are called
    for creation.
    """

    jobs = {
        "job-one": {
            "resource": "test-machine",
            "scheduler": "LSF",
            "jobid": "test123",
            "subfile": ""
        },
        "job-two": {
            "resource": "test-machine",
            "scheduler": "LSF",
            "jobid": "test456",
            "subfile": ""
        },
        "job-three": {
            "resource": "test-machine",
            "scheduler": "LSF",
            "jobid": "test789",
            "subfile": ""
        }
    }

    prepare(jobs)

    assert mock_prepare.call_count == 3, \
        "For a multi job this method should be called once for each job"


@mock.patch('longbow.schedulers.lsf.prepare')
def test_prepare_attrexcept(mock_prepare):

    """
    Test that errors with missing plugins are handled correctly.
    """

    jobs = {
        "job-one": {
            "resource": "test-machine",
            "scheduler": "LSF",
            "jobid": "test456",
            "subfile": ""
        }
    }

    mock_prepare.side_effect = AttributeError

    with pytest.raises(exceptions.PluginattributeError):

        prepare(jobs)


@mock.patch('longbow.schedulers.lsf.prepare')
def test_prepare_ownscript(mock_prepare):

    """
    Test that if user supplies a script that longbow doesn't create one.
    """

    jobs = {
        "job-one": {
            "resource": "test-machine",
            "scheduler": "LSF",
            "jobid": "test456",
            "subfile": "test.lsf",
            "upload-include": "file1, file2, file3"
        }
    }

    prepare(jobs)

    assert mock_prepare.call_count == 0, \
        "This method shouldn't be called at all in this case."
    assert jobs["job-one"]["upload-include"] == "file1, file2, file3, test.lsf"
