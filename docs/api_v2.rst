*****************
API Documentation
*****************

1. Basic functions
==================

+------------------------+------------------------------+
| URI                    | Functions                    |
+========================+==============================+
| ``/api/v2/experiment`` | experiment information       |
+------------------------+------------------------------+
| ``/api/v2/layout``     | layout information           |
+------------------------+------------------------------+
| ``/api/v2/plate``      | plate data                   |
+------------------------+------------------------------+
| ``/api/v2/timeseries`` | time series data for a gene  |
+------------------------+------------------------------+

2. Experiment
=============

1. Endpoint
---------------------
``/api/v2/experiment``

2. HTTP verbs
-------------

1. Get
^^^^^^
Some source code::

  {
    "exp_id1": 
    {
      "name": "exp_name1", 
      "users": ["user1", "user2"],
      "well": 384,
      "chanels": ["channel1", "chanel2"],
      "factors": [{"name": "factor1", "type": "decimal"}]
    },
  }

2. Post
^^^^^^^

