*****************
API Documentation
*****************
.. This is version 2 of API. Version 1 is hidden somewhere in the history.

1. Endpoints summary
====================

+------------------------+---------------------------------+
| URI                    | Target                          |
+========================+=================================+
| ``/api/v2/experiment`` | Experiment information          |
+------------------------+---------------------------------+
| ``/api/v2/layout``     | Layout information              |
+------------------------+---------------------------------+
| ``/api/v2/plate``      | Plate information and data      |
+------------------------+---------------------------------+
| ``/api/v2/timeseries`` | (Transformed) time series data  |
+------------------------+---------------------------------+

2. Experiment information
=========================

1. Summary
^^^^^^^^^^

Retrieve, upload and update information at experiment level, including
experiment name, user names, well number of plates, channels (dependent
variables) measured, factors (independent variables) set. 

The URI is ``/api/v2/experiment``. A summary of all HTTP verbs used for this 
endpoint is shown below:

+--------+--------------------------------------------+
| Verb   | Function                                   |
+========+============================================+
| GET    | Retrieve information for all experiments   |
+--------+--------------------------------------------+
| POST   | Upload a new experiment information        |
+--------+--------------------------------------------+
| PUT    | Update existing experiment(s) information  |
+--------+--------------------------------------------+

..
  | DELETE | Delete Experiment(s). **Not implemented**. |
  ``DELETE`` method is not implemented as it is not safe right now.

2. GET
^^^^^^

**Parameters**
    None.
**Input**
    None.
**Output**
    A json object mapping experiment IDs to experiment descriptions in the
    following format.

    ::

      {
        exp_id: 
        {
          "name"    : exp_name,
          "user"    : exp_user,
          "well"    : exp_well,
          "channels": 
          [
            {"id": channel_id, "name": channel_name}, 
            ...
          ],
          "factors" : 
          [
            {"id": factor_id, "name": factor_name, "type": factor_type}, 
            ...
          ]
        },
        ...
      }

    ..
      The ``channels`` and ``factors`` are designed to be array instead of
      objects mapping id to description is because all new factors and channels
      will have the same "0".


    The unquoted variables are:

    * ``exp_id``:       Integer. Experiment ID.
    * ``exp_name``:     String.  Experiment name.
    * ``exp_user``:     String.  Comma separated user names.
    * ``exp_well``:     Integer. Well number.
    * ``channel_id``:   Integer. Channel ID.
    * ``channel_name``: String.  Channel name.
    * ``factor_id``:    Integer. Factor id.
    * ``factor_name``:  String.  Factor name.
    * ``factor_type``:  String.  Factor type, can be either "Category", 
      "Integer", or "Decimal"

    Here is an expample:

    ::

      {
        "1": 
        {
          "name"    : "exp1",
          "user"    : "user1, user2",
          "well"    : 384,
          "channels": [{"id": "1", "name": "GFP"}, {"id"": "2", "name": "OD"}],
          "factors" : [{"id": "1", "name": "Dose", "type": "Decimal"}]
        },
        "2": 
        {
          "name"    : "exp2",
          "user"    : "user3",
          "well"    : 96,
          "channels": [{"id": "3", "name": "GFP"}],
          "factors" : 
          [
            {"id": "2", "name": "Dose", "type": "Decimal"},
            {"id": "3", "name": "Gene", "type": "Category"}
          ]
        }
      }

3. POST
^^^^^^^

**Parameters**
    None.
**Input**
    A json object with the same format as described in ``GET``. Only one
    experiment is allowed to be uploaded per request.  **Note**: ``exp_id`` and 
    factor ``id`` for a new experiment should be zero, ie. "0" or 0.

    Here is an example:

    ::

      {
        "0": {
          "name"    : "Exp1",
          "user"    : "user1, user2",
          "well"    : 384,
          "channels": [{"id": "0", "name": "GFP"}, {"id"": "0", "name": "OD"}],
          "factors" : [
            {"id": 0, "name": "Dose", "type": "Decimal"},
            {"id": 0, "name": "Gene", "type": "Category"}
          ]
        }
      }

**Output**
    None.

4. PUT
^^^^^^

**Parameters**
    None.
**Input**
    A json object with the same format as described in ``GET``. Only one
    experiment is allowed to updated at a time.

    Here is an example:

    ::

      {
        "1": {
          "name"    : "Exp 1",
          "user"    : "user1",
          "well"    : 96,
          "channels": [{"id": "1", "name": "GFP"}],
          "factors" : [
            {"id": "1", "name": "Dose", "type": "Decimal"},
            {"id": "2", "name": "Gene", "type": "Category"}
          ]
        }
      }

**Output**
    None.

3. Layout information
=====================

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

..
  | DELETE | Delete layout(s). **Not implemented**.                |

1. GET
^^^^^^

**Parameters**
    ``?eid=exp_id``, mandatory, experiment id.
**Input**
    None.
**Output**
    A json object that specifies experiment id and maps layout IDs to layout
    descriptions, for expample:

    ::

      {
        layout_id: {
          "name": name,
          "factors": [
            {
              "id": id, "name": name, "type": type", "levels":{well: level, ...}
            },
            ...
          ]
        },
        ...
      }

    Unquoted variables are:

    * ``layout_id``: Integer. Layout ID.
    * ``name``:      String.  Layout name.
    * ``id``:        Integer. Factor id.
    * ``name``:      String.  Factor name
    * ``type``:      String.  Factor type, "Category", "Integer", or "Decimal"
    * ``well``:      String.  Well name, e.g., "A01", "C04"
    * ``level``: 	 String.  Factor level.

    Here is an expample:

    ::

      {
        "1": {
          "name": "Layout 1",
          "factors": [
            {
              "id"    : 1, 
              "name"  : "Dose", 
              "type"  : "Decimal", 
              "levels": {'A01':'42', 'A02':'42', ...}
            },
            {
              "id"    : 2, 
              "name"  : "Gene", 
              "type"  : "Category", 
              "levels": {'A01':'aa', 'A02':'aa', ...}
            }
          ]
        },
        "2": {
          "name": "Layout 2",
          "factors": [
            {"id": 1, "name": "Dose", "type": "Decimal", 
             "levels": {'A01':'42', 'A02':'42', ...}},
            {"id": 2, "name": "Gene", "type": "Category",
             "levels": {'A01':'bb', 'A02':'bb', ...}}
          ]
        }
      }

      # The factor levels are not shown in full here.

2. POST
^^^^^^^

**Parameters**
    ``?eid=exp_id``, mandatory, experiment id.
**Input**
    A json object with the same format as described in ``GET``. Only one layout
    is allowed to be uploaded per request. **Note** ``layout_id`` for a new
    layout should be character zero, ie. "0".

    Here is a json file example:

    ::

      {
        "0": {
          "name": "Layout 1",
          "factors":
          {
            "1":
            {
              "name": "Dose",
              "levels":
              {
                "A01":"42", "A02":"42", "A03":"42", "A04":"42", ...
              }
            },
            "2":
            {
              "name": "Gene",
              "levels":
              {
                "A01":"aa", "A02":"aa", "A03":"aa", "A04":"aa", ...
              }
            }
          }
        }
      }

      # The factor levels are not shown in full here.

**Output**
    None.

3. PUT
^^^^^^

**Parameters**
    None.
**Input**
    A json object with the same format as described in ``GET``. Only one layout
    is allowed to be updated at a time.

    Here is a json file example:

    ::

      {
        "0": {
          "name": "Layout 1",
          "factors":
          {
            "1":
            {
              "name": "Dose",
              "levels":
              {
                "A01":"42", "A02":"42", "A03":"42", "A04":"42", ...
              }
            },
            "2":
            {
              "name": "Gene",
              "levels":
              {
                "A01":"bb", "A02":"bb", "A03":"bb", "A04":"bb", ...
              }
            }
          }
        }
      }

      # The factor levels are not shown in full here.

**Output**
    None.

3. Plate information
====================

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

**Parameters**
    ``?exp=exp_id&layout=layou_id``, mandatory.
**Input**
    None.
**Output**
    A json object mapping experiment IDs to experiment descriptions, for
    expample:

    ::
    
      {
        "exp_id": exp_id,
        "layout_id": layout_id,
        "plates": 
        {
          plate_id: 
          {
            channel_id: 
            {
              "name": channel_name, 
              "time": time,
              "values": {well: value, ...} 
            },
            ...
          },
          ...
        }
      }

    * ``exp_id``: integer, experiment id
    * ``layout_id``: integer, layout id
    * ``plate_id``: integer, plate id
    * ``channel_id``: integer, channel id
    * ``channel_name``: string, channel name
    * ``well``: string, well name, e.g., "A01", "C04"
    * ``value``: array of  decimals, measurements for the channel 
    * ``time``: array of strings, measurement time point, should have the same
      dimension as the value arrays

    Here is an expample:


2. POST
^^^^^^^

**Parameters**
    ``?exp=exp_id&layout=layou_id``, mandatory.
**Input**
    A json object with the same format as described in ``GET``. Only one plate
    is allowed to be uploaded per request. **Note** ``plate_id`` for a new
    layout should be character zero, ie. "0".
**Output**
    None.

3. PUT
^^^^^^

**Parameters**
    ``?exp=exp_id&layout=layou_id``, mandatory.
**Input**
    A json object with the same format as described in ``GET``.
**Output**
    None.

5. Time Series
==============

A summary of all HTTP verbs used for this endpoint:

+--------+--------------------------------------------+
| Verb   | Function                                   |
+========+============================================+
| GET    | Retrieve information for all experiments   |
+--------+--------------------------------------------+

1. GET
^^^^^^

**Parameters**
    None
**Input**
    A json object describing query criteria. Mandatory.

::

  {
    "exp_id"   : "exp_id1",
    "channel"  : "GFP",
    "factors"  : {
      "factor1":  [4.2, 4.2, 42, 42, ...],
      "factor2":  [4.2, 4.2, 42, 42, ...],
      ...
    }
  }

**Output**
  A json object containing time series data, for expample:

::

  {
    "query_id"   : "query_id1",
    "query" : {},
    "Result" :
    [{
       "value": -1.1618426259,
       "time": "00:00:00",
       "l": -2.6017329022,
       "u": 0.2949717757
      },{
       "value": -1.1618426259,
       "time": "00:00:05",
       "l": -2.6017329022,
       "u": 0.2949717757
      },
      ...
    ]
  }
