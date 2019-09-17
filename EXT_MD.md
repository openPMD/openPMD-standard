Domain-Specific Naming Conventions for Molecular Dynamics Simulation Codes
=======================================================================

openPMD extension name: `MD`

VERSION: 0.0.1 (September 17th, 2019)

Introduction
------------

This extension is specifically designed for the molecular dynamics simulation codes.

The current version of this extension is suitable to allow the output of
arbitrary simulation codes to be post-processed and compared with common
tools and frameworks ([SIMEX](https://github.com/eucall-software/simex_platform)). Future versions will define a common set of required
records and further attributes.

The example data structure can be found [HERE](https://github.com/ejcjason/MDDomainExtension).

Root Group
---------------------------

### Additional Attributes for the `Root` group

The following additional attributes are defined in this extension.
The individual requirement is given in `scope`.

  - `forceField`
    - type: 1-dimensional array of N (string) elements, where N is the number of force fields (interatomic potentials) implemented in the simulation.
    - scope: *optional*
    - description: the methods implemented in the simulation to describe the force fields (interatomic potentials). See [Interatomic Potentials Repository](https://www.ctcms.nist.gov/potentials/) and [potential styles in LAMMPS](https://lammps.sandia.gov/doc/Commands_pair.html)
    - example values:
      - `eam/alloy`
      - `lj/cut 3.0`
      - ...
  - `forceFieldParameters`
    - type: 1-dimensional array of N (string) elements, where N is the number of force fields (interatomic potentials) implemented in the simulation.
    - scope: *optional*
    - description: the parameters specification for the `forceField` methods. See [Interatomic Potentials Repository](https://www.ctcms.nist.gov/potentials/) and [potential styles in LAMMPS](https://lammps.sandia.gov/doc/Commands_pair.html).
    - example values:
      - `pair_coeff * * 1 1`
      - `pair_coeff 1 1 Cu_mishin1.eam.alloy Cu`
      - ...

Observable Records
---------------------------

`observables` is an *optional* group that contains physical observables that are derived from the system state, i.e., thermodynamic information (e.g. temperature, energy, pressure). See [LAMMPS thermo_style command](https://lammps.sandia.gov/doc/thermo_style.html).

### Naming conventions

The naming conventions conforming the naming conventions for [Scalar, Vector and Tensor Records](https://github.com/openPMD/openPMD-standard/blob/latest/STANDARD.md#naming-conventions) in [openPMD base standard](https://github.com/openPMD/openPMD-standard/blob/latest/STANDARD.md).

- `scalar` record
  - type: *(any type)*
  - data set: `recordName` unique name in group `basePath` + `observables`
  - examples:
    - /data/observables/temperature
    - /data/observables/pressure

### Attributes for each `observable` record

The attributes of unit system for records should be included as defined in [openPMD base standard](https://github.com/openPMD/openPMD-standard/blob/latest/STANDARD.md#unit-systems-and-dimensionality)  .


Particle Records
---------------------------

### Additional Sub-Group for each Particle Species

`box` is an *optional* sub-group for each particle species to contain the information of the simulation box. 

### Attributes for Sub-Group `box`

The following attributes are defined in this extension.
If the `box` sub-group exists, the following attribute within it are required.
The individual requirement is given in `scope`. 

  - `dimension`
    - type: *(uint32)*
    - description: the spacial dimension **D** of the simulation box.
    - example values:
      - `2` 2D simulation box
      - `3` 3D simulation box
      - ...

  - `bounday`
    - type: array of *(string)* containing **D** elements, where **D** is the value of `dimension`.
    - description: the boundary condition of the box along each dimension. The allowed values in `boundary` are either **periodic** or **none**.
    - example values:
      - `["periodic","periodic","periodic"]`  periodic in all the three dimensions
      - `["none","periodic","periodic"]` periodic in only *y* and *z* dimensions

### Records for Sub-Group `box`

The following records are defined in this extension.
If the `box` sub-group exists, the following records within it are required.
The individual requirement is given in `scope`. 
  - `edge`
    - type: DxD array of *(floatX)*, where **D** is the value of `dimension`.
    - description: the edge vector of the simulation box in each dimension.
    - example values:
      - `[[1.,0.,0.],[0.,1.,0.],[0.,0.,1.]]` 3D cubic simulation box, Ax = (1.,0.,0.), Ay = (0.,1.,0.), Az = (0.,0.,1.)
      - `[[3.46,0.,0.],[1.73,2.997,0.],[0.,0.,10.]]` 3D cubic simulation box, Ax = (3.46,0.,0.), Ay = (1.73,2.997,0.), Az = (0.,0.,10.)
      - `[[1.,0.],[1.,1.]]` 2D rectangle simulation box, Ax = (1.,0.), Ay = (0.,1.)
  - `limit`
    - type: Dx2 array of *(floatX)*, where **D** is the value of `dimension`.
    - description: the starting and the ending of each edge vector.
    - example values:
      - `[[0.,300.],[0.,150.],[0.,180.]]`  A 3D box example: xlo = 0, xhi = 300, ylo = 0, yhi = 150, zlo = 0, zhi = 180 
      - `[[0.,300.],[15.,280.]]` A 2D box example: xlo = 0, xhi = 300, ylo = 15, yhi = 280
  - `unitSI`
    - type: *(float64)*
    - description: unit-conversion factor to convert simulation unit to SI units
    - example: `1.0e-10`