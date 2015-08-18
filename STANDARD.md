The openPMD Standard
====================

VERSION: *draft* (April 14th, 2015)

Conventions Throughout this Documents
--------------------------------------

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED",  "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC 2119](http://tools.ietf.org/html/rfc2119).

All `keywords` in this standard are case-sensitive.

The naming *(float)* without a closer specification is used if the user can
choose which kind of floating point precision shall be used.
The naming *(uint)* and *(int) without a closer specification is used if the
user can choose which kind of (un)signed integer type shall be used.
The naming for the type *(string)* refers to fixed-length, plain ASCII encoded
character arrays since they are the only ones that are likely to propagate
through all file-format APIs and third-party programs that use them.

Sometimes brackets `<Name>` are used for keywords while the `<>` only indicate
the keyword is mandatory (but the `<>` itself shall not be written).
Accordingly, optional keywords and options are indicated via square brackets
`[Name]`.


The Versions of this Standard
-----------------------------

Versions of the standard allow codes and implementors to easily differenciate
between new updates that are incooperated.

The full version number is always used in format `<MAJOR>.<MINOR>.<REVISION>` .

Improvements will be sought to be backwards compatible, if that is not
possible then changes in the major version of this standard indicate
incompatibility.
Minor version updates instead need to be backwards compatible and should for
example only add optional information or tool updates.
Revisions are reserved for minor typos in the documentation and tools (but not
for changes in keywords).


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

  - `openPMD`
    - type: *(string)*
    - description: (targeted) version of the format in "MAJOR.MINOR.REVISION",
                   see section "The versions of this standard",
                   minor and revision must not be neglected
    - example: `1.0.0`

  - `openPMDextension`
    - type: *(uint32)*
    - description: the bit-mask of unique IDs of applied extensions of the
                   openPMD standard
                   (see: *Domain-Specific Extensions*);
                   to test for a specific extension `ID` perform a bit-wise
                   `AND` operation on `openPMDextension`:
                   `extension_1_used = (( openPMDextension AND ID ) == ID)`
    - note: if only one extension is used at a time, the value for
            `openPMDextension` is simply the `ID` of the extension
    - examples:
      - `0`: only the base standard is used
      - `1`: the base standard and the extension with ID `1` apply for the file
      - general case (discouraged in this version of the standard):
             `openPMDextension=0 OR <ID1> OR <ID2> OR <...>` (bit-wise `OR`)

  - `basePath`
    - type: *(string)*
    - description: a common prefix for all data sets and sub-groups of a
                   specific iteration;
                   this string only indicates *how* the data is stored,
                   to create a real path from it replace all occurences
                   of `%T` with the integer value of the iteration, e.g.,
                   `/data/%T` becomes `/data/100`
    - allowed value: fixed to `/data/%T/` for this version of the standard

  - `meshesPath`
    - type: *(string)*
    - description: path *relative* from the `basePath` to the mesh records
    - example: `meshes/`

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
time step or in groups of the same file. (Here, an *iteration* refers
to a single simulation cycle.)

The choosen style shall not vary within a related set of iterations.

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

In addition to holding information about the iteration, each series of
files  (`fileBased`) or series of groups (`groupBased`) should have
attributes that describe the current time and the last
time step. 

 - `time`
   - type: *(float / REAL8)*
   - description: the time corresponding to this iteration. Because at
                  one given iteration, different quantities may be defined
                  at different times (e.g. in a staggered code), this time is
                  defined as a global reference time for this iteration. This
                  ambiguity is then resolved at the *record* level (see below),
                  where each quantity has an attribute `timeOffset` which
                  corresponds to its offset with respect the reference `time`.
   - example: In a staggered PIC code, the `time` attribute can be the time at
              which the electric field is defined, and the magnetic field would
              then have a non-zero `timeOffset`.

 - `dt`
   - type: *(float / REAL8)*
   - description: The latest time step (that used to reach this iteration).
                  This is needed at the iteration level, since the time step
                  may vary from iteration to iteration in certain codes.

 - `timeUnitSI`
    - type: *(double / REAL8)*
    - description: a conversation factor to convert `time` and `dt` to `seconds`
    - example: `1.0e-16`


Unit Systems and Dimensionality: Required for each `Record`
-----------------------------------------------------------

While this standard does not impose any unit system on the data that is
stored itself, it still imposes a common interface to convert one system
to an other.

Each quantity with a dimension must define a unit conversation factor,
often called `unitSI` in the document, to transform it to a corresponding
quanity in the International System of Units (SI).

For each mesh or particle `record` (defined later) the following
attributes shall be added:

- **Required:**

  - `unitSI`
    - type: *(double / REAL8*)
    - description: a conversation factor to multiply data with to be
                   represented in SI
    - example: `2.99792e8`

  - `unitDimension`
    - type: array of 7 *(double / REAL8)*
    - powers of the 7 base measures characterizing the record's unit in SI
      (length L, mass M, time T, electric current I, thermodynamic temperature
       theta, amount of substance N, luminous intensity J)
    - does *not* represent if the record is a 1, 2 or 3D array
    - examples:
      - "m / s" is of dimension `L=1` and `T=-1`,
        store array `[1.; 0.; -1.; 0.; 0.; 0.; 0.]`
      - "N = kg * m / s^2", store array `[1.; 1.; -2.; 0.; 0.; 0.; 0.]`

  - `timeOffset`
    - type: *(float / REAL8)*
    - description: the offset between the time at which this record is
                   defined and the `time` attribute of the `basePath` level.
                   This should be written in the same unit system as `time`
                   (i.e. it should be multiplied by `timeUnitSI` to get the
                   actual time in seconds.)
	- example: In a staggered PIC code, if `time` is chosen to correspond to
               the time at which the electric field is defined, and if `dt`
               is e.g. 1e-5, `timeOffset` would be 0.5e-5 for the magnetic
               field and 0. for the electric field.

- **Note to implementors:**

For the special case of simulations, there can be the situation that a certain
process scales independently of a given fixed reference quantity that
can be expressed in SI, e.g., the growth rate of a plasma instability can
scale over various orders of magnitudes solely with the plasma frequency
and the basic constants such as mass/charge of the simulated particles.

In such a case, picking a *reference density* to determine the `unitSI`
factors is mandatory to provide a fallback for compatibility.

For human readable output, it is *recommended* to add the actual string
of the unit in the corresponding `comment` attribute.


Scalar, Vector and Tensor Records
---------------------------------

In general, all data sets shall be stored as homogenous arrays or matrices
respectively, depending on the (spatial) dimensionality of the record they
represent.

Records with only a scalar component are stored in a data set with the same name
as the record. Vector and tensor records shall be represented component-wise as a
*collection of individual scalar data sets* using a common sub-group that
is equal to the record name. We refer to the scalar record itself and
the vector sub-group as `record`, to the data sets in the vector sub-group
as `components`.

### Naming conventions

  - names of `records` and `components`
    - type: *(string)*
    - description: names of records and their components are only allowed to
                   contain the characters `a-Z`, the numbers `0-9` and the
                   underscore `_` (the regex `\w`)
    - rationale: this avoids incompatibilities between file formats and
                 allows efficient parsing via regular expressions

  - `scalar` record
    - type: *(any type)*
    - data set: `recordName` unique name in group `basePath` +
                `meshesPath` or alternatively in `basePath` +
                `particleName` + `particlesPath`
    - examples:
      - `/data/meshes/temperature`
      - `/data/particles/electrons/charge`

  - `vector` records
    - type: *(any type)*
    - data sets: `recordName/x`, `recordName/y`, `recordName/z` when
                 writing the *Cartesian* components of the vectors;
                 `recordName/r`, `recordName/t`, `recordName/z` when
                 writing the *cylindrical* components of the vectors.
                 Here `recordName` is a sub-group. The components `x`,
                 `y`, `z` (or respectively `r`, `t`, `z`) are data
                 sets of `scalar` meshes.
    - examples:
      - `/data/meshes/F/`
        - `x`
        - `y`
        - `z`
      - `/data/meshes/F/`
        - `r`
        - `t`
        - `z`
      - `/data/particles/electrons/position/`
        - `x`
        - `y`
        - `z`

### Required Attributes for `vector` and `tensor` records

  - `componentOrder`
    - type: *(string)*
    - description: semicolon-separated list that corresponds exactly to the
                   names of the components of the `vector` record;
                   this attribute determines the natural order of the
                   components in this record
    - examples:
      - `x;y;z`
      - `x;y`
      - `r;z`
      - `r;t;z`


Constant Record Components
--------------------------

For records components that are constant (for a certain iteration), replacing
the record component with a group attribute of the same name is possible, as
described in the following paragraphs. For scalar records, the component is as
usual the record itself.

Replacing a record component with a constant value for all values on the mesh
or for all particles respectively (see definitions below) works as follows:
The record's *data set* `component` shall be replaced with an empty *sub-group*
`component/` that hosts the group-attribute `value`.

Other mandatory attributes such as `unitSI` need to be added to the new
sub-group for *scalar records* as well; for vector and tensor records these
standard record attributes are still stored with the group of the
`recordName/`.

Examples:
  - the mesh record for a magnetic field `B` is constant for `B.x` and `B.y`:
    - `<basePath><meshesPath>B/`: record group with standard attributes, e.g.,
                                  `unitSI`
      - `x/`: sub-group with attribute `value=<C0>`
      - `y/`: sub-group with attribute `value=<C1>`
      - `z`: data set
  - the mesh record for a temperature field `T` is constant
    - `<basePath><meshesPath>T/`: record group with attribute `value=<C0>` and
                                  standard attributes, e.g., `unitSI`
  - the particle record `charge` for the particle species `electrons` is
    constant
    - `<basePath><particlesPath>electrons/charge/`: record group with attribute
                                                    `value=-1.0` and standard
                                                    attributes, e.g.,
                                                    `unitSI=1.60217657e-19`

Mesh Based Records
------------------

Mesh based records such as discreticed fields shall be represented as
homogenous records, usually in a N-dimensional matrix.

### Mandatory attributes for each `mesh record`

The following attributes must be stored additionally with the `meshName` record
(which is a data set attribute for `scalar` or a group attribute for `vector`
meshes):

  - `geometry`
    - type: *(string)*
    - description: geometry of the mesh of the mesh record, right-handed
                   coordinate systems are imposed
    - allowed values:
      - `cartesian`: standard Cartesian mesh, the standard order of axes indexing
                     shall be `x`, `y`, `z`
      - `thetaMode`: regularly-spaced mesh in the r-z plane, with
                     Fourier decomposition in the azimuthal direction (See
                     [doi:10.1016/j.jcp.2008.11.017](http://dx.doi.org/10.1016/j.jcp.2008.11.017))
                     In this case, the mesh arrays are stored as a
                     three-dimensional record where the last axis corresponds
                     to the `z` direction, the second axis correspond to the
                     `r` direction and where the first axis corresponds to
                     the azimuthal mode. (This last axis has length `2m+1`,
                     where `m` is the number of modes used. By convention,
                     this first stores the real part of the mode `0`, then
                     the real part of the mode `1`, then the imaginary part
                     of the mode `1`, then the real part of the mode `2`,
                     etc.)
      - reserved: `cylindrical`, `spherical`
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
        `N` of the array determines if the mesh record is 1, 2 or 3D. The
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

The following attributes must be stored with each `scalar record` and each
*component* of a `vector record`:

  - `position`
    - type: 1-dimesional array of N *(float / REAL4)* where N is the number of
            dimensions in the simulation.
    - range of each value: `[ 0.0 : 1.0 )`
    - description: relative position of the component on the current element of
                   the mesh/grid/node/cell/voxel;
                   `0.0` means at the beginning of the mesh element and `1.0` is the
                   beginning of the next mesh element;
                   the same dimensionality N as in `gridSpacing` and `gridOffset`


Particle Records
----------------

Each `particle species` shall be represented as a group `particleName/` that
contains all its records. Particles records are generally represented in
one-dimensional contigous records, where the n-th entry in
`particleName/recordNameA` and the n-th entry in `particleName/recordNameB`
belong to the same particle.

### Naming conventions

As with general `vector` records, compound particle vector records
are again splitted in scalar components that are stored in a common
sub-group `particleName/recordName/`
(see: *Scalar, Vector and Tensor Records*). Also, record components that are
constant for all particles of a species (and iteration) can be replaced with a
short-hand notation (see: *Constant Record Components*).

### Mandatory Records for each `Particle Species`

  - `position/` + components such as `x`, `y`, `z` (or `r`, `t`, `z` respectively)
    - type: each component in *(float)*
    - description: component-wise global position of a particle, if not
                   enforced otherwise by a domain-specific extension (see below)

### Additional `Records` for each `Particle Species`

- **Recommended:**

  - `particlePatches`
    - type: one dimensional array of *(double)* values,
            repeating the following entries for each particle patch:
      - `numParticles`: number of particles in this patch
      - `numParticlesOffset`: offset within the one-dimensional records where
                              the first particle in this patch is stored
      - `offset`: n-values with positions where the particle patch begins; the
                  order of positions is given in component order
                  `x`[, `y`[, `z`]] of the species' `position` record and `n`
                  by the number of components of `position`
      - `extend`: n-values with extend of the particle patch; order and
                  `n` are defined as in `offset`
    - description: to allow post-processing, efficient checkpointing and
                   visualization tools to read records with the size of more
                   than the typical size of a local-node's RAM, this attribute
                   allows to sub-sort records that are close in the n-dimensional
                   `position` to ensure an intermediate level of data locality;
                   patches of particles must be hyperrectangles regarding
                   the `position` of the particles within; the union of all
                   particle patches must resemble all elements in the particle's
                   records


Domain-Specific Extensions
--------------------------

The base standard defined in this document is sufficient for describing
*general* mesh and particle based records.

For specific domains of engineering and science and to allow code
interoperability, specific conventions are necessary. As an example, some
records might be of distinct importance and should be read/written with exactly
the same name or are always required for, e.g., restarts and checkpoints.

Also additional meta information might be useful for publishing the data
created by a scientific instrument or simulation, e.g., the focal length
of a camera objective or the used algorithms in a specific simulation.
Even if they are not necessary for code-interoperability, an extension
can require additional information to describe the created data further.

The openPMD standard is therefore organized in the *base standard* and
*domain-specific extensions* (with a unique ID). In the current version of
the standard, using multiple extensions at the same time is discouraged.

Up to now, the following domain-specific naming conventions for have been
defined:

- **ED-PIC**: electro-dynamic/static particle-in-cell codes,
  see [EXT_ED-PIC.md](EXT_ED-PIC.md).

Extensions to similar domains such as fluid, finite-element or
molecular-dynamics simulations, CCD images or other particle and/or mesh-based
records can proposed for [future versions](CONTRIBUTING.md) of this document.
