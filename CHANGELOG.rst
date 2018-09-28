Changelog
*********

Changes to the Longbow source code are listed below by release version.

Version 1.5.2
-------------

1. Bug fix - OMP environment variable added to all schedulers to fix a specific
   set of user reported issues (issue #114).

2. Bug fix - Further PBS and NAMD SMP issues relating to under subscription,
   users had to do a hacky way by dropping the corespernode parameter to under
   subscribe which resulted in errors from the scheduler. Now users wishing to
   do this should set mpiprocs in their job or host conf files to do this (issue #105).

3. Bug fix - The memory parameter only worked with the PBS scheduler, this has
   now been extended to work in all schedulers (issue #98).

4. Bug fix - The --maxtime parameter went missing from the --help output (issue #96).

5. Doc fix - The documentation for the recovery mode was incorrect (issue #102).

6. New feature - An update mode has been added so that users doing
   disconnectable sessions can simply run an update to get the current
   simulation status and download a snapshot of the data (issue #61).
   
7. New feature - Move documentation to be under version control, using sphinx
   and readthedocs for auto documentation assembly. Documentation can then
   become part of the CI cycle and thus be enforced on code contribution (issue #90).
   
8. Enhancement - users can now explicitly set the filenames of stderr and
   stdout from the scheduler script using the parameters "stdout = filename"
   and "stderr = filename" in their host of job conf files (issue #108).
   
9. Enhancement - Users can now make use of existing job scripts, by providing
   the name of the script to the parameter "subfile" in their host or job conf
   files. This mode is mainly aimed at advanced users that understand the short
   falls of doing this and the problems that could occur (issue #77).

10. Enhancement - Users can now set the naming scheme of the replicate
    directories. Instead of having to provide directories of the form
    rep1, rep2, ...., repx. Users can now set the name of the "rep" part by
    setting the "replicate-naming" parameter. So "replicate-naming = foo"
    would need directories named foo1, foo2, ...., foox (issue #92).

11. Enhancement - Documentation for the examples have been cleaned up and added
    to the new sphinx docs (issue #10).

12. Enhancement - Refactor the exception code in the top level API methods to
    remove duplication (issue #44).
   
13. Removed support for Python versions 2.6, 3.2 and 3.3 due to these versions
    being old unsupported versions and various python packages such as 
    pip/ci-tools withdrawing support. Longbow may still work for these versions
    but this is no longer guaranteed (issue #113).


Version 1.5.1
-------------

1. Bug fix - a number of parameters that are only used in specific scheduler or
   application plugins have been renamed to include the plugin name prefix (issue #54).

2. Bug fix - executables expressed as absolute paths for supported plugins
   would cause a crash due to searching for a module with that key (issue #63).

3. Bug fix - wrong error message was displayed when an executable didn't exist
   on HPC machine (issue #65).

4. Bug fix - fix for crash when using NAMD SMP builds, the commandline
   parameters beginning with "+" would trigger the crash (issue #66).

5. Bug fix - fixed misleading error messages about missing files and flags (issue #67).

6. Bug fix - fixed problem where the newly added bash autocomplete did not
   allow filenames on disk to autocomplete (issue #68).

7. Bug fix - fixed a problem when a large number of short jobs that trigger job
   subqueuing would cause a crash (issue #72).

8. Bug fix - fixed user reported bug with strange looking error messages
   concealing a further absolute path bug (issue #75).

9. New feature - Added support for the slurm gres flag so users can do
   something like this "slurm-gres = gpu:1" in their host or job conf files (issue #76).

10. Bug fix - Restored the ability to issue --maxtime on the commandline (issue #78).

11. New feature - support added for the upcoming release of python chemshell (issue #80).

12. Bug fix - fix for problem where parameters in configuration files
    containing the "=" sign would cause the input file parser to misread
    them (issue #81).

13. Bug fix - fix for problem with LAMMPS jobs where files provided with
    "include" or as part of other parameters would not be transferred, thanks
    to Anders Johansson for suggesting some ideas and solutions (issue #86).

14. The structure of the Longbow API has been simplified, the source files no
    longer reside in a subdirectory called "core" within the installation
    directory. This has made importing much simpler and imports shorter.

15. Examples have been restructured and the how to run instructions updated.
    The actual run files remain the same, there are still incompatibilities
    with these and newer versions of MD codes but this will be addressed in
    the next version.


Version 1.5.0
-------------

1. Change of license from GPLv2 to the BSD 3 clause license. This will resolve
   the copy-left issues a number of projects are having (Issue #30).

2. Fix for problem where environment is not properly loaded on some machines,
   this is a non-login shell related problem (Issue #4).

3. Removal of capitalisation from around the whole project for convenience
   (Issues #26 #28 #46 #47).

4. Longbow will now clean out recovery files upon successful completion of the
   session (Issue #24).

5. Bash autocomplete creation added to the setup.py (Issue #23 #49).

6. Fix for bad exit from recovery mode when user issues a keyboard interrupt
   (ctrl-c) (Issue #25).

7. Fix for monitoring phase causing CPU to be spun up to 100% (Issue #35).

8. Fix for bug when examples are downloaded in app, the original zip archive
   is not removed after extraction (Issue #34).

9. Fixed a bug in setup script with the python version check code (Issue #32).

10. Python 3.6 added to supported versions (Issue #33).

11. All public methods in the Longbow API can now be accessed from a single
    import, (ie "import longbow" then "longbow.somemethod()") (Issue #27).


Version 1.4.0
-------------

This release is a rather large release with a lot of changes to the code and
also to the way things are being done. This project is moving towards using CI
tools more and more, and in this release and all future releases tools for
automated unit testing and code quality checks will be used. 

In this release the following changes have been made in this regard:

1. Travis-CI is now used to automate testing for all versions of python 2.6
   through 3.5 https://travis-ci.org/HECBioSim/Longbow.

2. Unit testing added to repository and increased to 100% code coverage. Badges
   have also been implemented so users can monitor success rate. Code coverage
   is picked up from Travis and compiled at
   https://coveralls.io/github/HECBioSim/Longbow.

3. Automated running of code quality checks is now triggered via github pushes
   and is done at https://landscape.io/github/HECBioSim/Longbow

These tools will eventually be used to test upon merge into the main two
branches of the repo (master and development) and will have tolerances set for
auto-rejection.

The actual changes to the code are:

1. Added in some extra commonly found naming for GROMACS executables
   (gmx_mpi and gmx_mpi_d).

2. Bugs detected in shellwrappers.py during unit test writing have now been
   fixed.

3. Fixed formatting issue with logging in staging.py - stage_downstream().

4. Removed import statements for relative imports, this eliminated the need for
   the try/except imports at the top of each code module.

5. The parameter "frequency" has been split into two parameters
   "polling-frequency" and "staging-frequency". This enables the user to have
   Longbow poll jobs without staging all the time.

6. The timing mechanism for timing between polling events has now been changed
   from a disruptive wait() to a timestamp comparison. This stops the process
   being "blocked" by wait() and in future will allow the addition of other
   features that can happen on different timelines to polling.

7. There are now two steps to job completion, instead of marking a job as
   finished when it is finished on the remote host and results downloaded,
   Longbow will now mark at as finished as it is finished on the remote host
   and then once staging has happened it will then be marked as complete.

8. Fixed glitch in applications.py processjobs() where the wrong comparitor was
   used on the if statement to construct the upload include list.

9. Huge refactoring of code to break down larger methods into smaller easier to
   test methods. All new methods are private methods (starting with "_") these
   should not be used by people making use of Longbow in their own code, unless
   they know what they are doing!

10. Moved all code for Longbow entrypoints out of the executable and into
    corelibs/entrypoints.py, this allows more options for integration and also
    simplifies it somewhat since the library top level can now be imported from
    the library (otherwise hooking against the executable or copying the code
    into a project was the only way).

11. The plugin framework no longer has a complicated path such as
    plugins/apps/gromacs.py, now two directories "apps" and "schedulers" sit at
    the same level as corelibs in the library. This removed most of the
    complexity in the import system, now it is a very simple and elegant way to
    provide plugins for these two categories.

12. Fixed the problem of returning information upon job submission error, this
    was a typo in each of the scheduler plugins.

13. Fix for strange job status glitch when jobid appeard in say a timestamp or
    some other parameter in the output of qstat etc, this has been fixed across
    all schedulers.

14. Fixed spacing problem in some generated job submit files.

15. Modification into the way command-lines are parsed, this is so that the
    detection of executables and their commands as well as Longbow commands is
    much more robust and can now handle arbitrary executables.

16. Addition of --nochecks command-line flag, this will disable testing whether
    the application is available on the remote host. In some circumstances it
    is very difficult to get Longbow to recognise an application is installed.
    This is aimed at advanced users only.

17. All parameters in the main entry point that were previous passed into
    longbow have now all been assimilated into one dictionary "parameters" this
    then allowed refactoring all the switch cases for command-line parameters
    into a much neater single method.

18. Fix for problem detected during unit test writing for configurations.py
    saveconfigs() where if used incorrectly would blow up.

19. Fixed problem in applications.py causing failed run under python 3.2.

20. Fix for filenaming glitch when using global files in replicates.

21. Fixed problem where if required files were not found this was ignored but
    should have been flagged up.

22. Fixed a number of bad initialisers that would cause filenames to go
    missing.

23. legacy code in status method in all schedulers removed.

24. Fixed freezing glitch when all jobs failed to submit.

25. Fixed bad parameter in substitutions.

 
Version 1.3.2
-------------

1. Fix for new gromacs packaging where the gmx mdrun CLI would not be
   recognised.

2. Fix for case in gromacs where if input file -s and -deffnm would be provided
   together and a file was a global file in a replicate job that all files
   would be set to output global.

3. Can now use -deffnm with gromacs on replicate jobs with global files without
   having to also set -s.

4. Fix for missing space in sge replicate script generator.

5. Added the ability for emails to be sent to the user, these are invoked by
   providing the email address in a submit file by
   'email-address = blah@blah.com' and also to set the email flags, these flags
   should be the same ones and same format you use in your submit script for
   example 'email-flags = -M' or 'email-flags = ib'.

6. New common executable naming schemes added for things like cuda.

7. Fixed some missing newline characters from the job submit script generator.

8. Recovery system broken by renaming the method to same as a variable, this
   has now been resolved.

9. Rewrites to the applications.py module, it was too unwield to add to. This
   has now been split down to allow future expansion in a much easier fashion.

 
Version 1.3.1 
-------------

1. For machines running SGE a new parameter to control the flag used on the -pe
   directive has been implemented. This parameter is "sge-peflag" and has a
   default value of "mpi", if your cluster requires something different then
   use this parameter in a configuration file to set it.

2. Some cases on SGE clusters, it can be set that even if a job needs only 1
   core that the -pe mpi #cores must be set. A new flag called "sge-peoverride"
   will make this happen, just provide "sge-peoverride = true" in a
   configuration file to enable.

3. Fixed a problem where Longbow would exit when no jobs are running, this was
   fixed in PBS but not in other schedulers. It is now fixed in all supported
   schedulers.

4. The import statements that looked pretty nasty across the library have been
   changed for nicer more pythonic ones.

5. Some refactoring to get rid of pylint warnings about not using lazy logging.

6. Ability to add script calls into the job submission script that is created
   by Longbow. The parameter "scripts" should be used, for multiple script
   references then a comma separated list should be provided. Just add
   something like this to your configuration file "scripts = source /some/file"
   or "scripts = source /first/file, source /second/file".

7. Fix a problem when using job configuration files and not referencing a
   resource, what should have happened is that Longbow should choose the
   default (top one in hosts.conf). But it crashed with a KeyError exception,
   this is now fixed.
 

Version 1.3.0
-------------

1. Fix for recovery file bug where the file name was mangled by misplaced comma
   in os.path.join().

2. Fix for bug where the recovery file was not being recognised from the
   command-line.

3. Hydra MPI support was added to the LSF plugin, to get this to work a user
   needs to supply mpiexec.hydra as the handler parameter in hosts.conf.

4. Some bad file keywords have been removed from the NAMD plugin, more files
   have been added to the list and some corrections to bad case in list.

5. Fix for required parameters for staging not being written into the recovery
   file.

6. GROMACS files added to NAMD plugin.

7. A disconnect feature has been implemented, users supplying --disconnect on
   the command-line will have Longbow disconnect after submitting jobs, these
   can be reconnected by using the recovery file.

8. Small change to the executable, all code moved from the if
   __name__ == "__main__": to main() and all code previously in main() moved
   to longbowmain() so unit tests can be made for this part of the application.


Version 1.2.1
-------------

1. Fix for annoying error in pip when not using http on urls.

2. Modified recovery mode to use recovery files that are signed by a time stamp
   rather than using a single file, this preserves the ability to have multiple
   Longbow instances.


Version 1.2.0
-------------

1. Simplification of the whole Longbow library. This means lots of changes have
   been made to the source code and thus developers making use of Longbow in
   their code might be affected, those that simply wrap the executable will be
   largely unaffected by this, but may be affected by the below changes. The
   main change as part of the API re-write is that the hosts and jobs
   structures have simply been merged into a single structure called jobs, the
   library is now much more simple to use since all parameters are passed
   around in this single structure, so no more checking which data structure a
   parameter belongs to.

2. Extend informative error messages to all schedulers. This is issue is all
   about trying to get information from the scheduler as to why a job
   submission has failed.

   Error messages from PBS/Torque now passed to the Longbow logging system.
   Error messages from LSF now passed to the Longbow logging system.
   Error messages from SGE now passed to the Longbow logging system.
   Error messages from slurm now passed to the Longbow logging system.
   Error messages from SoGE now passed to the Longbow logging system.
   Fixed vague error that occurs during staging if bad path is used.

3. Longbow can now detect queue size limits dynamically. Machines such as
   ARCHER that only allow a certain number of jobs in the queued state at any
   one time would mean users have to use multiple Longbow sessions to do larger
   numbers of jobs. This improvement now means that a single Longbow instance
   can now submit a number of jobs larger than this limit and Longbow will hold
   back any that cannot get onto the queue in the first submit instance, as
   jobs complete, further jobs will be submitted.

4. A new recovery mode has been introduced that can recover a Longbow session
   if for some reason it gets disconnected. See documentation for more details
   on this.
5. Removal of the logging module and explicit error handling configuration
   within the top level of the library, this issue has ramifications mainly for
   developers using Longbow within their applications, users of Longbow won't
   be affected much.

   The console output messages have been aligned to 80 character widths for
   portability (users might notice this).
   Removal of the internal logging module from within Longbow (affects
   developers).

   Logging for Longbow is now configured and instantiated at the entry point
   of the application (affects developers).
   For developers using Longbow as a library now have the ability to specify
   how logging happens themselves each Longbow module logs to its own log,
   these can then be controlled by the developer allowing for deeper
   integration (affects developers).

   The top level longbow method main() has had all unnecessary code and
   parameters stripped out, this has all been moved to the application entry
   point. This now provides developers with a very high level integration point
   for simple integrations (affects developers).

6. Bad comment on the configuration method fixed (developers only).

7. API comments have been updated to be more accurate with latest changes.

8. Fix for unicode/byte string problem between Python2.x and Python3.x which
   would garble outputs from subprocess.

9. Rename the scheduler plugin "sge_arc2" to "soge" (Son of Grid Engine).

10. All Longbow command-line arguments now support both GNU standard and non
    standard forms for convenience (eg. --version and -version would be valid),
    although future versions might phase out the non-standard -param in favour
    of --param but keeping the single letter -h, -V etc as these are part of
    the standard.


Version 1.1.6
-------------

1. Fix for issue on install through pip where it was complaining about the
   missing README.rst.

2. A manifest file was added to make sure that the setuptools picks up the
   extra files.


Version 1.1.5
-------------

1. Longbow would not install under python 3 using either pip or by running the
   setup script manually. This has now been fixed by using print statements of
   the format print("text"), this form will work in all versions of python.

2. Fix for user reported annoyance of installing the hosts.conf in secret, and
   also leaving the archive that is downloaded in $home. This has now been
   replaced with a warning during install, and also the file is created locally
   and not downloaded.

3. Removed padding from version numbers so v1.01.005 > v1.1.5.

4. Changed the README.md from markdown format to reStructured text, so now the
   README is README.rst, this is to make Longbow more pip friendly whilst still
   being bitbucket and possibly github (in case in future we move).

5. setup.py modified to eliminate the python 3 issues, and also the long
   description is now the README.rst, this means that users will see something
   standard between the pip page and the bitbucket page, this will also tie in
   with new pages on the HECBioSim website which will push pip as the preferred
   way to install more prominently.

6. hosts.conf file has been removed from the development version since this is
   now created on install for new users using pip, this will be marked as
   deprecated on the website for a while so users on old versions can still get
   it. Documentation will need to be updated to reflect this change and provide
   the quickstart example that users can grab a copy of if they are doing a more
   manual install. However pip will be the encouraged way to install.

7. Parameters specified within the configuration files had to be specified in a
   very strict format (param = value), users that omitted the spaces would find
   that Longbow would crash. The code has now been fixed to use regular
   expression to read in and parse for the equals sign, this can now handle
   cases where users specify cases such as:

           param1 = value1
           param2 =value2
           param3= value3
           param4=value4

8. Added python version to logging.

9. Added longbow version to logging.

10. Moved version to the top of the longbow file.

11. Added the paper citation to the logging and readme.
 

Version 1.1.4
-------------

1. The saveconfigs method would overwrite entries within the hosts config with
   potentially blank entries if it was triggered and parameters existed in such
   a state (perhaps via overrides).

2. There was a missing clause on one of the if statements that prevented
   parameters at the hosts level from overriding internal defaults. This
   has now been added in.
 

Version 1.1.3
-------------

1. Update to the supported command line arguments to support non and GNU
   standard options for help and version number.

2. Update to allow the creation of repX directories when they are missing
   (Stops gromacs etc from exiting with path not found error).

3. Fix for bugs in python 3, there were two issues, one a python name change
   and the second was due to garbled output coming from the linux shell
   environment.
 

Version 1.1.1
-------------

1. Modifications to how Longbow accepts the help and version command line
   parameters, some people don't follow GNU standards and thus so that we can
   show them the help message/version we have allowed -v, -version, --version,
   -h, -help and --help.

2. Longbow now creates missing repX directories if they are missing in cases
   where all input files are global. This would allow jobs that might use
   different random seeds on the same input files to be efficient on transfers.


Version 1.1.0
-------------

1. Fix for overwritten rsync-includes (developers only).

2. Bad character length on PBS now has an error message to inform the user what
   went wrong. Job names longer than 15 chars would be rejected.

3. Jobs that failed in a multi job would bring down the whole lot due to a bad
   initialisation now fixed.

4. Command line Longbow is submitted with is now logged to the log file for
   debugging purposes.

5. Bug fix with a bad initialisation in job processing code.

6. New ini parsers that don't rely on python std lib parser, this means
   comments are no longer deleted.

7. The following methods; loadhosts(), loadjobs(), sortjobsconfigs(),
   sorthostsconfigs(), amendjobsconfigs() have been replaced with single method
   processconfigs().

8. Fix for critical failure when the remoteworkdir did not exist.
