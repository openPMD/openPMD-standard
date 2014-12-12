The openPMD Convention
======================

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED",  "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC 2119](http://tools.ietf.org/html/rfc2119).


A Note on Unit Systems
----------------------

  - SI
  - "unitless" simulations -> choose a reference value, e.g. density
  - `unitSI`: always double precision, always the factor to *multiply* the
              data with to get a SI value


Hierarchy of the data file
--------------------------

The used hierarchical data file format must provide the capability to

  - create groups and sub-groups (in-file directories)
  - create multi-dimensional, homogenous array-based data structures

while allowing for each of those to assign

  - multiple, distinct attributes
    (values of basic and/or combined floating/integer types and strings)
  - with platform-independent representation.

We define the following placeholders and reserved characters:

  - `/`: separator of groups
  - `%T`: a time step (unsigned integer type,
                       same range as a 64bit unsigned integer).

**Paths** to **groups** end on `/`, e.g., `/mySubGroup/` and **data sets** end
without a `/`, e.g., `dataSet` or `/path/to/dataSet`.

Each file's *root* directory (path `/`) must at leat contain the attributes:

  - `basePath`
    - type: *(string)*
    - description: a common prefix for all data sets and sub-groups
    - example: "/data/%T/" but at least `/`

  - `fieldsPath`
    - type: *(string)*
    - description: path *relative* from the baseDir to the field data sets
    - example: "fields/"

  - `particlesPath`
    - type: *(string)*
    - description: path *relative* from the baseDir to the particle data sets
    - example: "particles/"


Time Series
-----------

Time series can be encoded in either the file name of each master-file of a
time step or in groups of the same file.

The choosen style shall not vary within a single time series.

Each file's *root* directory (path `/`) must further define the attributes:

  - `timeStepEncoding`
    - type: *(string)*
    - description: are other time steps of this series, from the file-format's
                   API point of view, encoded in the same file or is an
                   other `open/close` call necessary to access other time steps?
    - allowed options: selection of either "fileBased" (multiple files) or
                       "groupBased" (one file)

  - `timeStepFormat`
    - type: *(string)*
    - description: a well defined string with the time `%T` placeholder
                   defining either the series of files (`fileBased`) or the
                   series of groups within a single file (`groupBased`)
                   that allows to extract the time step from it;
                   for `fileBased` formats the time step must be included
                   in the file name;
                   the format depends on the selected `timeStepEncoding` method
    - examples:
      - `fileBased`: "filename_%T.h5" (without file system directories)
      - `groupBased`: "/data/%T/"

  - `timeStepUnitSI`
    - type: *(double)*
    - description: a conversation factor to `seconds`
    - example: `1.0e-16`


Mesh based data (fields)
------------------------

  - scalar vs vector fields
  - position of the component on the grid/node/cell/voxel
  - dimension of the unit of the data field
  - unit-conversion factor to SI


Particle data (particles)
-------------------------


Domain-Specific Extensions
--------------------------

Up to now, the following domain-specific naming conventions for data fields
and *algorithms*, *methods* and/or *schemes* have been defined:

- **ED-PIC**: electro-dynamic/static particle-in-cell codes,
  see [EXT_ED-PIC.md](EXT_ED-PIC.md).

Extensions to similar domains such as fluid, finite-element or
molecular-dynamics simulations, CCD images or other grid-based data can
proposed for [future versions](CONTRIBUTING.md) of this document.
