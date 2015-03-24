The openPMD Standard
====================

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED",  "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC 2119](http://tools.ietf.org/html/rfc2119).


The versions of this standard
-----------------------------

Major versions of this standard do not need to be backwards compatible.
Minor versions need to be backwards compatible and should for example
only add additional information.
Revisions are reserved for minor typos in the documentation (but not in
keywords).


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

  - `version`
    - type: *(string)*
    - description: (targeted) version of the format in "MAJOR.MINOR.REVISION",
                   see section "The versions of this standard",
                   minor and revision must not be neglected
    - example: "1.0.0"

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

Each file's *root* directory (path `/`) might contain these attributes
(these attributes are *recommended* and their usage is *reserved* for):

  - `author`
    - type: *(string)*
    - description: Author and contact of the data
    - example: "Axel Huebl <a.huebl@hzdr.de>"

  - `software`
    - type: *(string)*
    - description: the software/code/simulation that created the file
    - example: "PIConGPU", "Warp"

  - `softwareVersion`
    - type: *(string)*
    - description: the version of the software/code/simulation that created the file
    - example: "1.2.1", "80c7551", "rev42"

  - `date`
    - type: *(string)*
    - description: date of creation in format "YYYY-MM-DD HH:mm:ss TZ"
    - example: "2015-12-02 17:48:42 +0100"

Each group and path might contain the attribute **comment** for general
human-readable documentation, e.g., for features not yet covered by the
standard:

  - `comment`
    - type: *(string)*
    - description: An arbitrary comment
    - example: "After each time step we randomly removed 5 particles."


Iterations and Time Series
--------------------------

Iterations can be encoded in either the file name of each master-file of a
time step or in groups of the same file.

The choosen style shall not vary within a related set of iterations.

Since the meaning of *time* can be confusing for simulations with non-constant
time steps or or simulations in a frame of reference moving with relativistic
speeds, an iteration describes a single simulation cycle.

Each file's *root* directory (path `/`) must further define the attributes:

  - `iterationEncoding`
    - type: *(string)*
    - allowed values: selection of either "fileBased" (multiple files) or
                      "groupBased" (one file)
    - description: are other iterations of this series, from the file-format's
                   API point of view, encoded in the same file or is an
                   other `open/close` call necessary to access other iterations?

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
      - `fileBased`: "filename_%T.h5" (without file system directories)
      - `groupBased`: "/data/%T/" (must be encoded in the `basePath`)

  - `time`
    - type: *(float / REAL4)*
    - description: the current time;
                   add a `comment` to your data set if it can not be described
                   with a common "time"

  - `timeStep`
    - type: *(float / REAL4)*
    - description: the time step used for each iteration;
                   for simulations with non-constant time steps, use
                   the last time step used to reach this iteration

  - `timeUnitSI`
    - type: *(double / REAL8)*
    - description: a conversation factor to `seconds`
    - example: `1.0e-16`


Unit Systems and Dimensionality
-------------------------------

While this standard does not impose any unit system on the data that is
stored itself, it still imposes a common interface to convert one system
to an other.

Each quantity with a dimension must define a unit conversation factor,
often called `unitSI` in the document, to transform it to a corresponding
quanity in the International System of Units (SI).

Attribute of a data set:

  - `unitSI`
    - type: *(double / REAL8*)
    - description: a conversation factor to multiply data with to be
                   represented in SI
    - example: `2.99792e8`

  - `unitDimension`
    - reserved for future use (requires struct-attribute support)
    - powers of the 7 base measures characterizing this data set
      (length L, mass M, time T, electric current I, thermodynamic temperature
       theta, amount of substance N, luminous intensity J)
    - does *not* represent if the data set is a 1, 2 or 3D array
    - example: "N = kg * m / s^2", store struct "[1.; 1.; -2.; 0.; 0.; 0.; 0.]"

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
data set attribute for `scalar` or a group attribute for `vector` fields):

  - `unitSI`
    - type: *(double / REAL8)*
    - description: unit-conversion factor to multiply the stored data with to
                   be represented in SI
    - example: 2.99792e8

  - `unitDimension`
    - reserved for future use (requires struct-attribute support)
    - powers of the 7 base measures characterizing this data set
      (length L, mass M, time T, electric current I, thermodynamic temperature
       theta, amount of substance N, luminous intensity J)
    - does *not* represent if the data set is a 1, 2 or 3D array

  - `geometry` / `coordinateSystem` ?
    - type: *(string)*
    - description: geometry of the mesh of the field data, right-handed
                   coordinate systems are imposed
    - allowed values:
      - `cartesian`
      - `cylindrical` ([doi:10.1016/j.jcp.2008.11.017](http://dx.doi.org/10.1016/j.jcp.2008.11.017))
      - `other`

  - `geometryParameters`
    - type: *(string)*
    - description: additional parameters for the geometry, separated by a `;`,
                   this attribute can be omitted if `cartesian` geometry
                   or `cylindrical` geometry with only mode `m=0` is used
    - examples:
      - for `cylindrical` geometry:
        - `m=3;imag=+` (3 *modes* and using a `+` sign for the definiton of the *imaginary* part)
                        ![definition of imaginary part](img/cylindrical.png)

  - `gridSpacing`
    - type: N-dimensional struct of *(float / REAL4)*
    - description: spacing of the grid; the dimensionality `N` of the struct (array)
                   determines if the field data is 1, 2 or 3D
    - examples and required order of attributes:
      - `cartesian`: `dx`, `dy`, `dz`
      - `cylindrical`: `dr`, `dz`

  - `gridGlobalOffset`
    - type: N-dimensional struct of *(float / REAL4)*
    - ...

  - `gridUnitSI`
    - type: *(double / REAL8)*
    - description: unit-conversion factor to multiply each value in `gridSpacing`
                   and `gridGlobalOffset` with to be represented in SI
    - example: 1.0e-9

  - `dataOrder`
    - type: *(string)*
    - allowed values: `Fortran` or `C` (also for 2D data sets)
    - description: describes the fastest/slowest increasing index for 2D and 3D
                   data sets (e.g., the difference between a Fortran and C array);
                   can be omitted for 1D data sets
    - example:
      - `Fortran`: ordering of matrixes is linearized in memory in column-major order
      - `C`:       exactly the opposite ordering (row-major), reading matrixes from
                   a Fortran code will appear transposed in C (or C-based applications
                   such as Python)

The following attributes must be stored with each data set:

  - `position`
    - type: struct of *(float / REAL4)*
    - range of each value: `[ 0.0 : 1.0 )`
    - description: position of the component on the grid/node/cell/voxel;
                   `0.0` means at the beginning of the cell and `1.0` is the
                   beginning of the next cell;
                   in the same order as the `gridSpacing` and `gridOffset`

Particle data (particles)
-------------------------

Each particle species shall be represented as a group `particleName/` that
contains all its properties. Properties per particle are generally stored as
contigous array of a non-compound type.

For properties that are the same for all particles in a particle species, e.g.,
all electrons have `charge` `-1`, replacing the data set with a group
attribute of the same name is possible, as described in the following
paragraphs.

### Naming conventions

As with mesh-based `vector` properties, compound particle vector properties
are again splitted in scalar sub-properties that are stored in a common
sub-group `particleName/propertyName/`.

Replacing a data set for a particle property with a constant property for all
particles in the particle species, independent if the data set is stored as a
sub-property in a sub-group or if the data set is the scalar property itself,
works as follows. The data set `particleName/propertyName` shall be replaced
with an empty sub-group `particleName/propertyName/` that hosts the
group-attribute `value` and other mandatory attributes such as `unitSI`. The
sub-property `particleName/propertyName/x` shall be replaced with an  empty
sub-sub-group `particleName/propertyName/x/` that again hosts the
group-attribute `value` and other mandatory attributes such as `unitSI`.

### Mandatory properties for each particle species

  - `position/` + `x` or `y` or `z`
    - type: each data set in *(float / REAL4)* or *(double / REAL8)*
    - description: component-wise global position of a particle, if not
                   enforced otherwise by a domain-specific extension (see below)

  - `momentum/` + `x` or `y` or `z`
    - type: each data set in *(float / REAL4)* or *(double / REAL8)*
    - description: component-wise momentum of the attribute

### Mandatory attributes for each particle property

The following attributes must be stored with the `particleName/propertyName`
(which is a data set attribute for a `scalar` particle property or a group
attribute for a `compound` or `vector` particle property):

  - `unitSI`
    - type: *(double / REAL8)*
    - description: unit-conversion factor to multiply the stored data with to
                   be represented in SI
    - example: 1.0e-9

  - `unitDimension`
    - reserved for future use (requires struct-attribute support)
    - powers of the 7 base measures characterizing this data set
      (length L, mass M, time T, electric current I, thermodynamic temperature
       theta, amount of substance N, luminous intensity J)
    - does *not* represent if the data set is a 1, 2 or 3D array


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
