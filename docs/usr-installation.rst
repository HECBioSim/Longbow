Installation
************

**Longbow is designed to be as simple as possible to install**

The software has been written in vanilla python to be compatible with versions 3.11 onwards, and has no other dependencies on other python packages. The result is that Longbow is very quick and simple to install.

There are two ways to install Longbow, we recommend you use the pip method, however your circumstances may mean that you require other ways to install (permissions, no pip, no outbound connection, firewall, or testing a development build etc). Each method is detailed below.

Installation with pip
---------------------

By far, the easiest method of installation is to use pip. To install via pip, simply open up a terminal window and type::

    pip install longbow

Better still, to avoid permissions problems or pollution of the system python libraries::

    pip install longbow --user

Test that the installation went ahead::

    longbow --about

If a welcome message is output then you have successfully installed Longbow! If you get an error go to the :ref:`installation-troubleshooting` section to help diagnose your problem.

Finally, notice that the installation process has created the directory ~/.longbow which contains a file called hosts.conf and will be used later to store recovery files.

Installation with setup.py
--------------------------

If you don't/can't have access to pip on your computer then Longbow can be installed via its setup.py script. Before completing the installation, firstly you will need to download Longbow from `here <http://www.hecbiosim.ac.uk/longbow>`_ and then extract the archive. Upon extraction of the zip archive you will find a directory called "Longbow", change into this directory, within this directory you will see there is a python script in there called setup.py. Execute this script::

    python setup.py install

Better still, to avoid permissions problems or pollution of the system python libraries::

    python setup.py install --user

Test that the installation went ahead::

    longbow --about

If a welcome message is output then you have successfully installed Longbow! If you get an error go to the :ref:`installation-troubleshooting` section to help diagnose your problem.

Finally, notice that the installation process has created the directory ~/.longbow which contains a file called hosts.conf and will be used later to store recovery files.



