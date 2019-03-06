Extension to the openPMD Standard for Describing Particle Beams and X-rays
==========================================================================

Version 2.0.0

Overview
--------

The `BeamPhysics` extension to the openPMD standard is meant for describing particles and fields commonly encountered
in accelerator physics simulations.

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

- **Global coordinate system**: The **global** coordinate system is a coordinate system that is used to describe the position and orientation of machine elements in space. That is, the **global** coordinate system is fixed with respect to the building or room where the machine is placed independent of the machine itself.

- **Lattice coordinate system**: The curvilinear coordinate system whose "longitudinal" coordinate (**s**) typically runs through the nominal centers of the elements in the machine. The **lattice** coordinate system is often used to describe particle positions.

- **Macro-particle**: Macro-particles are simulation particles that represent multiple real particles. The number of real particles that a macro-particle represents affects the calculation of the field due to a macro-particle but does not affect tracking.

- **Polar coordinates**: **Polar** coordinates are **(r, theta, phi)** where **r** is the radius, **theta** is the angle from the **z** or **s** axis, and **phi** is the projected azimuthal angle in the **(x, y)** plane.

- **Particle Root Group**: The **Particle Root Group** is a group for specifying a group of particles. See the Base Standard for more information.

- **Phase Space Coordinates**: Phase space coordinates are ordered (x, px, y, py, z, pz).

Notes:
------

- When using the **lattice** coordinate system, the `position` coordinates are **(x, y, s)** or **(x, y, z)** where, nominally, **x** is the "horizontal" component, **y** is the "vertical" coordinate, and **s** or **z** is the lattice longitudinal coordinate.

Additional File Root Group (Path `/`) Records
---------------------------------------------

The following records are defined for the file root group.

- `latticeName`
  - Type: Optional *(string)*
  - Description: The name of the lattice.

- `latticeFile`
  - Type: Optional *(string)*
  - Description: The location of the root lattice file.


`Particle Root Group` records
-----------------------------

For each **particle root group** the following records are defined:

- `latticeElementName`
  - Type: Optional *(string)*
  - Description: The name of the lattice element the particle or particles are in. This only makes sense if all particles are in the same lattice element. Also see: `latticeElementID` and `locationInElement`.

- `latticeElementID`
  - Type Optional *(string)*
  - Description: The ID string for the lattice element given by `latticeElementName`. The idea is that while more than one lattice element may have the same name, the ID string will be unique.
  - This, along with `locationInElement` sets the origin for specifying particle positions in the **lattice** coordinate system.
  - Example: With [Bmad](https://www.classe.cornell.edu/bmad/) based programs the ID string is of the form
    **branch-index>>element-index** where **branch-index** is the associated branch index integer, and **element-index** is the associated lattice element index within the branch.

- `locationInElement`
  - Type Optional *(integer)*
  - Description: The program generating the data file may model a lattice element using a "hard edge" model where the fringe fields at the ends of the element are modeled as having zero longitudinal length. In such a case, if a particle is at the end of the lattice element, it is important to know if the particle is outside of the fringe or if the particle is inside the fringe within the body of the element. Note that with a hard edge fringe, the longitudinal **s**-position does not necessarily provide enough information to determine where a particle is with respect to an edge field. Another situation where `locationInElement` is useful is with zero length elements that affect the particle transport (such as zero length multipole elements). If the program generating the data file does **not** use any hard edge models or zero length non-marker elements, `locationInElement` should not be present since this parameter is meaningless in this case.
  - Possible values:    
    - -1: Upstream end of element outside of the upstream fringe edge.
    - 0: Inside the element.
    - 1: Downstream end of the element outside the downstream fringe edge.

- `referenceMomentum`
  - Type: Optional *(float)*
  - Description: Reference momentum Possibly used for normalizing particle momentum values.

- `referenceTotalEnergy`
  - Type: Optional *(string)*
  - Description: Reference total (kinetic + rest mass) energy. Possibly used for normalizing particle momentum values.

- `speciesType`
  - Type: Required *(string)*
  - Description: The name of the particle species. Species names must conform to the `SpeciesType` extension.
  - Example: `electron`, `H2O`.


Per-Particle Records of the `Particle Root Group`
-------------------------------------------------

The following records store data on a particle-by-particle basis.

- `charge/`
  - Type: Optional *(int)*
  - Description: The charge state of the particles. Used for atoms and molecules. Not needed if the charge can be computed from knowledge of the `SpeciesType` (That is, a fundamental particle). Also see `weight`.

- `electricField/`
    - Type: Optional 3-vector *(float)*
    - Description: External electric field at the particle.
    - Components: (`x`, `y`, `z`).

- `magneticField/`
    - Type: Optional 3-vector *(float)*
    - Description: External magnetic field at the particle.
    - Components: (`x`, `y`, `z`).

- `photonPolarization/`
    - Type: Optional 2-vector *(complex)*
    - Description: Polarization of the photon
    - Components: (`x`, `y`), transverse to the direction of the photon.

- `momentum/`
  - Type: Optional 3-vector *(float)*
  - Description: The momentum vector of the particles relative to `momentumOffset`
  - Components: (`px`, `py`, `pz`).
  - True momentum = `momentum + momentumOffset`

- `momentumOffset/`
  - Type: Optional 3-vector *(float)*
  - Description: offset for each momentum component.
  - Components: (`px`, `py`, `pz`).

- `totalMomentum/`
  - Type: Optional *(float)*
  - Description: Total momentum relative to the totalMomentumOffset. That is, True total momentum = `totalMomentum + totalMomentumOffset`.

- `totalMomentumOffset/`
  - Type: Optional *(float)*
  - Description: Offset for the total momentum.

- `totalEnergy/`
  - Type: Optional *(float)*
  - Description: Total energy relative to the totalEnergyOffset. That is, true total energy = `totalEnergy + totalEnergyOffset`.

- `totalEnergyOffset/`
  - Type: Optional *(float)*
  - Description: Offset for the total momentum.

- `particleStatus/`
    - Type: Optional *(int)*
    - Description: Integer indicating whether a particle is "alive" or "dead" (for example, has hit the vacuum chamber wall). A zero value indicates the particle is alive and any other value indicates that the particle is dead. Programs are free to distinguish how a particle died by assigning different non-zero values to "modes of death". For example, a program might want to differentiate between particles that are dead due to hitting one surface verses hitting a different surface.

- `pathLength/`
    - Type: Optional *(float)*
    - Description: Length that a particle has traveled.

- `position/`
    - Type: Required 3-vector *(float)*
    - Components: (`x`, `y`, `z`)
    - Description: particle Position relative to the `positionOffset`.
    That is, true position relative to the curvilinear coordinate origin = `position + positionOffset`.

- `positionOffset/`
    - Type: Optional 3-vector *(float)*
    - Description: Offset for each particle position component relative to the curvilinear coordinate origin.
    - Components: (`x`, `y`, `z`)
    - Attributes:

- `speed/`
    - Type: Optional *(float)*
    - Description: The speed (velocity magnitude) of a particle.

- `spin/`
    - Type: Optional 3-vector *(float)*
    - Description: Particle spin.
    - Components: (`x`, `y`, `z`) or (`r`, `theta`, `phi`).

- `time/`
    - Type: Optional *(float)*
    - Description: Time relative to `timeOffset`. That is, absolute time = `time + timeOffset`.

- `timeOffset`
    - Type: Optional *(float)*
    - Description: The reference particle time.
    Note that the reference time is a function of **s** and therefore can be different for different particles.

- `velocity/`
  - Type: Optional 3-vector *(float)*
  - Description: (`Vx`, `Vy`, `Vz`) velocity vector.

- `weight/`
    - Type: Optional *(float)*
    - Description: If macro-particles are being simulated, the `weight` is the total charge of a macro-particle or the total number of particles that a macro-particle represents. Also see `charge`.


Non Per-Particle Records of the `Particle Root Group`
-----------------------------------------------------

The following possible records of the `Particle Root Group` are for specifying properties of the entire group of particles.

- `phaseSpaceFirstOrderMoment/`
  - Type: Optional 6-vector *(float)*
  - Description: First order beam moments.

- `phaseSpaceSecondOrderMoment/`
  - Type: Optional 6x6-matrix *(float)*
  - Description: Second order beam moments.

- `phaseSpaceThirdOrderMoment/`
  - Type: Optional 6x6x6-tensor *(float)*
  - Description: Third order beam moments.

- `latticeToGlobalTransformation/`
  - Type: Optional group.
  - Description: Defines the transformation from **lattice** coordinates to **global** coordinates for a position
  specified by `latticeElementName`/`latticeElementID` and `locationInElement`.
  - `R_frame`:
    - Required 3-vector *(float)* Attribute
    - Description: specifying the (x, y, z) position of the **lattice** coordinate origin with respect
  to the **global** coordinates.
  - `W_matrix`:
    - Required 3 x 3 matrix *(float)*
    - Description: Dataset holding the 3x3 transformation matrix from **lattice** coordinates to **global**
  coordinates.
  - Position Transformation: Position_global = W_matrix * Position_lattice + R_frame
  - Momentum transformation: Momentum_global = W_matrix * Momentum_lattice

- `totalCharge`
  - Type: Optional *(float)* attribute.
  - Description: The total charge of all the particles.

Particle Record Dataset Attributes
----------------------------------

The following attributes can be used with any dataset:

- `minValue`:
  - Type: Optional *(float)*
  - Description: Minimum of the data.

- `maxValue`:
  - Type: Optional *(float)*
  - Description: Maximum of the data.
