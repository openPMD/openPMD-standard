Extension to the openPMD Standard for Describing Particle Beams and X-rays
==========================================

Version 1.0.0 (March 1, 2018)

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
coordinate (typically called **s**) typically runs through the nominal centers of the elements
in the machine. Typically, the **lattice** coordinate system is used to describe misalignments
of lattice elements with respect to the rest of the lattice.

- **Group**: A **group** is a container structure containing
a set of zero or more **attributes**, a set of zero or more **groups** (which can be called
**sub-groups**), and a set of zero or more **datasets**. Note: In HDF5, these are also
called **groups**.

- **Dataset**: A **dataset** is a structure that contains a set of zero or more **attributes** and a
data aray (which may be multidimensional).  Note: In HDF5, these are also called **datasets**.

- **Record**: A **record** is a **group** (without any sub-groups) or a **dataset** that contains data
on a physical quantity like particle charge or electric field. There are two types of **records**:
    - **scalar records** hold scalar quantity
    values (like particle charge). If all the particles have the same charge, the value of the charge
    is stored as an attribute of the **record** and there is no associated data array. That is, the
    **record** is a **group**. If the particles have differing charges, the values are stored in an array
    of the **scalar record**. In this case the **scalar record** is a **dataset**.
    - **vector records** hold a set of **datasets**. In this case the **record** is a **group**.
        - Example: A **record** named **E** for holding electric field values may have three datasets holding
        the components of the field named **E/x**, **E/y**, and **E/z**.

- **Attribute**: An **attribute** is a variable associated with a **group** along with a
value. Example: **snapshotPath** is a string variable associated with the root **/** group.

- **Polar coordinates**: **Polar** coordinates are **(r, theta, phi)** where **r** is the radius, **theta** is he angle
from the **z** or **s** axis, and **phi** is the projected azimuthal angle in the **(x, y)**
plane.

- **Particle Root Group**: The **Particle Root Group** is the root group for specifying a group of particles. There can be multiple **particle root groups** in a data file. For example, a set of particle bunches might specify one particle root group for each bunch. See the Base Standard for more information.

Notes:
------

- When using the **lattice** coordinate system, the `position` coordinates are **(x, y, s)** where
nominally **x** is the "radial" component,
**y** is the "vertical" coordinate, and **s** is the lattice longitudinal coordinate.


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
  - Type Optional *(int)*
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
        - `referenceEnergy`: Normalize with respect to the `referenceEenergy` attribute.
        - `none`: No normalization.

- `referenceEnergy`
    - Type: Optional *(float)* attribute.
    - Description: Specifies the reference energy from which the `energy` is measured with respect to.

- `referenceTotalMomentum`
    - Type: Optional *(float)* attribute
    - Description: Specifies the reference total momentum from which the total momentum is measured with respect to.

- `totalCharge`
    - Type: Optional *(float)* attribute.
    - Description: The total charge of all the particles.

Per-Particle Records of the `Particle Root Group`
---------------------

The following records store data on a particle by particle basis.

- `time-refTime`
- Type: Optional *(float)*
- Description: Particle time minus the referece time.

- `energy/`
  - Type: Optional *(float)*
  - Description: The total energy of the particles relative to the `referenceEnergy` attribute.

- `electricField/`
    - Type: Optional 2-component *(float)*
    - Description: Electric field. Used for photons only.
    - Components: (`x`, `y`).
        - For each component, the field is specified using either (`amplitude`, `phase`) or (`Real`, `Imaginary`)
        subcomponents.

- `macroCharge/`
    - Type: Optional *(float)*
    - Description: "Macro"-particles are simulation particles that represent multiple real particles.
    The `macroCharge` is the the total charge of the collection of particles that a macro-particle
    represents.

- `momentum/`
    - Type: Optional 2 or 3-vector *(float)*
    - Description: The total momentum of the particles relative to the `momentumOrigin` attribute.
    - Components: (`px`, `py`) or (`px`, `py`, `pz`).
    - Note: A program using phase space coordinates to describe particle positions will typically use the transverse momentum
    `px` and `py` along with the `totalMomentum` or `energy` records.

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


Particle Record Dataset Attributes
-----------------------------

The following attributes can be used with any dataset:

- `minValue`:
  - Type: Optional *(float)*
  - Description: Minimum of the data.

- `maxValue`:
  - Type: Optional *(float)*
  - Description: Maximum of the data.
