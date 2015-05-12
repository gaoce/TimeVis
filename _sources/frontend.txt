***********************
Front End Documentation
***********************

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
