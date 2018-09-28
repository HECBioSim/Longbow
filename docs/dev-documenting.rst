Documenting
***********

Developers wishing to add to/modify existing features of Longbow are responsible for documenting them. As is similar with missing unit tests, pull requests that arrive with an absence of documentation for the addition/modification will be rejected upon review. The Longbow project should have good documentation both at a source code level and in the written documentation that goes out to users. The Longbow project is using Sphinx to compile its documentation, you will need to get some tools installed and try out building the documentation yourself locally before adding to them. The following process will show you how to achieve this:

**1. Install the required packages**

Before you can start documenting, you'll need some packages. So install these if you haven't already::

    pip install --user sphinx sphinx-autobuild sphinx_rtd_theme


**2. Try and make the documentation**

The next step is to see if you can build the documentation html from the source. So change into the "docs" directory inside the Longbow source directory and run::

    make html

If everything has gone to plan then you should be able to now view the documentation in your web browser by navigating to the index.html file inside the "_build/html" directory.

Adding to the documentation is easy, each page in the documentation has a .rst file associated with it. So to add documentation to an existing page then simply modify the relevant .rst file, if you are unsure which .rst file belongs to which page, then you can find out by looking at the index.rst table of contents and the titles at the top of each .rst file.

The documentation simply uses reStructuredText format, not all features that are available in the reStructuredText will be available through Sphinx so it is best to use the Sphinx documentation for the reST format than the actual reST format documentation. This can be found at http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html

happy documenting!
