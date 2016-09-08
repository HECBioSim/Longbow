Longbow is a piece of software that acts as a job proxying tool for 
biomolecular simulations, Longbow reproduces the native look and feel of using
popular molecular dynamics packages (AMBER, CHARMM, GROMACS, LAMMPS and NAMD),
with the difference that when those packages are used through Longbow 
simulations can be run on High Performance Computing (HPC) resources such as 
ARCHER. Longbow handles jobs setup in terms of creating job submission scripts, 
automatically stages input files, launches and monitors jobs and stages back 
simulation results. The option is also there to persistently monitor and stage 
(realtime local syncing with remote simulation files) simulation files at a 
specified time interval.


This is designed to have the jobs running on the HPC remote resource appear to 
the user as if the simulation has run on their local computer/cluster. Users do
not have to concern themselves with writing submission files, nor do they have 
to worry about staging. Longbow provides a convenient interface for generating 
large ensembles of simulation jobs which in effect extends the packages it 
supports.


Licensing
=========

Longbow is released under the GNU GPLv2 license. A copy of this license will
be provided with the Longbow application when it is downloaded and installed.


Citing
======

If you make use of Longbow in your own code or in production simulations that
result in publishable output, then please reference our paper:

Gebbie-Rayet, J, Shannon, G, Loeffler, H H and Laughton, C A 2016 Longbow: 
A Lightweight Remote Job Submission Tool. Journal of Open Research Software, 
4: e1, DOI: http://dx.doi.org/10.5334/jors.95


Installation
============

Releases can be installed either via pip or can be installed manually, to
install via pip:

pip install longbow

or to install manually (see docs) Longbow can be downloaded here:

http://www.hecbiosim.ac.uk/longbow

Please note: In cases where you run the setup script, Longbow will create the
host configuration file in a hidden directory in your user directory. In some
cases doing a manual install (not using the setup.py) then you will have to
make this yourself.


Documentation
=============

Documentation for Longbow can be found here:

http://www.hecbiosim.ac.uk/longbow-docs


Examples
========

Example files can be installed either through the Longbow command-line or by
downloading from the HECBioSim website manually here:

http://www.hecbiosim.ac.uk/longbow-examples


Support
=======

Support for any issues arising from using Longbow, whether these are questions, 
to report bug or to suggest new ideas. You should use the Longbow forums here:

http://www.hecbiosim.ac.uk/longbow-support


Developers
==========

Developers of software that wish to contribute to Longbow/integrate Longbow 
into other software tools are welcome, we do ask that if you wish to contribute
to the Longbow base code that you contact us first. The following resources are
available to developers:

source code: https://github.com/jimboid/longbow

documentation: http://www.hecbiosim.ac.uk/longbow-devdocs
