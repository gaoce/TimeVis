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
| POST   | Upload a new experiment information        |
+--------+--------------------------------------------+
| PUT    | Update existing experiment(s) information  |
+--------+--------------------------------------------+
| DELETE | Delete Experiment(s). **Not implemented**. |
+--------+--------------------------------------------+

1. GET
^^^^^^

* **Parameters**: None.
* **Input**: None.
* **Output**: A json object mapping experiment IDs to experiment descriptions,
  for expample:

::

  {
    "exp_id1": {
      "name"    : "exp1",
      "users"   : ["user1", "user2"],
      "well"    : 384,
      "channels": ["GFP", "OD"],
      "factors" : [{"name": "Dose", "type": "decimal"}]
    },
    "exp_id2": {
      "name"    : "exp2",
      "users"   : ["user3"],
      "well"    : 96,
      "channels": ["GFP"],
      "factors" : [
      	{"name": "Dose", "type": "decimal"},
      	{"name": "Gene", "type": "category"},
      ]
    },
    ...
  }

2. Post
^^^^^^^

* **Parameters**: None.
* **Input**: A json object with the same format as described in ``GET``. Only
  one experiment is allowed to be uploaded per request. **Note ``exp_id`` for a
  new experiment should be character zero, ie. '0'**
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

* **Parameters**: ``?exp=exp_id``, mandatory.
* **Input**: None.
* **Output**: A json object that specifies experiment id and maps layout IDs to
  layout descriptions, for expample:

::

  {
    "exp_id"     : "exp_id1",
    {
      "layout_id1": {
        "name"   : "layout1",
        "factors": [
          {"name": "Dose", "levels": [4.2, 4.2, 42, 42, ...]},
          {"name": "Gene", "levels": ['aa', 'aa', 'bb', ...]}
        ]
      },
      "layout_id2": {
        "name"   : "layout2",
        "factors": [
          {"name": "Dose", "levels": [0.42, 0.42, 0.042, ...]},
          {"name": "Gene", "levels": ['aa', 'aa', 'bb',  ...]}
        ]
      },
      ...
    }
  }

2. Post
^^^^^^^

* **Parameters**: ``?exp=exp_id``, mandatory.
* **Input**: A json object with the same format as described in ``GET``. Only
  one layout is allowed to be uploaded per request. **Note ``layout_id`` for a
  new layout should be character zero, ie. '0'**
* **Output**: None.

3. PUT
^^^^^^

* **Parameters**: ``?exp=exp_id``, mandatory.
* **Input**: A json object with the same format as described in ``GET``.
* **Output**: None.

4. DELETE
^^^^^^^^^
**Not implemented**. It is not a safe practice to delete layout either, so this
verb is not implemented.

3. Plate
========

A summary of all HTTP verbs used for this endpoint:

+--------+--------------------------------------------------------------------+
| Verb   | Function                                                           |
+========+====================================================================+
| GET    | Retrieve plate information for a particular layout within a        |
|        | certain experiments. The returned data can be for single or        |
|        | multiple plates                                                    |
+--------+--------------------------------------------------------------------+
| POST   | Upload plate data for a layout of an experiment                    |
+--------+--------------------------------------------------------------------+
| PUT    | Update existing plate(s) information                               |
+--------+--------------------------------------------------------------------+
| DELETE | Delete Experiment(s). **Not implemented**.                         |
+--------+--------------------------------------------------------------------+

1. GET
^^^^^^

* **Parameters**: ``?exp=exp_id&layout=layou_id``, mandatory.
* **Input**: None.
* **Output**: A json object mapping experiment IDs to experiment descriptions,
  for expample:

::

  {
    "exp_id"     : "exp_id1",
    "layout_id1" : "layout_id1",
    {
      "plate1": {
        "name"   : "plate1",
        "channels": [
          {"GFP": [4.2, 4.2, 42, 42, ...]},
        ]
      },
      "plate_id2": {
        "name"   : "plate2",
        "channels": [
          {"GFP": [4.2, 4.2, 42, 42, ...]},
        ]
      },
      ...
    }
  }



2. Post
^^^^^^^

* **Parameters**: ``?exp=exp_id&layout=layou_id``, mandatory.
* **Input**: A json object with the same format as described in ``GET``. Only
  one plate is allowed to be uploaded per request. **Note ``plate_id`` for a
  new layout should be character zero, ie. '0'**
* **Output**: None.

3. PUT
^^^^^^

* **Parameters**: ``?exp=exp_id&layout=layou_id``, mandatory.
* **Input**: A json object with the same format as described in ``GET``.
* **Output**: None.

4. DELETE
^^^^^^^^^
**Not implemented**.
