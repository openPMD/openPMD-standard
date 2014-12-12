The openPMD Standard
====================

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED",  "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC 2119](http://tools.ietf.org/html/rfc2119).


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


Unit Systems and Dimensionality
-------------------------------

While this standard does not impose any unit system on the data that is
stored itself, it still imposes a common interface to convert one system
to an other.

Each quantity with a dimension must define a unit conversation factor,
often called `unitSI` in the document, to transform it to a corresponding
quanity in SI (International System of Units).

Attribute of a data set:

  - `unitSI`
    - type: *(double*)
    - description: a conversation factor to multiply data with to be
                   represented in SI
    - example: `2.99792e8`

  - `dimension`
    - reserved for future use (requires struct-attribute support)
    - powers of the 7 base measures characterizing this data set
      (length L, mass M, time T, electric current I, thermodynamic temperature
       theta, amount of substance N, luminous intensity J)
    - does *not* represent if the data set is a 1, 2 or 3D array

*Note to implementors* 

For the special case of simulations, there can be the situation that a certain
process scales independently of a given fixed reference quantity that
can be expressed in SI, e.g., the growth rate of a plasma instability can
scale over various orders of magnitudes solely with the plasma frequency
and the basic constants such as mass/charge of the simulated particles.

In such a case, picking a *reference density* to determine the `unitSI`
factors is mandatory to provide a fallback for compatibility.


Grid based data (fields)
------------------------

Fields shall be represented as homogeneous data sets of on a equal-spaced,
regular grid.

Scalar fields are stored in a data set with the same name as the field.
Vector and tensor fields shall be represented component-wise as a *structure
of scalar fields* using a common sub-group as the name.

### Naming conventions

  - `scalar` fields
    - type: *(any type)*
    - data set: `fieldName` unique name in group `basePath` + `fieldsPath`

  - `vector` fields
    - type: *(any type)*
    - data set: `fieldName/x`, `fieldName/y`, `fieldName/z`
                while `fieldName` is a sub-group and `x`, `y`, `z` are
                data sets of `scalar` fields

### Mandatory attributes for each field

The following attributes must be stored with the `fieldName` (which is a
data set attribute for `scalar` and a group attribute for `vector` fields):

  - unit-conversion factor to SI
  - dimension of the unit of the data field
  - dx, dy, dz + units
  - order: ijk or kji

The following attributes must be stored with each data set:

  - position of the component on the grid/node/cell/voxel (=left/right handed)

The total size of a field and it's offset, e.g., in a co-moving window
simulation, are not covered by this standard and shall be provided by
the API of the according file format.


Particle data (particles)
-------------------------

  - min attributes: position, momentum
  - recommendation for particle data sets > 100 GB,
    data locality aware particleGroups aka "particle_info"


Domain-Specific Extensions
--------------------------

Why extensions?
  -> standard == enough for general fields & analysis
  -> extensions == code interoperability of the same domain (naming conventions)
                   open access unique description & meta
                   additional hints for domain-specific analysis

-> format == openPMD + ED-PIC
                     + ExtensionABC

Up to now, the following domain-specific naming conventions for data fields
and *algorithms*, *methods* and/or *schemes* have been defined:

- **ED-PIC**: electro-dynamic/static particle-in-cell codes,
  see [EXT_ED-PIC.md](EXT_ED-PIC.md).

Extensions to similar domains such as fluid, finite-element or
molecular-dynamics simulations, CCD images or other grid-based data can
proposed for [future versions](CONTRIBUTING.md) of this document.
