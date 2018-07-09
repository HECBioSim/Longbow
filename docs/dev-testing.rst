Testing
*******

Developers contributing code to the Longbow base code will be expected to provide unit tests for their contributions and have these passing at time of merger, pull requests with failing tests will not be accepted. It is also strongly suggested to gain as much testing coverage as possible for contributions, as poor coverage will also lead to rejected contributions.

The unit tests are run via Travis CI automatically upon commits and pull requests to assist maintainers with assessing whether code contributions represent the quality and stability our users deserve.

Developers can rely on the Travis tests if they like, but this can often mean a lot of little tweaks need commiting to GitHub branches before they are ready. It is often a better idea to implement local testing with your installed Python toolchain and then push to GitHub and have Travis do the multi-version based testing.

A convenient way to set up a simple test environment locally is to implement the following recipe.

**1. Install testing tools**

To start testing, you'll need some tools, so first thing is to get these if you haven't already.

unit testing::

    pip install --user pytest

mock::

    pip install --user mock

code coverage::

    pip install --user coverage

beautify output (optional)::

    pip install --user pytest-sugar

**2. Make testing script to copy source and launch test suite**

Next, you will need a way to run your tests without disturbing your pristine source code. The simplest way to do this is have a simple script copy and launch your tests. To do this creare a bash script::

    nano ~/.local/bin/test-longbow

and add::

    #!/usr/bin/env bash

    # copy source to user home directory
    cp -r /path/to/your/longbow-source ~

    # change path to longbow source
    cd ~/Longbow

    # run tests and report coverage
    coverage run --source longbow -m py.test
    coverage report -m

    # after testing, clean up
    cd ..
    rm -rf ~/Longbow

after saving, make it executable::

    chmod +x ~/.local/bin/test-longbow

that should be it. You should simply be able to run "test-longbow" and see the unit testing suite run its tests locally on your machine. This will give details of the coverage report so that you can see lines that are not covered by testing and details of any tests that fail as a result of your changes. Failing tests are not always a bad idea, you may have altered core functionality to fix a bug that is currently passing an existing test, you should then fix the existing tests to test your new code.

Thats it, happy coding.....

