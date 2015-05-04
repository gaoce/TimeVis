******************
Design of Software
******************
The cell array research can be organized at three different levels: experiment,
layout and plate. Accordingly, the data are organized with these three levels
too.

1. Experiment
=============
A single experiment aims to answer one question: how different factors
(independent variables) influence channels (dependent variables). The experiment
information consists experiment name, user and number of wells for microplates,
as well as meta information about factors and channels.

2. Layout
=========
A unique layout is determined by the specific combination of factors in all the
wells. For example:

+------+------+------+-----+
| Well | Gene | Dose | ... |
+======+======+======+=====+
| 1    | 'aa' | 42   | ... |
+------+------+------+-----+
| 2    | 'aa' | 4.2  | ... |
+------+------+------+-----+
| ...  | ...  | ...  | ... |
+------+------+------+-----+


3. Plate
========
A unique plate is foundamental unit of experimetn. Plate information includes
the experiment measures.
