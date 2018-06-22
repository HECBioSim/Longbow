.. _troubleshooting:

Troubleshooting
***************

If you are unable to find a solution to your problem listed here, then you should contact us for support.

.. _installation-troubleshooting:

Installation Troubleshooting
============================

The issues in this section relate to problems encountered during or immediately related to the installation of Longbow.

**When I try to launch Longbow I see a "Command not found" error message**

If after installing Longbow, the command::

    longbow --about

produces an error message similar to "longbow: Command not found", first open a new terminal and try again. If the same output is observed, execute the command::

    echo $PATH

If in the output of this command, you cannot see the directory in which the longbow executable of the same name is installed (usually in ~/.local/bin), then you need to add this path to your environment.

If you use the Bash shell, add the following lines to your ~/.bashrc file::

    PATH="/home/user/.local/bin:${PATH}"
    export PATH

On the other hand, if you use a C shell, add the following lines to your ~/.cshrc file::

    set path = ( /home/user/.local/bin $path )

To activate these changes, either close and reopen your terminal or use the source command::

    source ~/.bashrc

for bash or for c shell::

    source ~/.cshrc

**When I try to launch Longbow I see the message "Permission Denied"**


This is usually due to the execute permission not being granted on the Longbow executable file during installation. To remedy this you will need to grant permission for the Longbow executable to be executed. To do this you will need to run chmod on the longbow executable (usually this is in ~/.local/bin) to add the execute permission by doing::

    chmod +x path/to/longbow

If you are having difficulties finding the Longbow executable then the following might help you based on which installation methods you chose during installation.

1. using pip or the manual setup script as root - usually when using this method the executable should be in /usr/local/bin/

2. using pip or setup script with --user - usually with this method the executable will be in ~/.local/bin/

3. manual install - the Longbow executable will be where you unpacked the archive after download.

Troubleshooting Longbow Examples
================================

Due to the inevitable variation between environments, some users may find that the example job in the Running Longbow Examples section of this user guide will not run first time. The point of failure will be output to the log file and also the console if the --verbose flag is used on the command line.

To overcome the variation between systems, Longbow has numerous parameters that can be specified in configuration files to support a range of requirements. Read the Longbow Configuration section of this user guide to see which other parameters or command line options could be included to enable your job to run.

If you can successfully reach the stage where a submit.* file is created in the example directory, compare this file to a standard submission script you would normally use to run jobs on the remote resource. In this way, one can identify what information may be missing with the current configuration setup.

 
General troubleshooting
=======================

**When I use < or > on the desktop terminal to supply an input script for an MD job or to redirect output, it doesn't work**

When launching longbow with the < or > characters in the commandline, your shell will interpret these as pipes for input and output to longbow itself. To get around this put the < or > in quotation marks e.g::

    longbow charmm "<" input.inp

