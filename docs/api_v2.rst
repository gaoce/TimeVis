*****************
API Documentation
*****************
.. This is version 2 of API. Version 1 is hidden somewhere in the history.

1. Endpoints summary
====================

+------------------------+-------------------------+
| URI                    | Target                  |
+========================+=========================+
| ``/api/v2/experiment`` | Experiment information  |
+------------------------+-------------------------+
| ``/api/v2/layout``     | Layout information      |
+------------------------+-------------------------+
| ``/api/v2/plate``      | Plate data              |
+------------------------+-------------------------+
| ``/api/v2/timeseries`` | Time series data        |
+------------------------+-------------------------+

2. Experiment
=============

A summary of all HTTP verbs used for this endpoint:

+--------+--------------------------------------------+
| Verb   | Function                                   |
+========+============================================+
| GET    | Retrieve information for all experiments   |
+--------+--------------------------------------------+
| POST   | Upload new experiment(s) information       |
+--------+--------------------------------------------+
| PUT    | Update existing experiment(s) information  |
+--------+--------------------------------------------+
| DELETE | Delete Experiment(s). **Not implemented**. |
+--------+--------------------------------------------+

1. GET
^^^^^^

* **Parameters**: None.
* **Input**: None.
* **Output**: A json object mapping experiment IDs to experiment descriptions, for
  expample:

::

  {
    "exp_id1": {
      "name": "exp1",
      "users": ["user1", "user2"],
      "well": 384,
      "chanels": ["GFP", "OD"],
      "factors": [{"name": "Dose", "type": "decimal"}]
    },
    "exp_id2": {
      "name": "exp2",
      "users": ["user3"],
      "well": 96,
      "chanels": ["GFP"],
      "factors": [
      	{"name": "Dose", "type": "decimal"},
      	{"name": "Gene", "type": "category"},
      ]
    },
    ...
  }

2. Post
^^^^^^^

* **Parameters**: None.
* **Input**: A json object with the same format as described in ``GET``.
* **Output**: None.

3. PUT
^^^^^^

* **Parameters**: None.
* **Input**: A json object with the same format as described in ``GET``.
* **Output**: None.

4. DELETE
^^^^^^^^^

**Not implemented**. It is not a safe practice to delete an experiment so this
verb is not implemented.

3. Layout
=========

A summary of all HTTP verbs used for this endpoint:

+--------+-------------------------------------------------------+
| Verb   | Function                                              |
+========+=======================================================+
| GET    | Retrieve layout information for a specific experiment |
+--------+-------------------------------------------------------+
| POST   | Upload a new layout for a specific experiment         |
+--------+-------------------------------------------------------+
| PUT    | Update existing layout(s) information                 |
+--------+-------------------------------------------------------+
| DELETE | Delete layout(s). **Not implemented**.                |
+--------+-------------------------------------------------------+

1. GET
^^^^^^

* **Parameters**: exp=exp_id.
* **Input**: None.
* **Output**: A json object mapping experiment IDs to experiment descriptions, for
  expample:

::

  {
    "layout_id1": {
      "name": "exp1",
      "users": ["user1", "user2"],
      "well": 384,
      "chanels": ["GFP", "OD"],
      "factors": [{"name": "Dose", "type": "decimal"}]
    },
    "exp_id2": {
      "name": "exp2",
      "users": ["user3"],
      "well": 96,
      "chanels": ["GFP"],
      "factors": [
      	{"name": "Dose", "type": "decimal"},
      	{"name": "Gene", "type": "category"},
      ]
    },
    ...
  }
