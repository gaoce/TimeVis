***********
Development
***********
This page describes the commands used during development.

1. Documentation
================

1.1 Documentation and sphinx
----------------------------

All the documents are in docs/ folder under the root directory. The
documentation of this project is using `Sphinx <http://sphinx-doc.org/>`_. 

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

To deploy the generated documentation to github pages, issue the following 
commands in the root directory. The documentation can be now visited from
`<username>.github.io/<project_name>`.

::

  # Switch to gh-pages branch
  $ git checkout gh-pages

  # Deploy
  $ make github

