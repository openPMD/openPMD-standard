Extension to the openPMD Standard for Describing Particle Beams and X-rays
==========================================

Version 2.0.0

Overview
------------

The `BeamPhysics` extension to the openPMD standard is meant for describing particles and fields commonly encountered
in accelerator physics simulations.

How to Use this Extension
---------------

The `BeamPhysics` extension to the openPMD standard is indicated in a data file by the setting of the `openPMDextension` attribute:
```
  openPMDextension = BeamPhysics, SpeciesType
```

Note: The `SpeciesType` extension must be used when using the `BeamPhysics` extension.

Definitions
-----------

- **Lattice**: A **lattice** is the arrangement of elements in a machine such as a particle accelerator.

- **Global coordinate system**: The **global** coordinate system is a coordinate system that is
used to describe the position and orientation of machine elements in space. That is, the **global**
coordinate system is fixed with respect to the building or room where the machine is placed independent of the
machine itself.

- **Lattice coordinate system**: The curvilinear coordinate system whose "longitudinal"
coordinate (**s**) typically runs through the nominal centers of the elements
in the machine. The **lattice** coordinate system is often used to describe particle positions.

- **Macro-particle**: Macro-particles are simulation particles that represent multiple real particles.

- **Polar coordinates**: **Polar** coordinates are **(r, theta, phi)** where **r** is the radius, **theta** is the angle
from the **z** or **s** axis, and **phi** is the projected azimuthal angle in the **(x, y)**
plane.

- **Particle Root Group**: The **Particle Root Group** is a group for specifying a group of particles. See the Base Standard for more information.

- **Phase Space Coordinates**: Phase space coordinates are ordered (x, px, y, py, z, pz).

Notes:
------

- When using the **lattice** coordinate system, the `position` coordinates are **(x, y, s)** where
nominally **x** is the "horizontal" component, **y** is the "vertical" coordinate, and **s** is the lattice longitudinal coordinate.

- T

Additional File Root Group (path `/`) Attributes
-------------------------

The following attributes are defined for the file root group.

- `latticeName`
  - Type: Optional *(string)*
  - Description: The name of the lattice.

- `latticeFile`
  - Type: Optional *(string)*
  - Description: The location of the root lattice file.


`Particle Root Group` Attributes
---------------------

For each **particle root group** the following attributes are defined:

- `SpeciesType`
  - Type: Required *(string)*
  - Description: The name of the particle species. Species names must conform to the
  `SpeciesType` extension.
  - Example: `electron`, `H2O`.

- `charge`
  - Type: Optional *(int)*
  - Description: The charge state of the particles. Not needed if the charge can be computed
  from knowledge of the `SpeciesType`.

- `latticeElementName`
  - Type: Optional *(string)*
  - Description: The name of the lattice element the particle or particles are in. This only makes sense if all
  particles are in the same lattice element. Also see: `latticeElementID` and `locaitonInElement`.

- `latticeElementID`
  - Type Optional *(string)*
  - Description: The ID string for the lattice element given by `latticeElementName`. The idea is that while more than
    one lattice element may have the same name, the ID string will be unique.
  - This, along with `locationInElement` sets the origin for specifying particle positions in the **lattice** coordinate system.
  - Example: With [Bmad](https://www.classe.cornell.edu/bmad/) based programs the ID string is of the form
    **branch-index>>element-index** where **branch-index** is the associated
branch index integer, and **element-index** is the associated lattice element index within the branch.

- `locationInElement`
  - Type Optional *(string)*
  - Description: This attribute is used with  `latticeElementID`/`latticeElementName` to specify
  the origin where the particle or particles are measured with respect in the **lattice** coordinate system.   
  - The origin is always on the longitudinal axis (x = y = 0) of the **lattice** coordinate system.
  - Possible values:    
    - `Upstream-End`: Upstream end of element outside of any edge fields.
    - `<s-position>`: Where `<s-position>` is a number. Inside the element at a distance, given by `<s-position>`,
    from the upsteam end of the element.
    - `Downstream-End`: Downstream end of the element outside of any edge fields.
  - Note: Since some programs will model edge fields of a lattice element as having zero length, the longitudinal **s**-position
does not necessarily provide enough information to determine where a particle is with respect to an edge field so `Upstream-End` and `Downstream-End` are provided.

- `momentumNormalization`
    - Type: Optional *(string)*
    - Description: Normalization used for momentum values.
    - Possible values:
        - `referenceTotalMomentum`: Normalize with respect to the `referenceTotalMomentum` attribute
        - `referenceEnergy`: Normalize with respect to the `referenceEnergy` attribute.
        - `none`: No normalization.


Per-Particle Records of the `Particle Root Group`
---------------------

The following records store data on a particle by particle basis.

- `time-refTime`
- Type: Optional *(float)*
- Description: Particle time minus the reference time.

- `energy/`
  - Type: Optional *(float)*
  - Description: The total energy of the particles. This record may be used instead of specifying the `pz` phase space coordinate.
  - Attributes: The following attributes are defined.
    - `relative`:
      - Type: Required **(bool)**
      - Description: Is the energy relative to the `referenceEnergy`?
    - `normalized`:
      - Type: Required **(bool)**
      - Description: Is the energy normalized by the `totalMomentum`?
  - Examples: [E = Energy, E0 = `referenceEnergy`, p0 = `totalMomentum`]
    - `relative` = `F`, `normalized` = `F`  --> Energy = E
    - `relative` = `F`, `normalized` = `T`  --> Energy = E / p0
    - `relative` = `T`, `normalized` = `F`  --> Energy = E - E0
    - `relative` = `T`, `normalized` = `T`  --> Energy = (E - E0) / p0

- `electricField/`
    - Type: Optional 2-component *(float)*
    - Description: Electric field. Used for photons only.
    - Components: (`x`, `y`).
        - For each component, the field is specified using either (`amplitude`, `phase`) or (`Real`, `Imaginary`)
        subcomponents.

- `momentum/`
    - Type: Optional 2 or 3-vector *(float)*
    - Description: The total momentum of the particles relative to the `momentumOrigin` attribute.
    - Components: (`px`, `py`) or (`px`, `py`, `pz`).
    - Attributes: The following attributes are defined.
      - `normalized`:
        - Type: Required **(bool)**
        - Description: Is the energy normalized by the `referenceTotalMomentum`? That is, is `px` equal to Px or Px/P0 (where Px is the true momentum component and P0 is `referenceTotalMomentum`)?
    - Note: A program using phase space coordinates to describe particle positions will typically use the transverse momentum `px` and `py` along with the `totalMomentum` or `energy` records.

- `pathLength/`
    - Type: Optional *(float)*
    - Description: Length that a particle has traveled.

- `position`
    - Type: Required 3-vector *(float)*
    - Description: Position relative to the coordinate origin.
    - Components: (`x`, `y`, `<z-coord>`) where `<z-coord>` is one of:
        - `z`: True longitudinal coordinate.
        - `-beta.c.dt`: Phase space coordinate conjugate to a momentum based "pz".
        - `-beta.c.t`:Phase space coordinate conjugate to a momentum based "pz".
        - `-c.dt`: Phase space coordinate conjugate to an energy based "pz".
        - `-c.t`: Phase space coordinate conjugate to an energy based "pz".
        - Where: **beta** = particle speed, **c** = speed of light, **t** = time, and **dt** = time relative to the reference time.

- `refTime/`
    - Type: Optional *(float)*
    - Description: The reference particle time.
    Note that the reference time is a function of **s** and therefore can be different for different particles.

- `s-Position`
    - Type: Optional *(float)*
    - Description: Absolute longitudinal distance in **lattice** coordinates.  

- `speed/`
    - Type: Optional *(float)*
    - Description: The speed of the particles.

- `spin/`
    - Type: Optional 3-vector *(float)*
    - Description: Particle spin.
    - Components: (`x`, `y`, `s`) or (`r`, `theta`, `phi`).

- `time/`
    - Type: Optional *(float)*
    - Description: Absolute particle time. Note: Particles may have different times if the snapshot
    is, for example, taken at constant **s**.

- `totalMomentum/`
    - Type: Optional *(float)*
    - Description: The total momentum of the particles relative to the `referenceTotalMomentum` attribute.

- `weighting/`
    - Type: Optional *(float)*
    - Description: If macro-particles are being simulated, the `weighting` is the the total charge or total number of the collection of particles that a macro-particle represents.


Non Per-Particle Records of the `Particle Root Group`
---------------------

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

- `referenceEnergy`
  - Type: Optional *(float)* attribute.
  - Description: Specifies the reference energy from which the `energy` is measured with respect to.

- `referenceTotalMomentum`
  - Type: Optional *(float)* attribute
  - Description: Specifies the reference total momentum from which the total momentum is measured with respect to.

- `totalCharge`
  - Type: Optional *(float)* attribute.
  - Description: The total charge of all the particles.

Particle Record Dataset Attributes
-----------------------------

The following attributes can be used with any dataset:

- `minValue`:
  - Type: Optional *(float)*
  - Description: Minimum of the data.

- `maxValue`:
  - Type: Optional *(float)*
  - Description: Maximum of the data.
