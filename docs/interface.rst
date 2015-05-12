*********************
Interface Development
*********************

The user interface of ``timevis`` is web based. The whole application is a
single webpage. Thanks to HTML template engine `Jinja2
<http://jinja.pocoo.org/>`_, we are able to separate different functionalities
into individual modular pages, see ``timevis/template`` folder.

1. Knockout View Models
=======================

1. ExpVM
^^^^^^^^
A view model for experiment information. Available attributes of an ``ExpVM``
object are:

:fun: observable. Functionality currently used.
:experiments: observableArray. A list of ``Exp`` objects.
  
2. Exp
^^^^^^
A object to repsent experiment information, used by both frontend and API (see
API). Available fields are:

:id: Integer. Experiment ID.
:name: String. Experiment name.
:user: String. Experiment user names.
:well: Integer. Number of well on the plate.
:channels: Array of channel objects.

    :id: Integer. Channel ID.
    :name: String. Channel name.

:factors: Array of factor objects.

    :id: Integer. Factor ID.
    :name: String. Factor name.
    :type: String. Factor type.
