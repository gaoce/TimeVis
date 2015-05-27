***********
Development
***********
The development of this project is facilitated by several open source tools.
This page describes the commands used for different automation jobs during
development.

1. Documentation
================
Documentation writing and revision happens at `gh-pages` branch. To merge the
updated docs back the `master` branch, issue `make update-doc` there.

1.1 Documentation and sphinx
----------------------------

All the documents are in docs/ folder under the root directory. The
documentation of this project is in `rst` format and will be transformed into
other formats like HTML using `Sphinx <http://sphinx-doc.org/>`_.

To convert the .rst file into visually appealling HTML files, issue the
following commands.

::

  $ cd docs
  $ make html

To see the html files on browser, issue the following commands, then the
generated web pages can be access at http://localhost:8000

::

  $ cd docs
  $ make test

1.2 Github pages
----------------

To deploy the generated documentation to github pages, issue the following
command in the root directory. The documentation can be now visited from
`<username>.github.io/<project_name>`.

::

  $ make github

2. Development Automation
=========================

Use the following make commands under the root directory for various automation
jobs.

2.1 Installation
----------------

To install a local copy, use

::

    $ make install

2.2 Test run
------------

To start a test run, including installing a local copy of the package and start
the server at http://localhost:8000, use

::

	$ make devserver

2.3 Clean
---------

To clean unnecessary files, use

::
	
    $ make clean
