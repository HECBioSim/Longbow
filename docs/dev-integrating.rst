Integrating Longbow
*******************

Perhaps one of the most useful features of Longbow is the ease in which it can be utilised in other software. Longbow has been successfully applied in a range of other software products that require jobs to be offloaded onto high performance computing systems. 

There are a number of ways in which Longbow can be integrated into other software, and which method should be used is largely dependant on how Longbow is going to be utilised. The following sections will introduce some of the most popular ways to integrate Longbow into other software and some of the use cases that each method should apply to.

Wrapping the Application
========================

The quickest and most stable way to integrate Longbow into another application is to wrap the executable itself. This is the most stable way to integrate Longbow when considered from a code change perspective, since it is unlikely that the way the executable is called will change, even if the API changes considerably.

This method is extremely useful for use in scripts, where the user might wish to make use of the power of Longbow to launch jobs after some automated setup. This does not mean that this is unsuitable for integration within applications, however, there are a number of considerations that should be made before choosing this method:

1. Configuration - you will need to provide a configuration file with at least the details of the HPC machines and some job defaults. This is useful in cases where a very loose level of integration is required, for example if these settings are not collected as part of the application that is being integrated with Longbow. If these parameters are intended to be collected (say in a GUI) then you would have to write out configuration files to pass any parameters you wish to change that are not available for configuration via the Longbow command-line.

2. Exceptions - exceptions will be difficult to deal with in this way of integrating, what will happen is that Longbow will handle its exceptions internally and the executable will exit should an error occur that Longbow can't handle by itself, this means that exceptions won't percolate up from Longbow and into your application. This will create an extra layer of complications when trying to deal with errors.

3. Logging - when linking the executable you will end up creating a log file by default either in the user home directory or inside the directory that Longbow is launched from. The only way you can capture the logging output is to turn on the logging to stdout and capture this output, on which you will likely need to some form of processing on to get this into a form you want. This means that you have very little control over the logging that comes out of Longbow.

The best way to start learning to use Longbow for an integration is to start using it, the following examples will show how to call the Longbow application in scripts. Before you can do these examples, you should complete the following prerequisites:

* Longbow should be installed as an application on the machine that the script/application subject to the integration is installed upon.

* Longbow should be configured with at least 1 HPC resource, it should be verified that you can run at least one of the examples.
 
**A Simple Python Script**

This example will highlight the simplest example of calling and capturing the output of Longbow in a python script::

    #!/usr/bin/env python

    import subprocess

    # Format a call to python subprocess. Here we are using a non-shell call so
    # the executable is in the format of a list, the first entry in the list should
    # be the longbow executable and the second entry the arguments to Longbow. We
    # are also piping stdout so we can capture the output.
    inst = subprocess.Popen(["longbow", "--help"], stdout=subprocess.PIPE)

    # Loop until the pipe is closed
    while inst.poll() is None:

        # Extract each line.
        line = inst.stdout.readline()

        # Output to the console, strip added newline chars.
        print line.rstrip() 

Integration by API
==================

The most flexible way to include Longbow into other software, is to integrate at an API level, this means that developers of other software can use Longbow in a seemless way without having to make external calls to the executable. There are many benefits to doing this, such as being able to create internal data structures directly, without having to firstly create Longbow configuration files, you can get access to the logging information and show this to users in a way you define and can interact with the Longbow exceptions.

Over the next few months, this part of the documentation will be developed further. To get you started though, the easiest way to get going with integrating Longbow into your software, is to copy what the longbow() method is doing, for some developers simply calling this method using the "parameters" dictionary to override internal configuration will be all that is needed. But for others, a more fine grain approach will be neccessary. We will be adding examples of this to this section over the coming months.

