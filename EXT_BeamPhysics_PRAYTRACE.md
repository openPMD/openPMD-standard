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

### Scope

Required

- `position/`
	- `x`, `y`, `z`
- `direction/`
	- `x`, `y`, `z`
- `photonSPolarizationAmplitude/`
	- `x`, `y`, `z`
- `photonSPolarizationPhase/`
	- `x`, `y`, `z`
- `photonPPolarizationAmplitude/`
	- `x`, `y`, `z`
- `photonPPolarizationPhase/`
	- `x`, `y`, `z`
- `wavelength`
	
### Attributes

- `momentum/`
  - type: Optional 3 x N-vector *(real)*
  - description: The momentum vector of the particles relative to `momentumOffset`
  - components: numParticles columns and rows of (`x`, `y`, `z`).
  - true momentum = `momentum + momentumOffset`

-`id`
  - type: Optional 1 x N-vector *(int)*
  - description: Some programs give each particle an ID number. This field can be used to record that number. The `id` parameter is defined in the openPMD base standard and is just mentioned here for completeness sake. See the openPMD base standard for more details.

- `photonSPolarizationAmplitude/`
  - type: Required 3 x N-vector *(real)*
  - description: Electric field amplitude of s- polarized photons.
  - components: numParticles columns and rows of (`x`, `y`, `z`).

- `photonSPolarizationPhase/`
  - type: Required 3 x N-vector *(real)*
  - description: Electric field phase of s- polarized photons.
  - components: numParticles columns and rows of (`x`, `y`, `z`).

- `photonPPolarizationAmplitude/`
  - type: Required 3 x N-vector *(real)*
  - description: Electric field amplitude of p- polarized photons.
  - components: numParticles columns and rows of (`x`, `y`, `z`).

- `photonPPolarizationPhase/`
  - type: Required 3 x N-vector *(real)*
  - description: Electric field phase of p- polarized photons.
  - components: numParticles columns and rows of (`x`, `y`, `z`).

- `particleStatus/`
    - type: Optional 1 x N-vector *(int)*
    - description: Integer indicating whether N-th particle is "alive" or "dead" (for example, has hit the vacuum chamber wall). A value of one indicates the particle is alive and any other value indicates that the particle is dead. Programs are free to distinguish how a particle died by assigning different non-unit values to `particleStatus`. For example, a program might want to differentiate between particles that are dead due to hitting the side walls versus reversing the direction longitudinally in an RF cavity.

- `position/`
    - type: Required 3 x N-vector *(real)*
    - components: numParticles columns and rows of (`x`, `y`, `z`)
    - description: particle Position relative to the `positionOffset`.
    That is, true position relative to the coordinate origin = `position + positionOffset`.

- `direction`
  - type: Required 3 x N-vector *(real)*
  - components: numParticles columns and rows of (`x`, `y`, `z`)
  - description: `velocity` in beamphysics extension. 3 x N vector with rows being the direction in (`x`, `y`, `z`) respectively.

- `wavelength/`
  - type: Required 1 x N-vector *(real)*
  - description: Wavelength of the N-th ray.

Particle Record Dataset Attributes
----------------------------------

The following attributes can be used with any dataset:

- `minValue`:
  - type: Optional *(real)*
  - description: Minimum of the data.

- `maxValue`:
  - type: Optional *(real)*
  - description: Maximum of the data.
