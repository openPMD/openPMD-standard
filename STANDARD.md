The openPMD Standard
====================

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED",  "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC 2119](http://tools.ietf.org/html/rfc2119).

All `keywords` in this standard are case-sensitive.

The naming *(float)* without a closer specification is used if the user can
choose which kind of floating point precision shall be used.
The naming *(int)* without a closer specification is used if the user can
choose which kind of signed integer type shall be used.


The Versions of this Standard
-----------------------------

Major versions of this standard do not need to be backwards compatible.
Minor versions need to be backwards compatible and should for example
only add optional information or tool updates.
Revisions are reserved for minor typos in the documentation (but not in
keywords).


Hierarchy of the Data File
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
  - `%T`: an iteration (unsigned integer type,
                        same range as a 64bit unsigned integer).

**Paths** to **groups** end on `/`, e.g., `/mySubGroup/` and **data sets** end
without a `/`, e.g., `dataSet` or `/path/to/dataSet`.

Each file's *root* directory (path `/`) must at leat contain the attributes:

  - `version`
    - type: *(string)*
    - description: (targeted) version of the format in "MAJOR.MINOR.REVISION",
                   see section "The versions of this standard",
                   minor and revision must not be neglected
    - example: `1.0.0`

  - `basePath`
    - type: *(string)*
    - description: a common prefix for all data sets and sub-groups of a
                   specific iteration
    - allowed value: fixed to `/data/%T/` for this version of the standard

  - `fieldsPath`
    - type: *(string)*
    - description: path *relative* from the `basePath` to the field records
    - example: `fields/`

  - `particlesPath`
    - type: *(string)*
    - description: path *relative* from the `basePath` to the groups for each
                   particle species and the records they include
    - example: `particles/`

It is *recommended* that each file's *root* directory (path `/`) further
contains the attributes:

  - `author`
    - type: *(string)*
    - description: Author and contact for the information in the file
    - example: `Axel Huebl <a.huebl@hzdr.de>`

  - `software`
    - type: *(string)*
    - description: the software/code/simulation that created the file
    - example: `PIConGPU`, `Warp`

  - `softwareVersion`
    - type: *(string)*
    - description: the version of the software/code/simulation that created the file
    - example: `1.2.1`, `80c7551`, `rev42`

  - `date`
    - type: *(string)*
    - description: date of creation in format "YYYY-MM-DD HH:mm:ss tz"
    - example: `2015-12-02 17:48:42 +0100`

Each group and path might contain the attribute **comment** for general
human-readable documentation, e.g., for features not yet covered by the
standard:

  - `comment`
    - type: *(string)*
    - description: an arbitrary comment
    - example: `After each time step we randomly removed 5 particles.`


Iterations and Time Series
--------------------------

Iterations can be encoded in either the file name of each master-file of a
time step or in groups of the same file.

The choosen style shall not vary within a related set of iterations.

Since the meaning of *time* can be confusing for simulations with non-constant
time steps, records that are stagered in time or simulations in a frame of
reference moving with relativistic speeds, an iteration describes a single
simulation cycle.

Each file's *root* directory (path `/`) must further define the attributes:

  - `iterationEncoding`
    - type: *(string)*
    - description: tells if other iterations of this series, from the
                   file-format's API point of view, encoded in the same file or
                   is an other `open/close` call necessary to access other iterations
    - allowed values:
      - `fileBased` (multiple files)
      - `groupBased` (one file)

  - `iterationFormat`
    - type: *(string)*
    - description: a well defined string with the iteration `%T` placeholder
                   defining either the series of files (`fileBased`) or the
                   series of groups within a single file (`groupBased`)
                   that allows to extract the iteration from it;
                   for `fileBased` formats the iteration must be included
                   in the file name;
                   the format depends on the selected `iterationEncoding` method
    - examples:
      - for `fileBased`:
        - `filename_%T.h5` (without file system directories)
      - for `groupBased`:
        - `/data/%T/` (must be equal to and encoded in the `basePath`)


Unit Systems and Dimensionality
-------------------------------

While this standard does not impose any unit system on the data that is
stored itself, it still imposes a common interface to convert one system
to an other.

Each quantity with a dimension must define a unit conversation factor,
often called `unitSI` in the document, to transform it to a corresponding
quanity in the International System of Units (SI).

For each field or particle `record` (defined later) the following
attributes are mandatory:

  - `unitSI`
    - type: *(double / REAL8*)
    - description: a conversation factor to multiply data with to be
                   represented in SI
    - example: `2.99792e8`

  - `unitDimension`
    - powers of the 7 base measures characterizing the record's unit in SI
      (length L, mass M, time T, electric current I, thermodynamic temperature
       theta, amount of substance N, luminous intensity J)
    - does *not* represent if the record is a 1, 2 or 3D array
    - examples:
      - "m / s" is of dimension `L=1` and `T=-1`,
        store array `[1.; 0.; -1.; 0.; 0.; 0.; 0.]`
      - "N = kg * m / s^2", store array `[1.; 1.; -2.; 0.; 0.; 0.; 0.]`


In addition to that, each `record` must define the attributes:

  - `time`
    - type: *(float / REAL8)*
    - description: the current time;
                   add a `comment` to your record if it can not be described
                   with a common "time" (or if it's definition of time varies
                   from the definition of time in other record)

  - `timeUnitSI`
    - type: *(double / REAL8)*
    - description: a conversation factor to `seconds`
    - example: `1.0e-16`


*Note to implementors* 

For the special case of simulations, there can be the situation that a certain
process scales independently of a given fixed reference quantity that
can be expressed in SI, e.g., the growth rate of a plasma instability can
scale over various orders of magnitudes solely with the plasma frequency
and the basic constants such as mass/charge of the simulated particles.

In such a case, picking a *reference density* to determine the `unitSI`
factors is mandatory to provide a fallback for compatibility.

For human readable output, it is *recommended* to add the actual string
of the unit in the corresponding `comment` attribute.


Grid Based Records (Fields)
---------------------------

Fields shall be represented via homogeneous data sets on an equal-spaced,
regular grid.

Scalar fields are stored in a data set with the same name as the field.
Vector and tensor fields shall be represented component-wise as a
*collection of individual scalar fields* using a common sub-group that
is equal to the field name. We refer to the scalar field itself and
the vector sub-group as `field record`.

### Naming conventions

  - `scalar` fields
    - type: *(any type)*
    - data set: `recordName` unique name in group `basePath` + `fieldsPath`

  - `vector` fields
    - type: *(any type)*
    - data sets: `recordName/x`, `recordName/y`, `recordName/z` when
                 writing the *Cartesian* components of the vectors;
                 `recordName/r`, `recordName/t`, `recordName/z` when
                 writing the *cylindrical* components of the vectors.
                 Here `recordName` is a sub-group. The components `x`,
                 `y`, `z` (or respectively `r`, `t`, `z`) are data
                 sets of `scalar` fields.

### Mandatory attributes for each field

The following attributes must be stored with the `fieldName` (which is a
data set attribute for `scalar` or a group attribute for `vector` fields):

  - `unitSI`
    - type: *(double / REAL8)*
    - description: unit-conversion factor to multiply the stored record with to
                   be represented in SI
    - example: `2.99792e8`

  - `unitDimension`
    - see general section above
    - powers of the 7 base measures characterizing the record's unit in SI
      (length L, mass M, time T, electric current I, thermodynamic temperature
       theta, amount of substance N, luminous intensity J)
    - does *not* represent if the record is a 1, 2 or 3D array

  - `geometry`
    - type: *(string)*
    - description: geometry of the mesh of the field record, right-handed
                   coordinate systems are imposed
    - allowed values:
      - `cartesian`: standard Cartesian mesh, the standard order of axes indexing
                     shall be `x`, `y`, `z`
      - `cylindrical`: regularly-spaced mesh in the r-z plane, with
                       Fourier decomposition in the azimuthal direction (See
                       [doi:10.1016/j.jcp.2008.11.017](http://dx.doi.org/10.1016/j.jcp.2008.11.017))
                       In this case, the field arrays are stored as a
                       three-dimensional record where the last axis corresponds
                       to the `z` direction, the second axis correspond to the
                       `r` direction and where the first axis corresponds to
                       the azimuthal mode. (This last axis has length `2m+1`,
                       where `m` is the number of modes used. By convention,
                       this first stores the real part of the mode `0`, then
                       the real part of the mode `1`, then the imaginary part
                       of the mode `1`, then the real part of the mode `2`,
                       etc.)
      - `other`

  - `geometryParameters`
    - type: *(string)*
    - description: additional parameters for the geometry, separated by a `;`,
                   this attribute can be omitted if geometry is `cartesian`
                   or `cylindrical` geometry with only mode `m=0` is used
    - examples:
      - for `cylindrical` geometry:
        - `m=3;imag=+` (3 *modes* and using a `+` sign for the definiton of the *imaginary* part)
                        ![definition of imaginary part](img/cylindrical.png)

  - `gridSpacing`
    - type: 1-dimensional array containing N *(float / REAL4)*
            elements, where N is the number of dimensions in the simulation.
    - description: spacing of the grid points along each dimension (in the
                   units of the simulation); this refers to the spacing of the
                   actual record that is written to the file, not that of the
                   simulation grid. (The record written may be down-sampled, as
                   compared to the simulation grid).
    - examples:
      - In the case where `geometry` is `cartesian`, the dimensionality
        `N` of the array determines if the field record is 1, 2 or 3D. The
        elements of the array should correspond to `dx`, `dy`, `dz`, in
        this order.
      - In the case where `geometry` is `cylindrical`, the array
        should be of length 2 and contain `dr` and `dz`, in that order.

  - `gridGlobalOffset`
    - type: 1-dimensional array containing N *(double / REAL8)*
            elements, where N is the number of dimensions in the simulation
    - description: start of the current domain of the simulation (position of the
                   beginning of the first cell) in simulation units
    - example: `[0.0; 0.0; 0.0]` or `[0.5; 0.5; 0.5]`

  - `gridUnitSI`
    - type: *(double / REAL8)*
    - description: unit-conversion factor to multiply each value in `gridSpacing`
                   and `gridGlobalOffset`, in order to convert from simulation units
                   to SI units
    - example: `1.0e-9`

  - `dataOrder`
    - type: *(string)*
    - allowed values: `Fortran` or `C` (also for 2D records)
    - description: describes the fastest/slowest increasing index for 2D and 3D
                   records (e.g., the difference between a Fortran and C array);
                   can be omitted for 1D record
    - example:
      - `Fortran`: ordering of matrixes is linearized in memory in column-major order
      - `C`:       exactly the opposite ordering (row-major), reading matrixes from
                   a Fortran code will appear transposed in C (or C-based applications
                   such as Python)

The following attributes must be stored with each scalar record and each
component of a vector record:

  - `position`
    - type: 1-dimesional array of N *(float / REAL4)* where N is the number of
            dimensions in the simulation.
    - range of each value: `[ 0.0 : 1.0 )`
    - description: position of the component on the grid/node/cell/voxel;
                   `0.0` means at the beginning of the cell and `1.0` is the
                   beginning of the next cell;
                   in the same order as the `gridSpacing` and `gridOffset`

Particle Records
----------------

Each particle species shall be represented as a group `particleName/` that
contains all its records. Records per particle are generally stored as
contigous array of a non-compound type.

For records that are the same for all particles in a particle species, e.g.,
all electrons have `charge` `-1`, replacing the record with a group
attribute of the same name is possible, as described in the following
paragraphs.

### Naming conventions

As with mesh-based `vector` record, compound particle vector records
are again splitted in scalar components that are stored in a common
sub-group `particleName/recordName/`.

Replacing a record for a particle with a constant value for all particles in
the particle species, independent if the record is stored as a vector or
scalar record, works as follows. The record `particleName/recordName` shall
be replaced with an empty sub-group `particleName/recordName/` that hosts the
group-attribute `value` and other mandatory attributes such as `unitSI`. For
components of vector-records, the component `particleName/recordName/x` shall
be replaced with an empty sub-sub-group `particleName/recordName/x/` that again
hosts the group-attribute `value` and other mandatory attributes such as
`unitSI`.

### Mandatory records for each particle species

  - `position/` + `x`, `y`, `z` (or `r`, `t`, `z` respectively)
    - type: each component in *(float)*
    - description: component-wise global position of a particle, if not
                   enforced otherwise by a domain-specific extension (see below)

  - `momentum/` + `x` or `y` or `z` (or `r`, `t`, `z` respectively)
    - type: each component in *(float)*
    - description: component-wise momentum of the attribute

### Mandatory attributes for each particle record

The following attributes must be stored with the `particleName/recordName`
(which is a data set attribute for a `scalar` particle record or a group
attribute for a `compound` or `vector` particle record):

  - `unitSI`
    - type: *(double / REAL8)*
    - description: unit-conversion factor to multiply the stored record with to
                   be represented in SI
    - example: `1.0e-9`

  - `unitDimension`
    - see general section above
    - powers of the 7 base measures characterizing the record's unit in SI
      (length L, mass M, time T, electric current I, thermodynamic temperature
       theta, amount of substance N, luminous intensity J)
    - does *not* represent if the record is a 1, 2 or 3D array


Domain-Specific Extensions
--------------------------

Why extensions?
  -> standard == enough for general fields & analysis
  -> extensions == code interoperability of the same domain (naming conventions)
                   open access unique description & meta
                   additional hints for domain-specific analysis

-> format == openPMD + ED-PIC
                     + ExtensionABC

Up to now, the following domain-specific naming conventions for have been
defined:

- **ED-PIC**: electro-dynamic/static particle-in-cell codes,
  see [EXT_ED-PIC.md](EXT_ED-PIC.md).

Extensions to similar domains such as fluid, finite-element or
molecular-dynamics simulations, CCD images or other grid-based records can
proposed for [future versions](CONTRIBUTING.md) of this document.
