Domain-Specific Naming Conventions for Electro-Dynamic/Static PIC Codes
=======================================================================

Grid based data (fields)
------------------------

### Additional Mandatory Attributes per `fieldName`

- fieldSolver
  - type: *(string)*
  - description: Maxwell/field solver
  - allowed values:
    - Yee
    - Karkinnen
    - DS
    - PSTD
    - PSATD
    - PSAOTD
    - other

- fieldSolverOrder
  - type: "(float)*
  - description: order of the `fieldSolver`
  - example: "2.0", "3.0", use "-1.0" for infinite

- reserved for future use: `fieldSolverParameters`

- `fieldSmoothing`
  - type: *(string)*
  - description: applied field filters for E and B
  - allowed values:
    - Binomial
    - ...
    - other

- reserved for future use:
  - `fieldSmoothingPeriod`
  - `fieldSmoothingOrder`
  - `fieldSmoothingParameters`


### Naming Conventions

- `E`/`B`/`J`
- fields derived from particles:
    `particleName_*`:
      `density`, `particleEnergy`, `energyDensity`, `particleCounter`, `larmor`?


Particle data (particles)
-------------------------

- `particleShape`
  - type: *(float)*
  - description: ... reference hockney ...
  - example values:
    - 0. pointlike
    - 1. linear
    - 2. quadratic
    - 3. quadrilinear
    - ...
    - other

- `currentDeposition`
  - type: *(string)*
  - description: current deposition scheme
  - allowed values:
    - VillaBune
    - Esirkepov
    - ZigZag
    - other

- reserved for future use: `currentDepositionParameters`

- `currentSmoothing`
  - type: *(string)*
  - description: applied current filters after current deposition

- reserved for future use:
  - `currentSmoothingPeriod`
  - `currentSmoothingOrder`
  - `currentSmoothingParameters`

- `particlePush`
  - type: *(string)*
  - description: Particle-Pushing Algorithm
  - reserved values:
    - Boris
    - Vay
    - Karkainen Pusher
    - other

- `particleInterpolation`
  - type: *(string)*
  - description:
  - reserved values:
    - Galerkin
    - Trilinear
    - other

- reserved for future use:
  - momemtum conserving? true/false
  - energy conserving? true/false

- `particleSmoothing`
  - type: *(string)*
  - description: applied transformations or smoothing filters while interpolating
                 fields to the particle

- reserved for future use:
  - `particleSmoothingPeriod`
  - `particleSmoothingOrder`
  - `particleSmoothingParameters`

### Additional Mandatory Properties per Particle Species

- required: charge, masss, weighting, globalCellId, position = in-cell-position,
            descriptive long name "2nd e-", "Deuterium"
  -> as usual as an array or attribute
  -> [!] if position is in-cell-position, than unitSI is different for each component
- charge state (float), "electron"/"fundamental" particle numbers (float)
- atomic numbers: proton number + neutron number (float)

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
