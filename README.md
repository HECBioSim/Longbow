[![ci](https://github.com/HECBioSim/Longbow/actions/workflows/ci.yaml/badge.svg)](https://github.com/HECBioSim/Longbow/actions/workflows/ci.yaml)
![PyPI - Version](https://img.shields.io/pypi/v/longbow?logo=pypi&logoColor=white)
![PyPI - Status](https://img.shields.io/pypi/status/longbow?logo=pypi&logoColor=white)
![PyPI - Downloads](https://img.shields.io/pypi/dm/longbow?logo=pypi&logoColor=white)
[![Coverage Status](https://coveralls.io/repos/github/HECBioSim/Longbow/badge.svg?branch=main)](https://coveralls.io/github/HECBioSim/Longbow?branch=main)
[![Docs - Status](https://readthedocs.org/projects/longbow/badge/?version=latest)](https://longbow.readthedocs.io/en/latest/?badge=latest)

# Longbow

Longbow is an automated simulation submission and monitoring tool. Longbow
is designed to reproduce the look and feel of using software on the users
local computer with the difference that the heavy lifting is done by a
supercomputer.

Longbow will automatically generate the necessary submit files and handle all
initial file transfer, monitor jobs, transfer files at configurable
intervals and perform final file transfer and cleanup.

Longbow can be used to launch one-off jobs, generate ensembles of similar jobs
or even run many different jobs over many different supercomputers.

Out of the box, Longbow is currently supporting the PBS/Torque, LSF, SGE,
Slurm, SoGE schedulers and ships with application plugins for commonly used
bio-molecular simulation softwares AMBER, CHARMM, GROMACS, LAMMPS, NAMD.
Longbow is however highly configurable and will function normally with generic
software without plugins, however plugins can easily be made to extend Longbow
to fully support applications and schedulers that do not ship out of the box.

Using Longbow can be as simple as the following example:

local: executable -a arg1 -b arg2 -c arg3

remote: longbow executable -a arg1 -b arg2 -c arg3

Longbow is also available to developers of applications which require support
for automating job submission. Longbow is available as a convenient and
light-weight python API that can be integrated in a number of different way.


## Licensing

Longbow is released under the BSD 3-clause license. A copy of this license is
provided when Longbow is downloaded and installed.


## Citing

If you make use of Longbow in your own code or in production simulations that
result in publishable output, then please reference our paper:

Gebbie-Rayet, J, Shannon, G, Loeffler, H H and Laughton, C A 2016 Longbow: 
A Lightweight Remote Job Submission Tool. Journal of Open Research Software, 
4: e1, DOI: http://dx.doi.org/10.5334/jors.95


## Installation

Releases can be installed either via pip or can be installed manually, to
install via pip:

pip install longbow

or to install manually (see docs) Longbow can be downloaded here:

http://www.hecbiosim.ac.uk/longbow

and then extract and run the setup.py script to install.


## Documentation

Documentation for Longbow users can be found here:

http://www.hecbiosim.ac.uk/longbow-docs


## Examples

Example files can be installed either through the Longbow command-line or by
downloading from the HECBioSim website manually:

longbow --examples

http://www.hecbiosim.ac.uk/longbow-examples


## Support

Support for any issues arising from using Longbow, whether these are questions,
to report a bug or to suggest new ideas. You should use the Longbow forums
here:

https://github.com/HECBioSim/Longbow/issues


## Developers

Developers that wish to contribute to Longbow are welcome. We do ask that if
you wish to contribute to the Longbow base code that you contact us first.

The following resources are available to developers:

Code repository: https://github.com/hecbiosim/longbow

Unit testing: https://github.com/HECBioSim/Longbow/actions

Code coverage: https://coveralls.io/github/HECBioSim/Longbow
