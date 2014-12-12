Domain-Specific Naming Conventions for Electro-Dynamic/Static PIC Codes
=======================================================================

Grid based data (fields)
------------------------

- Maxwell/field solver
- Current Solver
- smoothing

- naming conventions:
  - E/B/J
  - with species & added?
     e_#_*
      density, particleEnergy, energyDensity, particleCounter, larmor? skip?

Particle data (particles)
-------------------------

- Particle-Shape
- Particle-Pushing Algorithm
- Interpolation & smoothing for push

- required: charge, weighting, globalCellId, position = in-cell-position
  -> array or attribute
- optional: charge state

- naming conventions:
  - electrons      `e_#`
  - neutrals/atoms `n_#`
  - ions/positrons `p_#`

  `#` is either a number or a free description (e.g. `e_downstream`, `e_upstream`,
  `e_hot`, `e_beam`)
