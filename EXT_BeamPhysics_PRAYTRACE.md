Additional definitions for photon raytracing for BeamPhysics Extension of the openPMD Standard
=========================================================================================================
openPMD extension name: `BeamPhysics`

Overview
--------

The `BeamPhysics` extension to the openPMD standard is meant for describing particles and fields commonly encountered in accelerator physics simulations.

How to Use this Extension
-------------------------

The `BeamPhysics` extension to the openPMD standard is indicated in a data file by the setting of the `openPMDextension` attribute:
```
  openPMDextension = BeamPhysics;SpeciesType
```

Note: The `SpeciesType` extension must be used when using the `BeamPhysics` extension.

Definitions
-----------

- **Lattice**: A **lattice** is the arrangement of elements in a machine such as a particle accelerator.

- **Lattice branches**: The lattices of some programs can contain multiple connected beam lines or rings. For example, an injection line connected to a storage ring connected to X-ray beam lines. Each line or ring is called a **branch**. In the above example, the injection line is one branch, the storage ring another branch, and each X-ray beam line is a branch.

- **Global coordinate system**: The **global** coordinate system is a coordinate system that is used to describe the position and orientation of machine elements in space. That is, the **global** coordinate system is fixed with respect to the building or room where the machine is placed independent of the machine itself.

- **Lattice coordinate system**: The curvilinear coordinate system whose "longitudinal" coordinate (**s**) typically runs through the nominal centers of the elements in the machine. The **lattice** coordinate system is often used to describe particle positions.

- **Macro-particle**: Macro-particles are simulation particles that represent multiple real particles. The number of real particles that a macro-particle represents affects the calculation of the field due to a macro-particle.

- **Particle coordinate system**: The coordinate system with respect to which particles positions and momenta are given. Some programs use the **global coordinate system** as the **particle coordinate system** while other programs use a coordinate system that is derived from the curvilinear **lattice coordinate system**.

- **Polar coordinates**: **Polar** coordinates are **(r, theta, phi)** where **r** is the radius, **theta** is the angle from the **z** or **s** axis, and **phi** is the projected azimuthal angle in the **(x, y)** plane.

- **Particle Group**: The **Particle Group** is a group for specifying a set of particles such as the particles in a bunch. The Beam Physics extension defines a standard for the  **Particle Group** as discussed below.

- **Reference Time**, **Reference Energy**, etc. Some programs have a reference from which various quantities are measured. For example, the **Reference Position** may be defined as the position of the center of the bunch under consideration.

Notes:
------

- When using the **lattice** coordinate system, the `position` coordinates are **(x, y, s)** or **(x, y, z)** where, nominally, **x** is the "horizontal" component, **y** is the "vertical" coordinate, and **s** or **z** is the lattice longitudinal coordinate.

Additional File Root Group (Path `/`) Attributes
------------------------------------------------

The following records are defined for the file root group.

- `fileType`
  - type: Optional *(string)*
  - description: The type of data being stored in the file. If present, must be set to `openPMD`. This attribute is used in systems where different data files can contain different types of data and allows for quick identification of the what type of data is in a given file.

- `latticeName`
  - type: Optional *(string)*
  - description: The name of the beamline.

- `latticeFile`
  - type: Optional *(string)*
  - description: The location of the root lattice file.
  
- `particlesPath`
  - type: Optional *(string)*
  - value: `rays/`
  - description: name of the particles path

Particle Group Standard
=======================

The **Particle Group** is a group for specifying a set of rays. Multiple **Particle Groups** can be defined in a file. The path for a **Particle Group** is given by the **basePath** and **particlesPath** attributes in the file root group as discussed in the base OpenPMD standard. For example, if **basePath** is  `/data/%T/`, and **ParticlesPath** is `particles/`, then **Particle Groups** paths would be of the form `/data/%T/particles/` where `%T` is an integer. EG: `/data/37/particles/`.

In case of photon raytracing extension, the default **particlesPath** is `rays/`. EG: `data/%T/rays/`.


`Particle Group` Attributes
--------------------------------

For each **particle group** the following attributes are defined:

- `numParticles`
  - type: Required *(int)*
  - description: The number of particles in the group.

- `speciesType`
  - type: Required *(string)*
  - value: `photon`
  - description: The name of the particle species. Species names must conform to the `SpeciesType` extension.

Per-Particle Records of the `Particle Group`
--------------------------------------------

The following records store data on a particle-by-particle basis.

- `momentum/`
  - type: Optional 3-vector *(real)*
  - description: The momentum vector of the particles relative to `momentumOffset`
  - components: (`x`, `y`, `z`).
  - true momentum = `momentum + momentumOffset`

-`id`
  - type: Optional *(int)*
  - description: Some programs give each particle an ID number. This field can be used to record that number. The `id` parameter is defined in the openPMD base standard and is just mentioned here for completeness sake. See the openPMD base standard for more details.

- `photonPolarizationAmplitude/`
  - type: Optional 2-vector *(real)*
  - description: Polarization amplitude of the photon.
  - components: (`x`, `y`).

- `photonPolarizationPhase/`
  - type: Optional 2-vector *(real)*
  - description: Polarization phase of the photon.
  - components: (`x`, `y`).

- `totalMomentum/`
  - type: Optional *(real)*
  - description: Total momentum relative to the totalMomentumOffset. That is, True total momentum = `totalMomentum + totalMomentumOffset`. Assumed zero if not present.

- `totalMomentumOffset/`
  - type: Optional *(real)*
  - description: Base total momentum from which `totalMomentum` is measured. That is, True total momentum = `totalMomentum + totalMomentumOffset`. Some programs will use `totalMomentumOffset/` to store the **reference momentum** in which case `totalMomentum` will then be the deviation from the referece.

- `particleStatus/`
    - type: Optional *(int)*
    - description: Integer indicating whether a particle is "alive" or "dead" (for example, has hit the vacuum chamber wall). A value of one indicates the particle is alive and any other value indicates that the particle is dead. Programs are free to distinguish how a particle died by assigning different non-unit values to `particleStatus`. For example, a program might want to differentiate between particles that are dead due to hitting the side walls versus reversing the direction longitudinally in an RF cavity.

- `position/`
    - type: Required 3-vector *(real)*
    - components: (`x`, `y`, `z`)
    - description: particle Position relative to the `positionOffset`.
    That is, true position relative to the coordinate origin = `position + positionOffset`.

- `positionOffset/`
    - type: Optional 3-vector *(real)*
    - description: Offset for each particle position component relative to the coordinate origin. Assumed zero if not present.
    - components: (`x`, `y`, `z`)

- `velocity/`
  - type: Optional 3-vector *(real)*
  - description: (`x`, `y`, `z`) velocity vector. Meant to be used for photons where using `momentum` is not appropriate.

- `wavelength/`
  - type: Optional *(real)*
  - description: Wavelength of the ray.

Non Per-Particle Records of the `Particle Group`
------------------------------------------------

The following possible records of the `Particle Group` are for specifying properties of the entire group of particles.

- `phaseSpaceFirstOrderMoment/`
  - type: Optional 6-vector *(real)*
  - description: First order beam moments of `(x, px, y, py, z, pz)`.

- `phaseSpaceSecondOrderMoment/`
  - type: Optional 6x6-matrix *(real)*
  - description: Second order beam moments of `(x, px, y, py, z, pz)`.

Particle Record Dataset Attributes
----------------------------------

The following attributes can be used with any dataset:

- `minValue`:
  - type: Optional *(real)*
  - description: Minimum of the data.

- `maxValue`:
  - type: Optional *(real)*
  - description: Maximum of the data.

External Mesh Fields Groups
===========================

The **external mesh field group** is a group for specifying electric and/or magnetic fields, due to a lattice element, at regularly spaced grid points. For example, the fields due to an RF cavity or the fields due to a DC magnet. Multiple **external mesh field groups** can be defined in a file. The path for a **external mesh field group** is given by the **externalFieldPath** in the file root group:
- `externalFieldPath`
  - type: Required if there are external mesh field group(s) *(string)*
  - description: Base path to the external mesh field groups. Use the **%T** construct if there are multiple meshes present.
  - example: `/ExternalFieldMesh/%T/`. Base paths to the external fields group, in this case, would be `/ExternalFieldMesh/01/`, etc.
  - example: `/ExternalFieldMesh/`. In this case since there is no `%T` in the name, there is only one external fields group.

Notes
-----

- AC fields can be described using complex numbers. The actual field is the real part of

    Z &ast; Exp[-2 pi i f &ast; (t - t0)]

where `Z` is the complex field, `f` is the Oscillation frequency, `t` is the time, and `t0` is a reference time.

Note: To ensure portability, complex data types are to be stored in a group with datasets (or constant record components if the values are constant) labeled "r" for the real part and "i" for the imaginary part. Exception: If the storage format supports native complex numbers, use the native storage. Note: HDF5 in particular does not have native support for complex numbers.

`External Fields Group` Attributes
----------------------------------

- `gridCurvatureRadius`
  - type: Optional *(real)*
  - description: Only used if using **(x, y, z)** field components. A zero value (the default) indicates that the grid is rectilinear. A non-zero value indicates that the grid is curved. The curvature is in the **(x, z)** plane with positive **x** pointing away from the center of curvature if `gridCurvatureRadius` is positive and vice versa for negative values. `gridCurvatureRadius` is the radius for the lines **x = 0** at constant **y**.

- `eleAnchorPt`
  - type: Required *(string)*
  - description: Point on the lattice element that the grid origin is referenced to. Possible values are: `beginning`, `center`, or `end`. The `beginning` point is at the entrance end of the element, the `center` point is at the center of the element and the `end` point is at the exit end of the element. All three points are on the reference orbit.

- `fieldScale`
  - type: Optional *(real)*
  - description: A scale factor that is used to scale the fields. Default is 1.

- `fundamentalFrequency`
  - type: Optional *(real)*
  - description: The fundamental RF frequency. Used for AC fields.

- `gridSpacing`
  - type: Required 3-vector *(real)*
  - description: Spacing between grid points.

- `gridLowerBound`
  - type: Required 3-vector *(int)*
  - description: Lower bound of the grid index. Note: The grid upper bound will be `gridLowerBound` + `gridSize` - 1.

- `gridSize`
  - type: Required 3-vector *(int)*
  - description: Size of the grid.

- `gridOriginOffset`
  - type: Required 3-vector *(real)*
  - description: distance from `eleAnchorPt` to the grid origin point.

- `harmonic`
  - type: Required *(int)*
  - description: Harmonic number of the fundamental frequency. A value of zero implies a DC field.

- `name`
  - type: Optional *(string)*
  - description: Name to be used to identify the grid.

- `RFphase`
  - type Required if `harmonic` is not zero *(real)*
  - description: Phase offset for oscillating fields. See the note above. Default is zero.

Per-grid `External Fields Group` Records
----------------------------------------

- `magneticField`
  - type: Optional 3-vector *(complex)*
  - description: Magnetic field. If the field is DC, only the real part should be nonzero. The components of `magneticField` may be either **(x, y, z)** representing `Bx`, `By`, and `Bz` or **(r, theta, z)** representing `Br`, `Btheta`, and `Bz`. Each component contains a 3-dimensional table giving the field on a grid. When using **(x, y, z)** components, each component contains a  **(x, y, z)** spatial grid. When using **(r, theta, z)** components, each component contains a **(r, theta, z)** spatial grid. In this case, if the grid size in the `theta` direction is 1, the field is taken to be axially symmetric.

- `electricField`
  - type: Optional 3-vector *(complex)*
  - description: Electric field. If the field is DC, only the real part should be nonzero. The components of `magneticField` may be either **(x, y, z)** representing `Ex`, `Ey`, and `Ez` or **(r, theta, z)** representing `Er`, `Etheta`, and `Ez`. Each component contains a 3-dimensional table giving the field on a grid. When using **(x, y, z)** components, each component contains a  **(x, y, z)** spatial grid. When using **(r, theta, z)** components, each component contains a **(r, theta, z)** spatial grid. In this case, if the grid size in the `theta` direction is 1, the field is taken to be axially symmetric.
