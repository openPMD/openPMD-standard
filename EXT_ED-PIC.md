Domain-Specific Naming Conventions for Electro-Dynamic/Static PIC Codes
=======================================================================

Grid based data (fields)
------------------------

### Additional Mandatory Attributes per `fieldName`

- Maxwell/field solver
  - allowed values:
    - Yee
    - Karkinnen
    - DS
    - PSTD
    - PSATD
    - PSAOTD
    - other
  - reserved for future use: `solverParameters`

- Current Solver
  - allowed values:
    - VillaBune
    - Esirkepov
    - ZigZag
    - other
  - reserved for future use: `...Parameters`

- `smoothing`
  - allowed values:
    - Binomial
    - ...
    - other
  - `smoothingPeriod`
  - `smoothingParameters`


### Naming Conventions

- `E`/`B`/`J`
- fields derived from particles:
    `particleName_*`:
      `density`, `particleEnergy`, `energyDensity`, `particleCounter`, `larmor`?

Particle data (particles)
-------------------------

- Particle-Shape / -Order
  - 0 pointlike
  - 1 linear
  - 2 quadratic
  - 3 quadrilinear
  - ...
  - other

- Particle-Pushing Algorithm
  - Boris
  - Vay
  - Karkinnen Pusher
  - other

- Interpolation & smoothing for push
  - momemtum conserving? true/false
  - energy conserving? true/false
  - field-smoothing/transformation?

### Additional Mandatory Properties per Particle Species

- required: charge, weighting, globalCellId, position = in-cell-position
  -> as usual as an array or attribute
  -> [!] if position is in-cell-position, than unitSI is different for each component
- charge state, ionizable (true/false), "electron"/fundamental particle
- ions & atoms: proton number + neutron number?

### Additional Data Set per Particle Species

  - `particleGroups`
    - type: *(struct of five uint64)*
      - `numParticles`: number of particles in block
      - `rank`: unique, zero-based, contiguous index of the writing process
                (e.g., the MPI-rank)
      - `offsetX`: position offset in `x`, `y` and `z`
      - `offsetY`, `offsetZ`: see `offsetX`, must NOT be omitted or replaced
                              in 2D/1D
    - size: the data set contains `max(rank)` structs, e.g., the MPI-size
    - description: to allow post-processing and visualization tools
                   to read data sets with the size of more than the typical
                   size of a local-nodes RAM, this attribute allows to
                   group data sets that are close in `position` to ensure
                   an intermediate level of data locality;
                   groups of particles must be adjacent boxes (or rectangles
                   in 2D) regarding the `position` of the particles within
