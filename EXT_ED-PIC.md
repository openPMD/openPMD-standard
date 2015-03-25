Domain-Specific Naming Conventions for Electro-Dynamic/Static PIC Codes
=======================================================================

Grid based data (fields)
------------------------

### Additional Mandatory Attributes per `fieldName`

- `fieldSolver`
  - type: *(string)*
  - description: Maxwell/field solver
  - allowed values:
    - `Yee` ([doi:10.1109/TAP.1966.1138693](http://dx.doi.org/10.1109/TAP.1966.1138693))
    - `CK` (*Cole-Karkkainen* type solvers: [doi:10.1016/j.jcp.2011.04.003](http://dx.doi.org/10.1016/j.jcp.2011.04.003), [doi:10.1063/1.168620](http://dx.doi.org/10.1063/1.168620), [doi:10.1109/TAP.2002.801268](http://dx.doi.org/10.1109/TAP.2002.801268); M. Karkkainen et al., *Low-dispersionwake field calculation tools*, ICAP 2006)
    - `Lehe` ([doi:10.1103/PhysRevSTAB.16.021301](http://dx.doi.org/10.1103/PhysRevSTAB.16.021301))
    - `DS` (*Directional Splitting* after Yasuhiko Sentoku, [doi:10.1140/epjd/e2014-50162-y](http://dx.doi.org/10.1140/epjd/e2014-50162-y))
    - `PSTD`
    - `PSATD`
    - `PSAOTD`
    - `other`
    - `none`

- `fieldSolverOrder`
  - type: *(float)*
  - description: order of the `fieldSolver`
  - examples:
    - `2.0`
    - `3.0`
    - use `-1.0` for infinite order (for spectral solvers)

- `fieldSolverParameters`
  - type: *(string)*
  - description: additional parameters for fields solvers
                 (might be specified further in the future)

- `fieldSmoothing`
  - type: *(string)*
  - description: applied field filters for E and B
  - allowed values:
    - `Binomial`
    - `other`
    - `none`

- `fieldSmoothingParameters`
  - type: *(string)*
  - description: additional parameters to describe the applied filter further
  - example: `period=10;numPasses=4;compensator=true`
  - reserved for future use: `direction=array()`, `stride=array()`

- `currentSmoothing`
  - type: *(string)*
  - description: applied filters to the current field after the particles' current deposition
  - allowed values: same as for `fieldSmoothing`

- `currentSmoothingParameters`
  - type: *(string)*
  - description: additional parameters to describe the applied filter further
  - allowed values: same as for `fieldSmoothingParameters`

- `chargeCorrection`
  - type: *(string)*
  - description: applied corrections to fields to ensure charge conservation
  - allowed values:
    - `Mader`
    - `spectral` (various)
    - `other`

- `chargeCorrectionParameters`
  - example: `period=100`

### Naming Conventions

- fundamental: `E`/`B`
- auxiliary:
  - `J`/`rho`
  - fields derived from particles:
      `particleName_*`:
        `current`, `density`, `particleEnergy`, `energyDensity`, `particleCounter`, `larmor`?


Particle data (particles)
-------------------------

- `particleShape`
  - type: *(float)*
  - description: ... reference hockney ...
  - example values:
    - `0.` pointlike
    - `1.` linear
    - `2.` quadratic
    - `3.` quadrilinear
    - or an other `floating point` number

- `currentDeposition`
  - type: *(string)*
  - description: current deposition scheme
  - allowed values:
    - `VillaBune` ([doi:10.1016/0010-4655(92)90169-Y](http://dx.doi.org/10.1016/0010-4655(92)90169-Y))
    - `Esirkepov` ([doi:10.1016/S0010-4655(00)00228-9](http://dx.doi.org/10.1016/S0010-4655(00)00228-9))
    - `ZigZag`
    - `direct` (often used in spectral codes, usually used with `chargeCorrection`s)
    - `other`

- `currentDepositionParameters`
  - type *(string)*
  - description: further parameters for current deposition schemes;
                 optional attribute
                 (might be specified further in the future)
  - examples:
    - for `direct` scheme: (Birdsall & Langdon, *Plasma Physics via Computer Simulation*, 15-5)
      - `Boris`
      - `MorseNielson`

- `particlePush`
  - type: *(string)*
  - description: Particle-Pushing Algorithm
  - allowed values:
    - `Boris` (J.P. Boris. *Relativistic plasma simulation-optimization of a hybrid code.* USA, 1970)
    - `Vay` ([doi:10.1063/1.2837054](http://dx.doi.org/10.1063/1.2837054))
    - `other`

- `particleInterpolation`
  - type: *(string)*
  - description: method that was used to interpolate fields to particle positions,
                 as described in [doi:10.1016/j.crme.2014.07.006](http://dx.doi.org/10.1016/j.crme.2014.07.006)
                 section 2.4
  - allowed values:
    - `uniform`: The fields are interpolated directly from the staggered grid
                 to the particle positions (with the same interpolation order
                 in all directions).
    - `energyConserving`: Also known as *Galerkin method*.
                          The fields are interpolated directly from the staggered
                          grid to the particle positions (with reduced
                          interpolation order in the parallel direction). This
                          scheme is energy conserving in the limit of infinitely
                          small time steps.
    - `momentumConserving`: The fields are first interpolated from the staggered
                            grid points to the corners of each cell, and then from
                            the cell corners to the particle position (with the
                            same order of interpolation in all directions). This
                            scheme is momentum conserving in the limit of
                            infinitely small time steps.
    - `other`

- `particleSmoothing`
  - type: *(string)*
  - description: applied transformations or smoothing filters on copied
                 versions of the fields while interpolating those to 
                 the particle
  - allowed values:
    - `Binomial`
    - `other`
    - `none`

- `particleSmoothingParameters`
  - type: *(string)*
  - description: additional parameters to describe the applied filter further
  - example: `period=1;numPasses=2;compensator=false`
  - reserved for future use: `direction=array()`, `stride=array()`


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
