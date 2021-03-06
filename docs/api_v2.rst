*****************
API Documentation
*****************
.. This is version 2 of API. Version 1 is hidden somewhere in the history.

1. Summary
==========

The endpoints are summarized in the following table:

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

The data exchanged, except ``timeseries`` are generally in the following JSON
format:

::

  {
    endpoint_name: obj_array,
  }

``endpoint_name``
    Name of the endpoint, could be ``experiment``, ``layout``, etc.
``obj_array``
	An array of objects describing experiment, layout, etc, as discussed below.

..
    ``para_name*`` and ``para*``
        key-value pairs describing parameters for the requests

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
    A JSON object containing an array of experiment object describing experiment
    information.

    ::

      {
        "experiment":
        [
          {
            "id"      : exp_id,
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
              {"id": factor_id, "name": factor_name, "type": factor_type,
               "levels": factor_levels},
              ...
            ]
          },
        ...
        ]
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
    * ``factor_levels``:  Array of Strings.  Unique factor levels. This is an
      addon feature, only available for GET method.

    Here is an expample:

    ::

      {
        "experiment":
        [
          {
            "id"      : 1,
            "name"    : "exp1",
            "user"    : "user1, user2",
            "well"    : 384,
            "channels":
            [
              {"id": 1, "name": "GFP"},
              {"id": 2, "name": "OD"}
            ],
            "factors" :
            [
              {"id": 1, "name": "Dose", "type": "Decimal", 
              "levels": ["42", "43"]}
            ]
          },
          {
            "id"      : 2,
            "name"    : "exp2",
            "user"    : "user3",
            "well"    : 96,
            "channels": [{"id": "3", "name": "GFP"}],
            "factors" :
            [
              {"id": 2, "name": "Dose", "type": "Decimal", "levels": ["42"]},
              {"id": 3, "name": "Gene", "type": "Category", "levels": ["bb"]}
            ]
          }
        ]
      }

3. POST
^^^^^^^

**Parameters**
    None.
**Input**
    A JSON object with the same format as described in ``GET``.

    **Note**: ``exp_id`` and ``channel_id`` and ``factor_id`` for a new
    experiment should be zero.

    Here is an example:

    ::

      {
        "experiment":
        [
          {
            "id"      : 0,
            "name"    : "Exp1",
            "user"    : "user1, user2",
            "well"    : 384,
            "channels":
            [
              {"id": 0, "name": "GFP"},
              {"id": 0, "name": "OD"}
            ],
            "factors" :
            [
              {"id": 0, "name": "Dose", "type": "Decimal"},
              {"id": 0, "name": "Gene", "type": "Category"}
            ]
          }
        ]
      }

**Output**
	Newly created experiment object, e.g.,

    ::

      {
        "experiment":
        [
          {
            "id"      : 1,
            "name"    : "Exp1",
            "user"    : "user1, user2",
            "well"    : 384,
            "channels":
            [
              {"id": 0, "name": "GFP"},
              {"id": 0, "name": "OD"}
            ],
            "factors" :
            [
              {"id": 1, "name": "Dose", "type": "Decimal"},
              {"id": 2, "name": "Gene", "type": "Category"}
            ]
          }
        ]
      }


4. PUT
^^^^^^

**Parameters**
    None.
**Input**
    A JSON object with the same format as described in ``GET``. Note update may
    cause loss of factor and channel.

    Here is an example:

    ::

      {
        "experiment":
        [
          {
            "id"      : 1,
            "name"    : "Exp 1",
            "user"    : "user1",
            "well"    : 96,
            "channels": [{"id": 1, "name": "GFP"}],
            "factors" :
            [
              {"id": 1, "name": "Dose", "type": "Decimal"},
              {"id": 2, "name": "Gene", "type": "Category"}
            ]
          }
        ]
      }

    Note: ``id`` for newly created Channel or Factor should be 0

**Output**
	Updated experiment object, with possible altered IDs, e.g.,

    ::

      {
        "experiment":
        [
          {
            "id"      : 1,
            "name"    : "Exp 1",
            "user"    : "user1",
            "well"    : 96,
            "channels": [{"id": 2, "name": "GFP"}],
            "factors" :
            [
              {"id": 3, "name": "Dose", "type": "Decimal"},
              {"id": 4, "name": "Gene", "type": "Category"}
            ]
          }
        ]
      }

3. Layout information
=====================

1. Summary
^^^^^^^^^^

Retrieve, upload and update layout information, including layout name,
especially the levels of factors at each well.

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

2. GET
^^^^^^

**Parameters**
    ``?eid=exp_id``, mandatory, experiment id.
**Input**
    None.
**Output**
    A JSON object that specifies experiment id and maps layout IDs to layout
    descriptions, for expample:

    ::

      {
        "layout":
        [
          {
            "id":   layout_id,
            "name": layout_name,
            "factors":
            [
              {
                "id"    : factor_id,
                "name"  : factor_name,
                "levels": {well: level, ...}
              },
              ...
            ],
          },
          ...
        ]
      }

    The unquoted variables are:

    * ``layout_id``:   Integer. Layout ID.
    * ``layout_name``: String.  Layout name.
    * ``factor_id``:   Integer. Factor id.
    * ``factor_name``: String.  Factor name.
    * ``well``:        String.  Well name, e.g., "A01", "C04"
    * ``level``: 	   String.  Factor level.

    Here is an expample:

    ::

      {
        "layout":
        [
          {
            "id": 1,
            "name": "Layout 1",
            "factors": [
              {
                "id"    : 1,
                "name"  : "Dose",
                "levels": {'A01':'42', 'A02':'42', ...}
              },
              {
                "id"    : 2,
                "name"  : "Gene",
                "levels": {'A01':'aa', 'A02':'aa', ...}
              }
            ]
          },
          {
            "id":   2,
            "name": "Layout 2",
            "factors":
            [
              {
                "id"    : 3,
                "name"  : "Dose",
                "levels": {'A01':'42', 'A02':'42', ...}
              },
              {
                "id"    : 4,
                "name"  : "Gene",
                "levels": {'A01':'bb', 'A02':'bb', ...}}
            ]
          }
        ]
      }

      # The factor levels are not shown in full here.

3. POST
^^^^^^^

**Parameters**
    ``?eid=exp_id``, mandatory, experiment id.
**Input**
    A JSON object with the same format as described in ``GET``.

    **Note** ``layout_id`` for a new layout should be zero.

    Here is an example:

    ::

      {
        "layout":
        [
          {
            "id"        : 0,
            "name"      : "Layout 1",
            "factors"   :
            [
              {
                "id"    : 1,
                "name"  : "Dose",
                "levels": {"A01":"42", "A02":"42", "A03":"42", ...}
              },
              {
                "id"    : "2",
                "name"  : "Gene",
                "levels": {"A01":"aa", "A02":"aa", "A03":"aa", ...}
              }
            ]
          }
        ]
      }

      # The factor levels are not shown in full here.

**Output**
    Newly created factors, eg,


    ::

      {
        "layout":
        [
          {
            "id"        : "1",
            "name"      : "Layout 1",
            "factors"   :
            [
              {
                "id"    : "1",
                "name"  : "Dose",
                "levels": {"A01":"42", "A02":"42", "A03":"42", ...}
              },
              {
                "id"    : "2",
                "name"  : "Gene",
                "levels": {"A01":"aa", "A02":"aa", "A03":"aa", ...}
              }
            ]
          }
        ]
      }

      # The factor levels are not shown in full here.

4. PUT
^^^^^^

**Parameters**
    ``?eid=exp_id``, mandatory, experiment id.
**Input**
    A JSON object with the same format as described in ``GET``. Only one layout
    is allowed to be updated at a time.

    Here is an example:

    ::

      {
        "layout":
        [
          {
            "id"        : "1",
            "name"      : "Layout 1",
            "factors":
            [
              {
                "id"    : "1",
                "name"  : "Dose",
                "levels": {"A01":"42", "A02":"42", "A03":"42", ...}
              },
              {
                "id"    : "2",
                "name"  : "Gene",
                "levels": {"A01":"bb", "A02":"bb", "A03":"bb", ...}
              }
            ]
          }
        ]
      }

      # The factor levels are not shown in full here.

**Output**
    Update layout obj with possible altered IDs.

3. Plate information
====================

1. Summary
^^^^^^^^^^

Retrieve, upload and update plate data, including channels and time series data.

A summary of all HTTP verbs used for this endpoint is as follows:

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

..
  | DELETE | Delete Experiment(s). **Not implemented**.                         |

2. GET
^^^^^^

**Parameters**
    ``?lid=layout_id``, mandatory, Layout ID.
**Input**
    None.
**Output**
    A JSON object mapping experiment IDs to experiment descriptions, for
    expample:

    ::

      {
        "plate":
        [
          {
            "id"        : plate_id,
            "channels"  :
            [
              {
                "id"    : channel_id,
                "name"  : channel_name,
                "time"  : time,
                "well"  : well,
                "value" : [value, ...]
              },
              ...
            ]
          },
          ...
        ]
      }

    Unquoted variables are:

    * ``plate_id``:     Integer. Plate id.
    * ``channel_id``:   Integer. Channel id.
    * ``channel_name``: String.  Channel name.
    * ``time``: 		Array of strings. Measurement time point,
      should have the same dimension as the value arrays
    * ``well``:         String. Well name array, e.g., "A01", "C04"
    * ``value``:        Decimals. Value array. Record channel measurement at all
      wells at a given time point. The well order is the same as ``well``
      field, and the time point order is corresponding to the time order in
      ``time`` field.

    Here is an expample:

    ::

      {
        "plate":
        [
          {
            "id"        : 1,
            "channels"  :
            [
              {
                "id"    : 1,
                "name"  : "GFP",
                "time"  : ["00:00:00", "00:05:00", "00:10:00", "00:15:00"],
                "well"  : ["A01", "A02", "A03", "A04", "A05", "A06", ...],
                "value" : [ [0, 0, 0, ... ], ... ]
              }
            ]
          }
        ]
      }

2. POST
^^^^^^^

**Parameters**
    ``?lid=layout_id``, mandatory, Layout ID.
**Input**
    A JSON object with the same format as described in ``GET``. Only one plate
    is allowed to be uploaded per request. **Note** ``plate_id`` for a new
    layout should be 0, e.g.,

    ::

      {
        "plate":
        [
          {
            "id"        : 0,
            "channels"  :
            [
              {
                "id"    : 1,
                "name"  : "GFP",
                "time"  : ["00:00:00", "00:05:00", "00:10:00", "00:15:00"],
                "well"  : ["A01", "A02", "A03", "A04", "A05", "A06", ...],
                "value" : [ [0, 0, 0, ... ], ... ]
              }
            ]
          }
        ]
      }

**Output**
    Newly created plate object, eg.,

    ::

      {
        "plate":
        [
          {
            "id"        : 1,
            "channels"  :
            [
              {
                "id"    : 1,
                "name"  : "GFP",
                "time"  : ["00:00:00", "00:05:00", "00:10:00", "00:15:00"],
                "well"  : ["A01", "A02", "A03", "A04", "A05", "A06", ...],
                "value" : [ [0, 0, 0, ... ], ... ]
              }
            ]
          }
        ]
      }

3. PUT
^^^^^^

**Parameters**
	None. ``plate_id`` is unique and no ``layout_id`` is necessary.
**Input**
    A JSON object with the same format as described in ``GET``, eg.,

    ::

      {
        "plate":
        [
          {
            "id"        : 1,
            "channels"  :
            [
              {
                "id"    : 1,
                "name"  : "GFP",
                "time"  : ["00:00:00", "00:05:00", "00:10:00", "00:15:00"],
                "well"  : ["A01", "A02", "A03", "A04", "A05", "A06", ...],
                "value" : [ [1, 1, 1, ... ], ... ]
              }
            ]
          }
        ]
      }

**Output**
    Newly altered plate object, eg.,

    ::

      {
        "plate":
        [
          {
            "id"        : 1,
            "channels"  :
            [
              {
                "id"    : 1,
                "name"  : "GFP",
                "time"  : ["00:00:00", "00:05:00", "00:10:00", "00:15:00"],
                "well"  : ["A01", "A02", "A03", "A04", "A05", "A06", ...],
                "value" : [ [1, 1, 1, ... ], ... ]
              }
            ]
          }
        ]
      }

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
    A JSON object describing query criteria. Mandatory.

    ::

      {
        "experiment": eid,
        "channel"   : cid,
        "factors"   :
        [
          {
            "id"    : fid,
            "levels": flvl,
          },
          ...
        ]
      }

    Unquoted variables are

    * ``eid``:   Integer. Experiment ID.
    * ``cid``:   Integer. Channel ID.
    * ``fid``:   Integer. Factor ID.
    * ``flvl``:  Array of strings. Levels of factor.

**Output**
    A JSON object containing time series data, for expample:

    ::

      {
        "id"     : qid,
        "query"  : query,
        "result" :
        [
          {
           "value": -1.1618426259,
           "time" : "00:00:00",
           "l"    : -2.6017329022,
           "u"    : 0.2949717757
          },
          {
           "value": -1.1618426259,
           "time" : "00:00:05",
           "l"    : -2.6017329022,
           "u"    : 0.2949717757
          },
          ...
        ]
      }

    Unquoted variables are

    * ``qid``:    Integer. Query ID. Internal use only.
    * ``query``:  Object.  Input query body.
    * ``l`` and ``u`` are lower and upper limits (95% confidence interval) of time
      series data
