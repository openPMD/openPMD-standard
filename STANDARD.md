The openPMD Standard
====================

VERSION: **1.1.0** (Feburary 6th, 2018)

Conventions Throughout these Documents
--------------------------------------

The keywords "must", "must not", "required", "shall", "shall not", "should",
"should not", "recommended",  "may", and "optional" in this document are to be
interpreted as described in [IETF RFC 2119](https://datatracker.ietf.org/doc/html/rfc2119).

All `keywords` in this standard are case-sensitive.

The naming *(floatX)* without further specification is used if the implementor
can choose which kind of floating point precision shall be used
(e.g. *(float16)*, *(float32)*, *(float64)*, *(float128)*, etc.).
The naming *(uintX)* and *(intX)* without further specification is used if the
implementor can choose which kind of (un)signed integer type shall be used
(e.g. *(int32)*, *(uint64)*, etc.).
The naming for the type *(string)* refers to fixed-length, plain ASCII encoded
character arrays since they are the only ones that are likely to propagate
through all file-format APIs and third-party programs that use them.

Sometimes brackets `<Name>` are used for keywords while the `<>` only indicate
the keyword is required (but the `<>` itself shall not be written).
Accordingly, optional keywords and options are indicated via square brackets
`[Name]`.


The Versions of this Standard
-----------------------------

Versions of the standard allow codes and implementors to easily differentiate
between new updates that are incorporated.

The full version number is always used in format `<MAJOR>.<MINOR>.<REVISION>` .

Improvements will be sought to be backwards compatible, if that is not
possible then changes in the major version of this standard indicate
incompatibility.
Minor version updates instead need to be backwards compatible and should for
example only add new (ideally optional or recommended) keywords.
Revisions are reserved for typos and clarification in the standard (but not
for changes in keywords).


Hierarchy of the Data File
--------------------------

For simplicity, we call the storage concept of a specific data format that implements the openPMD hierarchy "files", even if they are implemented in-memory or by other means.

The used hierarchical data format must provide the capability to

  - create groups and sub-groups (in-file directories)
  - create multi-dimensional, homogeneous array-based data structures

while allowing for each of those to assign

  - multiple, distinct attributes
    (basic and array floating/integer types, strings)
  - with platform-independent representation.

We define the following placeholders and reserved characters:

  - `/`: separator of groups
  - `%T`: an iteration (unsigned integer type,
                        same range as a 64bit unsigned integer).

**Paths** to **groups** end on `/`, e.g., `/mySubGroup/` and **data sets** end
without a `/`, e.g., `dataSet` or `/path/to/dataSet`.

Each file's *root* group (path `/`) must at least contain the attributes:

  - `openPMD`
    - type: *(string)*
    - description: (targeted) version of the format in "MAJOR.MINOR.REVISION",
                   see section "The versions of this standard",
                   minor and revision must not be neglected
    - example: `1.1.0`

  - `basePath`
    - type: *(string)*
    - description: a common prefix for all data sets and sub-groups of a
                   specific iteration;
                   this string only indicates *how* the data is stored,
                   to create a real path from it replace all occurrences
                   of `%T` with the integer value of the iteration, e.g.,
                   `/data/%T` becomes `/data/100`
    - allowed values:
      - see *Iterations and Time Series* below
      - for `fileBased` and `groupBased`, this is fixed to `/data/%T/`
      - for `variableBased` this is fixed to `/data/`
    - note: all the data that is formatted according to the present
      standard (i.e. both the meshes and the particles) is to be
      stored within a path of the form given by `basePath` (e.g. in
      the above example, the data will be stored within the path `/data/100/`).
      If, for various reasons, a user wants to store *additional
      data* that is not (or cannot be) formatted according to the
      present standard (e.g. fields on an unstructured mesh),
      this can be done be storing this data within a path that *is not*
      of the form given by `basePath` (e.g. `/extra_data`). In this
      way, the openPMD data readers will not parse this additional data.

The following attribute is *optional* in each each file's *root* group
(path `/`) and indicates if a file also follows an openPMD extension
(see: *Domain-Specific Extensions*) on top of the base standard. It is
*required* to set them if one wants to declare an openPMD extension.

  - `openPMDextension`
    - type: *(string)*
    - description: the unique openPMD extension name of applied extensions on
                   top of the openPMD base standard
                   (see: *Domain-Specific Extensions*);
                   multiple extensions can be activated at the same time and
                   must appear as semicolon-separated list
    - note: do not create this attribute if no extension is used
    - note: if only one extension is used at a time, the value for
            `openPMDextension` is simply the name of the extension
    - examples:
      - `ED-PIC`: the base standard and the extension with name `ED-PIC` apply
                  for the file
      - `ED-PIC;SpeciesType`: the base standard and the extensions `ED-PIC` and
                              `SpeciesType` are used

The following attributes are *optional* in each each file's *root* group
(path `/`) and indicate if a file contains mesh and/or particle records. It is
*required* to set them if one wants to store mesh and/or particle records.

  - `meshesPath`
    - type: *(string)*
    - description: path *relative* from the `basePath` to the mesh records
    - example: `meshes/`
    - note: if this attribute is missing, the file is interpreted as if it
      contains *no mesh records*! If the attribute is set, the group behind
      it *must* exist!

  - `particlesPath`
    - type: *(string)*
    - description: path *relative* from the `basePath` to the groups for each
                   particle group and the records they include
    - example: `particles/`
    - note: if this attribute is missing, the file is interpreted as if it
      contains *no particle records*! If the attribute is set, the group behind
      it *must* exist!

It is *recommended* that each file's *root* group (path `/`) further
contains the attributes:

  - `author`
    - type: *(string)*
    - description: author and contact for the information in the file
    - example: `Axel Huebl <a.huebl@hzdr.de>`

  - `software`
    - type: *(string)*
    - description: the software/code/simulation that created the file
    - example: `PIConGPU`, `Warp`

  - `softwareVersion`
    - type: *(string)*
    - description: the version of the software/code/simulation that created the
                   file
    - example: `1.2.1`, `80c7551`, `rev42`

  - `date`
    - type: *(string)*
    - description: date of creation in format "YYYY-MM-DD HH:mm:ss tz"
    - example: `2015-12-02 17:48:42 +0100`

It is *optional* that each file's *root* group (path `/`) further contains
the attributes:

  - `softwareDependencies`
    - type: *(string)*
    - description: dependencies of `software` that were used when
                   `software` created the file,
                   semicolon-separated list
    - examples:
      - `gcc@5.4.0;boost@1.66.0;nvcc@9.1;python@3.6;adios@1.13;hdf5@1.8.17`
      - a long-time archived container image: `registry.example.com/user/repo:version`

  - `machine`
    - type: *(string)*
    - description: the machine or relevant hardware that created the file;
                   as semicolon-separated list if needed
    - example: `summit-ornl` (HPC cluster),
               `pco.pixelfly-usb` (scientific 14bit CCD camera)

Each group and data set may contain the attribute **comment** for general
human-readable documentation, e.g., for features not yet covered by the
standard:

  - `comment`
    - type: *(string)*
    - description: an arbitrary comment
    - example: `After each time step we randomly removed 5 particles.`


Iterations and Time Series
--------------------------

Iterations can be encoded in either the file name of each individual files, in groups of the same file, or in data sets & attributes (with supported data formats).
(Here, an *iteration* might refer to a single measurement or simulation cycle.)

The chosen style shall not vary within a related set of iterations.

Each file's *root* group (path `/`) must further define the attributes:

  - `iterationEncoding`
    - type: *(string)*
    - description: whether other iterations of this series, from the
                   file-format's API point of view, are encoded in the same file
                   or whether another `open/close` call is necessary to access
                   other iterations
    - allowed values:
      - `fileBased` (multiple files; one iteration per file)
      - `groupBased` (one file; iterations use groups in that file)
      - `variableBased` (one file; if the data format supports to store multiple iterations in the same variables and attributes)

  - `iterationFormat`
    - type: *(string)*
    - description: a well-defined string with the iteration `%T` placeholder
                   defining either the series of files (`fileBased`) or the
                   series of groups within a single file (`groupBased`)
                   from which the iteration can be extracted;
                   for `fileBased` formats the iteration must be included
                   in the file name;
                   the format depends on the selected `iterationEncoding` method
    - note: it is not required that every openPMD iteration contains an update for each declared openPMD record (see below)
    - examples:
      - for `fileBased`:
        - `filename_%T.h5` (without file system directories)
      - for `groupBased`: (fixed value)
        - `/data/%T/` (must be equal to and encoded in the `basePath`)
      - for `variableBased`: (fixed value)
        - data-format internal convention
        - *slowest varying index* of data

### `variableBased` Encoding of Iterations

In order to correlate openPMD iterations with an index of data-format internal updates/steps or an index in the slowest varying dimension of an array, the iteration base path (default: path `/data`) must contain an additional variable once `variableBased` is chosen for `iterationEncoding`:

  - `snapshot`
    - type: 1-dimensional array containing N *(int)* elements, where N is the number of updates/steps in the data format
    - description: for each update/step in a data format, this variable needs to be updated with the corresponding openPMD iteration.
    - note: in some data formats, updates/steps are absolute and not every update/step contains an update for each declared openPMD record
    - advice to implementers: an openPMD iteration might be spread over multiple updates/steps, but not vice versa.
                              In such a scenario, an individual openPMD record's update/step must appear exactly once per iteration.

Notes:

* In implementations without support for storing multiple versions of datasets/attributes, the variable-based encoding of iterations may still be used for storage of a single iteration.
  In that case, the `snapshot` attribute is optional and defaults to zero (0).
* In implementations with support for storing multiple versions of datasets/attributes, the `snapshot` attribute may optionally be used in group-based encoding to associate openPMD iterations with IO steps.
  In group-based encoding, there is still only one instance of this attribute globally (`/data/snapshot`).
  In consequence, the attribute shall only be written if modifiable attributes are supported by the implementation.


Required Attributes for the `basePath`
--------------------------------------

In addition to holding information about the iteration, each series of files  (`fileBased`), series of groups (`groupBased`) or internally encoded iterations (`variableBased`) should have attributes that describe the current time and the last step.

 - `time`
   - type: *(floatX)*
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
   - type: *(floatX)*
   - description: the latest time step (that was used to reach this iteration).
                  This is needed at the iteration level, since the time step
                  may vary from iteration to iteration in certain codes.

In addition, the following attribute is *recommended* (see the section
on Unit Systems and Dimensionality, further below):

 - `timeUnitSI`
    - type: *(float64 / REAL8)*
    - description: a conversation factor to convert `time` and `dt` to `seconds`
    - example: `1.0e-16`


Scalar, Vector and Tensor Records
---------------------------------

In general, all data sets shall be stored as homogeneous arrays or matrices
respectively, depending on the (spatial) dimensionality of the record they
represent.

Records with only a scalar component are stored in a data set with the same name
as the record. Vector and tensor records shall be represented component-wise as
a *collection of individual scalar data sets* using a common sub-group that is
equal to the record name.

We refer to the scalar record itself and the vector sub-group as `record`, to
the data sets in the vector sub-group as `components`. For scalar records,
the `record` is the `component` (and vice versa).

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
                `particlesPath` + `particleName`
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


Mesh Based Records
------------------

Mesh based records such as discretized fields shall be represented as homogeneous records, usually in a N-dimensional matrix.

### Required Attributes for each `mesh record`

The following attributes must be stored additionally with each `mesh record`
(which is a data set attribute for `scalar` or a group attribute for `vector`
meshes):

  - `geometry`
    - type: *(string)*
    - description: geometry of the mesh of the mesh record, right-handed
                   coordinate systems are imposed
    - allowed values:
      - `cartesian`: standard Cartesian mesh
      - `thetaMode`: regularly-spaced mesh in the r-z plane, with
                     Fourier decomposition in the azimuthal direction (See
                     [doi:10.1016/j.jcp.2008.11.017](http://dx.doi.org/10.1016/j.jcp.2008.11.017))
                     In this case, the mesh arrays are stored as a
                     three-dimensional record where the last axis corresponds
                     to the `z` direction, the second axis correspond to the
                     `r` direction and where the first axis corresponds to
                     the azimuthal mode. (This last axis has length `2m-1`,
                     where `m` is the number of modes used. By convention,
                     this first stores only the real part of the mode `0`, then
                     the real part of the mode `1`, then the imaginary part
                     of the mode `1`, then the real part of the mode `2`,
                     then the imaginary part of the mode `2`, etc.)
      - reserved: `cylindrical`, `spherical`
      - `other`

  - `geometryParameters`
    - type: *(string)*
    - description: additional parameters for the geometry, separated by a `;`,
                   this attribute is required when `geometry` is
                   `thetaMode`,  but can be omitted if geometry is `cartesian`
    - examples:
      - for `thetaMode` geometry:
        - `m=3;imag=+` (3 *modes* and using a `+` sign for the definition of
                        the *imaginary* part)
```math
    E_z = \mathcal{R}(\tilde{E}_{z,0}) + \sum_{l=1}^{m} \mathcal{R}(\tilde{E}_{z,l}) \cdot \cos(l \Theta) {\color{red}+} \mathcal{I}(\tilde{E}_{z,l}) \cdot \sin(l \Theta)$
```

  - `axisLabels`
    - type: 1-dimensional array containing N *(string)*
            elements, where N is the number of dimensions in the simulation
    - description: this attribute assigns human-readible labels for the
                   indices `i`, `j`, `k`, etc. denoting the axes of a mesh
                   `A_{i,j,k}`
    - advice to implementors:
      - dimensions shall be ordered from slowest to fastest varying index when
        accessing the mesh contiguously (as 1D flattened logical memory)
      - if you access a ND array in C-like languages, a matrix `A[i,j,k]` will
        have its first index as the slowest varying index (e.g. `i`)
      - if you access a ND array Fortran-like, a matrix `A(i,j,k)` will have
        its last index as the slowest varying index (e.g. `k`)
    - examples:
      - 3D `cartesian` mesh accessed in C-like as `A[z,y,x]` will have `z` as
        its slowest varying index name and `axisLabels`: `("z", "y", "x")`
      - 3D `cartesian` mesh accessed in C-like as `A[x,y,z]` will have `x` as
        its slowest varying index name and `axisLabels`: `("x", "y", "z")`
      - 2D `cartesian` mesh accessed in Fortran-like as `A(x,y)` will have `y` as
        its slowest varying index name and `axisLabels`: `("y", "x")`
      - `thetaMode` accessed Fortran-like `A(r,z)`, `axisLabels`: `("z", "r")`

  - `gridSpacing`
    - type: 1-dimensional array containing N *(floatX)*
            elements, where N is the number of dimensions in the simulation
    - description: spacing of the grid points along each dimension (in the
                   units of the simulation); this refers to the spacing of the
                   actual record that is written to the file, not that of the
                   simulation grid. (The record written may be down-sampled, as
                   compared to the simulation grid).
    - advice to implementors: the order of the N values must be identical to
                              the axes in `axisLabels`

  - `gridGlobalOffset`
    - type: 1-dimensional array containing N *(float64 / REAL8)*
            elements, where N is the number of dimensions in the simulation
    - description: start of the current domain of the simulation (position of
                   the beginning of the first cell) in simulation units
    - advice to implementors: the order of the N values must be identical to
                              the axes in `axisLabels`

    - example: `(0.0, 100.0, 0.0)` or `(0.5, 0.5, 0.5)`

In addition, the following attribute is *recommended* (see the section
on Unit Systems and Dimensionality, further below):

  - `gridUnitSI`
    - type: 1-dimensional array containing N *(float64 / REAL8)*
            elements, where N is the number of dimensions in the simulation.
            The order of the N values must be identical to the axes in `axisLabels`.
    - description: unit-conversion factor to multiply each value in
                   `gridSpacing` and `gridGlobalOffset`, in order to convert
                   from simulation units to SI units
    - example: `(1.0e-9, 1.0e-9, 1.0e-6)`

  - `gridUnitDimension`
    - type: 1-dimensional array of 7 N *(float64 / REAL8)*
            elements, where N is the number of dimensions in the simulation.
            The order of the N 7-value arrays must be identical to the axes in `axisLabels`.
    - description: powers of the 7 base measures characterizing the
            grid axes's dimensions (length L, mass M, time T,
            electric current I, thermodynamic temperature theta,
            amount of substance N, luminous intensity J)
    - note: this is similar to `unitDimension`, but applies to each axis
        The 7 numbers characterizing the dimension of an axis are stored
        contiguously in this 1D array.
    - examples (with `L`, `M` and `T` as defined in `unitDimension`)
        - For a 2D spatial grid (`L=1`), store array
        `(1., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0.)`
        - For a 2D phase space (Dimension "L" along the first axis
        and "L*M/T" along the second axis), store array
        `(1., 0., 0., 0., 0., 0., 0., 1., 1., -1., 0., 0., 0., 0. )`


The following attributes must be stored with each `scalar record` and each
*component* of a `vector record`:

  - `position`
    - type: 1-dimensional array of N *(floatX)* where N is the number of
            dimensions in the simulation.
    - range of each value: `[ 0.0 : 1.0 )`
    - description: relative position of the component on the current element of
                   the mesh/grid/node/cell/voxel;
                   `0.0` means at the beginning of the mesh element and `1.0` is
                   the beginning of the next mesh element;
                   the same dimensionality N as in `gridSpacing` and
                   `gridGlobalOffset`

### Optional Attributes for each `mesh record`

  - `particleList`
    - type: *(string)*
    - description:
        this adds a hint to analysis tools that this mesh record is related to one or more particle groups;
        multiple particle groups can be indicated at the same time and must appear as semicolon-separated list
    - note:
        this is often used in graphical user-interfaces to group projected meshes of particle distributions in a user-friendly manner;
        examples are particle densities and phase space projections
    - note:
        when reading this back, the particle groups listed here might not be present in some steps or are even skipped in the whole openPMD series by the writer
    - examples:
      - `electrons`: indicates this field is related to the `particle group` named `electrons`
      - `electrons;hydrogen;carbon`: indicates this field is related to the `particle group`s named `electrons`, `hydrogen` and `carbon`


Particle Records
----------------

Each `particle group` shall be represented as a group `particleName/` that
contains all its records. Particles records are generally represented in
one-dimensional contiguous records, where the n-th entry in
`particleName/recordNameA` and the n-th entry in `particleName/recordNameB`
belong to the same particle.

### Naming conventions

As with general `vector` records, compound particle vector records
are again split in scalar components that are stored in a common
sub-group `particleName/recordName/`
(see: *Scalar, Vector and Tensor Records*). Also, record components that are
constant for all particles of a group (and iteration) can be replaced with a
short-hand notation (see: *Constant Record Components*).

### Records for each `Particle Group`

  - `id`
    - type: *(intX)*
    - scope: *optional*
    - description: a globally-unique identifying integer for each particle,
                   that can be used to, e.g., track particles. This
                   identifying integer should be unique within the
                   simulation; in particular, even among different particle
                   groups, two particles should not have the same id unless
                   they are truly the same particle.
                   Also, when a particle exits the simulation box, its
                   identifying integer should not be reassigned to a new
                   particle.
    - advice to implementors: it is recommended to use the type
                              *(uint64 / UNSIGNED8)*

  - `position/` + components such as `x`, `y`, `z`
    - type: each component in *(floatX)* or *(intX)* or *(uintX)*
    - scope: *required*
    - description: component-wise position of a particle, relative to
                   `positionOffset`
    - example: use only `x` and `y` in 2D, use `x` in 1D

  - `positionOffset/` + components such as `x`, `y`, `z`
    - type: each component in *(floatX)* or *(intX)* or *(uintX)*
    - scope: *required*
    - description: an offset to be added to each element of `position`
    - rationale: for precision reasons and visualization purposes, it is
                 often more useful to define all positions of an iteration
                 relative to an offset; extensions might use this record to
                 define relations to mesh records
    - advice to implementors: to reduce read/write accesses and memory
                              consumption, it is often useful to implement this
                              with `constant record components`
    - example: reading example (with h5py) in Python:
```python
def is_const_component(record_component):
    return ("value" in record_component.attrs.keys())

def get_component(group, component_name):
    record_component = group[component_name]
    # `default` handles the case where conversion to SI is not provided
    unitSI = record_component.attrs.get("unitSI", default=1.)

    if is_const_component(record_component):
        return record_component.attrs["value"], unitSI
    else:
        return record_component.value, unitSI

f = h5py.File('example.h5')
species = f["<path_to_species_group>"]

position_x_relative, unitXRel = get_component(species, "position/x")
position_x_offset, unitXOff = get_component(species, "positionOffset/x")

x = position_x_relative * unitXRel + \
    position_x_offset * unitXOff
```


### Sub-Group for each `Particle Group`

Within each particle groups' group the sub-group `particlePatches` alongside
its records, as mentioned above, is *recommended* for parallel
post-processing. The idea is to logically order the 1D arrays of attributes into
local patches of particles that can be read and processed in parallel.

To allow efficient parallel post-processing, checkpointing and visualization
tools to read records with a size of more than the typical size of a
local-node's RAM, the records in this sub-group allow to sub-sort particle
records that are close in the n-dimensional `position` to ensure an
intermediate level of data locality. Patches of particles must be
hyperrectangles regarding the `position` (including `positionOffset`s as
described above) of the particles within. The union of all particle patches
must correspond to the complete particle's records.

For the creation of those particle patches, already existing information in
memory layouts such as linked lists of particles or per-node domain
decompositions can be reused. The most trivial (serial) implementation of a
particle patch would be the description of a single patch spaning the whole
spatial domain of particles.

If the `particlePatches` sub-group exists, the following records within it
are *required* and the entries in each record are stored in a per particle
patch order:

  - `numParticles`
    - type: *(uint64 / UNSIGNED8)*
    - description: number of particles in this patch
    - examples:
      - serial, one patch: the global number of all particles
      - parallel, e.g. MPI: the number of particles of a MPI rank;
                            the sum of all entries in this record is the global
                            number of particles

  - `numParticlesOffset`
    - type: *(uint64 / UNSIGNED8)*
    - description: offset within the one-dimensional records of the particle
                   species where the first particle in this patch is stored
    - examples:
      - serial, one patch: `0`
      - parallel, e.g. MPI: the number of particles of all MPI ranks' patches
                            that were stored before this one

  - `offset/` + components such as `x`, `y`, `z`
    - type: each component in *(floatX)* or *(intX)* or *(uintX)*
    - description: absolute position (`position` + `positionOffset` as defined
                   above) where the particle patch begins:
                   defines the (inclusive) lower bound with positions that are
                   associated with the patch;
                   the same requirements as for regular record components apply

  - `extent/` + components such as `x`, `y`, `z`
    - type: each component in *(floatX)* or *(intX)* or *(uintX)*
    - description: extent of the particle patch; the `offset` + `extent` must
                   be larger than the maximum absolute position of particles in
                   the patch as the exact upper bound of position `offset` +
                   `extent` is excluded from the patch;
                   the same requirements as for regular record components apply

### Optional Attributes for each `Particle Group`

  - `meshList`
    - type: *(string)*
    - description:
        this adds a hint to analysis tools that this particle group is related to one or more mesh records;
        multiple mesh records can be indicated at the same time and must appear as semicolon-separated list
    - note:
        this is often used in graphical user-interfaces to group meshes that are sampled with particles in a user-friendly manner;
        examples are particle probes as well as non-uniform and curved samples from large meshes
    - note:
        when reading this back, the mesh records listed here might not be present in some steps or are even skipped in the whole openPMD series by the writer
    - examples:
      - `E`: indicates this particle group is related to the `E` mesh record
      - `E;B;j`: indicates this particle group is related to the `E`, `B` and `j` mesh records


Unit Systems and Dimensionality
-------------------------------

All datasets and attributes can be written in arbitrary units, in openPMD.
Typically, this will be the unit system adopted internally by the
software that writes openPMD (e.g. the unit system adopted internally
by a physics simulation code), in order to avoid a reduction in performance
associated with unit conversion during the write process.

However, for each dataset and attribute, it is **very strongly** recommended to
provide the conversion factor from the chosen unit system to the International
System of Units (SI). (See the description of the attributes `timeUnitSI`,
`gridUnitSI` and `unitSI`, in the present document.) This allows
the reading softwares to convert the datasets to units that any user can
understand, without requiring them to know the chosen unit system.

In some exceptional cases, the software that produces the openPMD data may
not have a well-defined conversion to the SI system. (This is the case for
instance for plasma simulation codes where quantities are scaled with respect to
a given plasma density, and where this density could have any value.)
In this case, the attributes `timeUnitSI`, `gridUnitSI` and `unitSI` can
be omitted. However, note that, in this case, the reading softwares will
not be able to tell the user in which units the data is, and this will require
the user to have in-depth knowledge of the chosen unit system.
**Therefore, unless there is a very good reason to omit the conversion factors
to the SI system, it is very strongly recommended to include them.**

For each `mesh` or `particle` `record` and their `components` the following
attributes are defined:

### Recommended for each `Record Component`

Reminder: for scalar records the `record` itself is also the `component`.

  - `unitSI`
    - type: *(float64 / REAL8*)
    - description: a conversation factor to multiply data with to be
                   represented in SI
    - rationale: can also be used to scale a dimension-less `component`
    - rationale: if the `component` is dimension-less and in the right scaling
                 or already in SI, e.g., an index counter, set this to `1.0`
    - example: `2.99792e8`

### Required for each `Record`

  - `unitDimension`
    - type: array of 7 *(float64 / REAL8)*
    - description: powers of the 7 base measures characterizing the record's
                   unit in SI (length L, mass M, time T, electric current I,
                   thermodynamic temperature theta, amount of substance N,
                   luminous intensity J)
    - rationale: this allows to implement automated record detection,
                 identification and compatibility checks, independent of
                 specific names or string representations;
                 does *not* represent if the record is a 1, 2 or 3D array
    - rationale: if the `record` is dimension-less, such as an index, set this
                 to `(0., 0., 0., 0., 0., 0., 0.)`
    - advice to implementors: implement a lookup table for the most common
                              quantities/units in your simulation, e.g.,
                              electric field strengths, mass, energy, etc.
                              in the respect of the power of the base units
                              given here
    - examples:
      - "m / s" is of dimension `L=1` and `T=-1`,
        store array `(1., 0., -1., 0., 0., 0., 0.)`
      - "N = kg * m / s^2", store array `(1., 1., -2., 0., 0., 0., 0.)`
      - magnetic field: "T = kg / (A * s^2)", store array
                        `(0., 1., -2., -1., 0., 0., 0.)`
      - electric field: "V/m = kg * m / (A * s^3)", store array
                        `(1., 1., -3., -1., 0., 0., 0.)`

  - `timeOffset`
    - type: *(floatX)*
    - description: the offset between the time at which this record is
                   defined and the `time` attribute of the `basePath` level.
                   This should be written in the same unit system as `time`
                   (see `basePath`; i.e., it should be multiplied by
                   `timeUnitSI` to get the actual time in seconds.)
    - example: In a staggered PIC code, if `time` is chosen to correspond to
               the time at which the electric field is defined, and if `dt`
               is e.g. 1.e-5, `timeOffset` would be 0.5e-5 for the magnetic
               field and 0. for the electric field.


Constant Record Components
--------------------------

For records components that are constant (for a certain iteration), replacing
the record component with a group attribute of the same name is possible, as
described in the following paragraphs. For scalar records, the component is as
usual the record itself.

Replacing a record component with a constant value for all values on the mesh
or for all particles respectively works as follows:
The record's *data set* `<componentName>` must be replaced with an empty
*sub-group* `<componentName>/` that hosts the group-attributes `value` and
`shape`.

`shape` is a 1-dimensional array of `N` *(uint64)* elements, where `N` is the
number of dimensions of the record. It contains the number of elements of each
dimension that are replaced with a constant value. For `mesh` based records,
the order of the `N` values must be identical to the axes in `axisLabels`.

Other required attributes that where previously stored on the *data set* need
to be added to the new sub-group as well.

Examples:
  - the `mesh` record for a magnetic field `B` is constant for `B.x` and `B.y`:
    - `<basePath><meshesPath>B/`: record group with standard attributes, e.g.,
                                  `unitDimension`
      - `x/`: sub-group with attributes `value=<C0>`, `shape=array(..., ...)`
              and standard attributes, e.g., `unitSI`
      - `y/`: sub-group with attributes `value=<C1>`, `shape=array(..., ...)`
              and standard attributes, e.g., `unitSI`
      - `z`: data set with standard attributes, e.g., `unitSI`
  - the `mesh` record for a temperature field `T` is constant
    - `<basePath><meshesPath>T/`: record group with attribute `value=<C0>`,
                                  `shape=array(...)` and standard attributes,
                                  e.g., `unitDimension` and `unitSI`
  - the `particle` record `charge` for the particle species `electrons` is
    constant
    - `<basePath><particlesPath>electrons/charge/`: record group with attribute
                                                    `value=-1.0`,
                                                    `shape=array(...)` and
                                                    standard attributes, e.g.,
                                                    `unitSI=1.60217657e-19` and
                                                    `unitDimension=array(...)`


Domain-Specific Extensions
--------------------------

The base standard defined in this document is sufficient for describing
*general* mesh and particle based records.

For specific domains of engineering and science and to allow code
interoperability, specific conventions are necessary. As an example, some
records may be of distinct importance and should be read/written with exactly
the same name or are always required for, e.g., restarts and checkpoints.

Also additional meta information may be useful for publishing the data
created by a scientific instrument or simulation, e.g., the focal length
of a camera objective or the used algorithms in a specific simulation.
Even if they are not necessary for code-interoperability, an extension
can require additional information to describe the created data further.

The openPMD standard is therefore organized in the *base standard* and
*domain-specific extensions* (with a unique ID). In the current version of
the standard, using multiple extensions at the same time is discouraged.

Up to now, the following domain-specific naming conventions for have been
defined:

- **BeamPhysics**: particle beams, photons, and external fields for accelerator physics,
  see [EXT_BeamPhysics.md](EXT_BeamPhysics.md).
- **ED-PIC**: electro-dynamic/static particle-in-cell codes,
  see [EXT_ED-PIC.md](EXT_ED-PIC.md).
- **ParticleWeighting**: conventions for macroparticles,
  see [EXT_ParticleWeighting.md](EXT_ParticleWeighting.md).
- **SpeciesType**: naming lists for particle species,
  see [EXT_SpeciesType.md](EXT_SpeciesType.md).
- **Wavefront**: fields for coherent wavefront propagation codes,
  see [EXT_Wavefront.md](EXT_Wavefront.md).
- **LaserEnvelope**: envelope of a laser pulse,
  see [EXT_LaserEnvelope.md](EXT_LaserEnvelope.md).

Extensions to similar domains such as fluid, finite-element or
molecular-dynamics simulations, CCD images or other particle and/or mesh-based
records can proposed for [future versions](CONTRIBUTING.md) of this document.


Data-Format Specific Conventions
--------------------------------

Some low-level data formats and libraries need slight additional conventions to make best use of openPMD.
Individual implementation notes are described in:

- **ADIOS**: see [FORMAT_ADIOS.md](FORMAT_ADIOS.md)
- **HDF5**: see [FORMAT_HDF5.md](FORMAT_HDF5.md)
- **JSON**: see [FORMAT_JSON.md](FORMAT_JSON.md)


Implementations
---------------

### Writer

The created files must pass the provided validator/checker scripts.
The scripts can not check 100% of the standard, the words written in the
standard shall be checked manually for parts not covered by these when in
doubt.

#### Reader

Reader implementations that officially want to add support for the openPMD
standard must fulfill the following requirements:

- version checking:
  - description: in case the reader only supports a specific version of the
                 standard, the reader must abort on missing implementations
                 of major version changes;
                 see section "The versions of this standard"

- warnings and further constrains:
  - if the provided validator/checker scripts throw warnings (and the
    file does not violate the standard due to missing coverage of a certain
    critera in the scripts) the reader must be able to read the file
  - rationale: if you are creating a script specifically for a certain
               processing workflow and do have stronger constrains, e.g., about
               present records or extensions, you must explicitly state this in
               your reader to be allowed to reject a file even if it fulfills
               the standard, else the reader must process the file correctly

- errors:
  - if the provided validator/checker scripts throw errors (and/or additional
    violations of the standard are present in the file due to missing coverage
    of a certain criteria in the scripts), the reader should not accept the
    file
  - rationale: you are free to "try to parse" a file that is not valid openPMD
               but it is generally considered bad practice, leads to security
               problems, uncertainties in interpretation, blowed up code, etc.;
               we strongly recommend to reject invalid files that claim to
               fulfill the standard (e.g., with an error message pointing to
               the validator/checker scripts)
