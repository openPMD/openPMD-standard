Domain-Specific Naming Conventions for Electro-Dynamic/Static PIC Codes
=======================================================================

openPMD extension name: `ED-PIC`

openPMD extension ID: `1`


Introduction
------------

This extension is specifically designed for the domain of electro-dynamic and
electro-static particle-in-cell (PIC) codes.

The current version of this extension is suitable to allow the output of
arbitrary simulation codes to be post-processed and compared with common
tools and frameworks. Future versions will define a common set of required
records and further attributes (e.g., for moving window and boosted frame
simulations) that will allow to restart the checkpoints of one PIC code with
an other.


Mesh Based Records (Fields)
---------------------------

### Additional Attributes for the Group `meshesPath`

The following additional attributes are defined to this extension.
The individual requirement is given in `scope`.

  - `fieldSolver`
    - type: *(string)*
    - scope: *required*
    - description: Maxwell/field solver
    - allowed values:
      - `Yee` ([doi:10.1109/TAP.1966.1138693](http://dx.doi.org/10.1109/TAP.1966.1138693))
      - `CK` (*Cole-Karkkainen* type solvers: [doi:10.1016/j.jcp.2011.04.003](http://dx.doi.org/10.1016/j.jcp.2011.04.003),
              [doi:10.1063/1.168620](http://dx.doi.org/10.1063/1.168620),
              [doi:10.1109/TAP.2002.801268](http://dx.doi.org/10.1109/TAP.2002.801268);
              M. Karkkainen et al., *Low-dispersion wake field calculation tools*, ICAP 2006)
      - `Lehe` ([doi:10.1103/PhysRevSTAB.16.021301](http://dx.doi.org/10.1103/PhysRevSTAB.16.021301))
      - `DS` (*Directional Splitting* after Yasuhiko Sentoku,
              [doi:10.1140/epjd/e2014-50162-y](http://dx.doi.org/10.1140/epjd/e2014-50162-y))
      - `PSTD` (*Pseudo-Spectral Time Domain*, e.g.,
                Q. H. Liu, Letters 15 (3) (1997) 158–165)
      - `PSATD` (*Pseudo-Spectral Analytical Time Domain*, I. Haber, R. Lee,
                 H. Klein, J. Boris, Advances in electromagnetic simulation
                 techniques, 1973)
      - `GPSTD`
      - `other`
      - `none`

  - `fieldSolverParameters`
    - type: *(string)*
    - scope: *required* if `fieldSolver` is `other` or `GPSTD`, *optional*
             otherwise
    - description: additional scheme and parameters specification for fields
                   solvers

  - `fieldBoundary`
    - type: array of *(string)* of length 2 `N`
    - scope: *required*
    - description: boundary conditions in each direction (in the
                   above, `N` is the dimensionality of the field mesh)
                   ; the strings are stored in the following order:
      - boundary at the *lower* end of the *first* axis as in `axisLabels`
      - boundary at the *upper* end of the *first* axis as in `axisLabels`
      - boundary at the *lower* end of the *second* axis as in `axisLabels`
      - boundary at the *upper* end of the *second* axis as in `axisLabels`
      - ...
      - boundary at the *upper* end of the last axis as in `axisLabels`
    - allowed values:
      - `periodic`
      - `open` (optionally add scheme specification, such as PML,
                Silver-Muller, etc., in the `fieldBoundaryParameters` string)
      - `reflecting` (optionally add scheme specification, such as
                      Neumann-type or Dirichlet-type, in the
                      `fieldBoundaryParameters` string)
      - `other`

  - `fieldBoundaryParameters`
    - type: array of *(string)* of length 2 `N`
    - scope: *required* if `fieldBoundary` is `other`, *optional* otherwise
    - description: additional scheme and parameters specification for
                   the boundary conditions

  - `particleBoundary`
    - type: array of *(string)* of length 2 `N`
    - scope: *required*
    - description: boundary conditions in each direction (in the above, `N` is
                   the dimensionality of the field mesh)
                   The strings are stored in the following order:

      - boundary at the *lower* end of the *first* axis as in `axisLabels`
      - boundary at the *upper* end of the *first* axis as in `axisLabels`
      - boundary at the *lower* end of the *second* axis as in `axisLabels`
      - boundary at the *upper* end of the *second* axis as in `axisLabels`
      - ...
      - boundary at the *upper* end of the last axis as in `axisLabels`
    - allowed values:
      - `periodic`
      - `absorbing`
      - `reflecting`
      - `reinjecting` (optionally add scheme specification - such as
        "thermal, T=1keV" - in the `particleBoundaryParameters` string)
      - `other`
    - note: currently all particles must have the same boundary condition,
            might become a particle attribute in the future

  - `particleBoundaryParameters`
    - type: array of *(string)* of length 2 `N`
    - scope: *required* if `particleBoundary` is `other`, *optional* otherwise
    - description: additional scheme and parameters specification for the
                   boundary conditions

  - `currentSmoothing`
    - type: *(string)*
    - scope: *required*
    - description: applied filters to the current field after the particles'
                   current deposition
    - note: may becomes a particle record attribute in the future
    - allowed values:
      - `Binomial`
      - `other`
      - `none`

  - `currentSmoothingParameters`
    - type: *(string)*
    - scope: *required* if `currentSmoothing` is not `none`
    - description: additional parameters to describe the applied
                   filter further
    - note: may becomes a particle record attribute in the future
    - example: `period=10;numPasses=4;compensator=true`
    - reserved for future use: `direction=array()`, `stride=array()`

  - `chargeCorrection`
    - type: *(string)*
    - scope: *required*
    - description: applied corrections to fields to ensure charge conservation
    - allowed values:
      - `Marder` ([doi:10.1016/0021-9991(87)90043-X](http://dx.doi.org/10.1016/0021-9991(87)90043-X))
      - `Langdon` ([doi:10.1016/0010-4655(92)90105-8](http://dx.doi.org/10.1016/0010-4655(92)90105-8))
      - `Boris` (Birdsall & Langdon, *Plasma Physics via Computer Simulation*,
                 15-6)
      - `hyperbolic` (section III-B in [doi:10.1063/1.872648](http://dx.doi.org/10.1063/1.872648),
                      [doi:http://dx.doi.org/10.1006/jcph.2000.6507](http://dx.doi.org/10.1006/jcph.2000.6507),
                      section 2.3 in
                      [doi:10.1016/S0920-3796(96)00502-9](http://dx.doi.org/10.1016/S0920-3796(96)00502-9))
      - `spectral` (various)
      - `other`
      - `none`

  - `chargeCorrectionParameters`
    - type: *(string)*
    - scope: *required* if `chargeCorrection` is not `none`
    - description: additional parameters to describe the charge
      correction parameter
    - example: `period=100`

### Additional Attributes for each `mesh record` (field record)

The following additional attributes for `mesh record`s are defined in this
extension. The individual requirement is given in `scope`.

  - `fieldSmoothing`
    - type: *(string)*
    - scope: *required*
    - description: applied field filters for E and B
    - allowed values: same as for `currentSmoothing`

  - `fieldSmoothingParameters`
    - type: *(string)*
    - scope: *required* if `fieldSmoothing` is not `none`
    - description: additional parameters to describe the applied filter
                   further (similar to `currentSmoothingParameters`)

### Naming Conventions for `mesh record`s (field records)

When added to an output, the following naming conventions shall be used for
`mesh records` to allow an easy the identification of essential fields. If
these namings are not used, tools might still detect a record by it's
`unitDimension` as, e.g., *an* electric field but not as *the* main electric
field that should be distributed again on the cells.

- fundamental fields:
  - `E`
    - type: *(floatX)* or *(intX)* or *(uintX)*
    - description: the electric field
    - advice to implementors: a *(floatX)* type is likely the most frequent case
                              for this record
    - advice to implementors: must have
                              `unitDimension = (1., 1., -3., -1., 0., 0., 0.)`
                              (V/m = kg * m / (A * s^3))
  - `B`
    - type: *(floatX)* or *(intX)* or *(uintX)*
    - description: the magnetic field
    - advice to implementors: must have
                              `unitDimension = (0., 1., -2., -1., 0., 0., 0.)`
                              (T = kg / (A * s^2))
    - advice to implementors: a *(floatX)* type is likely the most frequent case
                              for this record

- auxiliary fields:
  - fields derived from particle species, discretized on the mesh (cells):
    prefix them with `<particleSpecies>_*`:
    - defined names and examples:
      - `J`: such as `electron_J` for current densities created by the
             particles in particle species `electron`
      - `density`: such as `electron_density` (elements per volume/area/line)
      - `chargeDensity`: such as `electron_chargeDensity` (charge per
                         volume/area/line)
      - `particleEnergy`: kinetic energy of all particles, with their weighted
                          contribution to a cell
      - `energyDensity`: same as `particleEnergy` but divided by `density`
      - `particleCounter`: ignores the shape of a particle and just checks if
                           the position of it "corresponds" to a cell

  - to store the same quantities as above, but summed for each cell over all
    particles in all particle species, skip the prefix and use the defined
    names directly


Particle Records (Macroparticles)
---------------------------------

### Additional Attributes for the `Group` of each Particle Species

The following additional attributes are defined in this extension.
The individual requirement is given in `scope`.

  - `particleShape`
    - type: *(floatX)*
    - scope: *required*
    - description: the order of the particle assignment function shape
                   (see *Hockney* reprint 1989, ISBN:0-85274-392-0, table 5-1)
    - example values:
      - `0.` pointlike (NGP)
      - `1.` linear (CIC)
      - `2.` quadratic (TSC)
      - `3.` quadrilinear (PQS)
      - or any other positive `floating point` number

  - `currentDeposition`
    - type: *(string)*
    - scope: *required*
    - description: current deposition scheme
    - allowed values:
      - `VillaBune` ([doi:10.1016/0010-4655(92)90169-Y](http://dx.doi.org/10.1016/0010-4655(92)90169-Y))
      - `Esirkepov` ([doi:10.1016/S0010-4655(00)00228-9](http://dx.doi.org/10.1016/S0010-4655(00)00228-9))
      - `ZigZag`
      - `directBoris` (Birdsall & Langdon,
                       *Plasma Physics via Computer Simulation*, 15-5)
      - `directMorseNielson` (Birdsall & Langdon,
                              *Plasma Physics via Computer Simulation*, 15-5)
      - `other`
      - `none`

  - `currentDepositionParameters`
    - type *(string)*
    - scope: *optional*
    - description: further parameters for current deposition schemes;
                   reserved for future use

  - `particlePush`
    - type: *(string)*
    - scope: *required*
    - description: Particle-Pushing Algorithm
    - allowed values:
      - `Boris` (J.P. Boris. *Relativistic plasma simulation-optimization of a*
                 *hybrid code.* USA, 1970)
      - `Vay` ([doi:10.1063/1.2837054](https://dx.doi.org/10.1063/1.2837054))
      - `free-streaming` (constantly moving with initial momentum)
      - `LLRK4` (reduced Laundau-Lifshitz pusher via RK4 and classical
                 radiation reaction,
                 [doi:10.1016/j.cpc.2016.04.002](https://dx.doi.org/10.1016/j.cpc.2016.04.002))
      - `none` (static particles such as probes)
      - `other`

  - `particleInterpolation`
    - type: *(string)*
    - scope: *required*
    - description: method that was used to interpolate fields to particle
                   positions, as described in
                   [doi:10.1016/j.crme.2014.07.006](http://dx.doi.org/10.1016/j.crme.2014.07.006)
                   section 2.4
    - allowed values:
      - `uniform`: The fields are interpolated directly from the staggered grid
                   to the particle positions (with the same interpolation order
                   in all directions).
      - `energyConserving`: Also known as *Galerkin method*.
                            The fields are interpolated directly from the
                            staggered grid to the particle positions (with
                            reduced interpolation order in the parallel
                            direction). This scheme is energy conserving in the
                            limit of infinitely small time steps.
      - `momentumConserving`: The fields are first interpolated from the
                              staggered grid points to the corners of each
                              cell, and then from the cell corners to the
                              particle position (with the same order of
                              interpolation in all directions). This
                              scheme is momentum conserving in the limit of
                              infinitely small time steps.
      - `other`



  - `particleSmoothing`
    - type: *(string)*
    - scope: *required*
    - description: applied transformations or smoothing filters on copied
                   versions of the fields while interpolating those to
                   the particle
    - allowed values:
      - `Binomial`
      - `other`
      - `none`

  - `particleSmoothingParameters`
    - type: *(string)*
    - scope: *required* if `particleSmoothing` is not `none`
    - description: additional parameters to describe the applied filter further
    - example: `period=1;numPasses=2;compensator=false`
    - reserved for future use: `direction=array()`, `stride=array()`

### Additional Attributes for each Particle `Record`

The following additional attributes for `particle record`s are defined in this
extension. The individual requirement is given in `scope`.

When using macroparticles (see below for the definition of the
macroparticle `weighting`), there is an ambiguity regarding whether the
particle quantity that is written (e.g. energy, momentum) is that of
the full macroparticle, or that of the underlying individual
particle. Therefore, this extension requires the two following attributes:

- `macroWeighted`
  - type: *(uint32)*
  - scope: *required*
  - description: indicates whether this quantity is written for the underlying
                 particle (`macroWeighted = 0`) or for the full macroparticle
                 (`macroWeighted = 1`)
  - example: Let us assume that a user writes the `charge` attribute of a
             macroparticle that represents 100 electrons. If this user chooses
             to write -1.6e-19 (charge of one individual electron) then
             `macroWeighted` must be 0. If the user writes -1.6e-17 (total
             charge of 100 electrons), then macroweighted must be 1

- `weightingPower`
  - type: *(float64 / REAL8)*
  - scope: *required*
  - description: indicates with which power of `weighting` (see below)
                 the quantity should be multiplied, in order to go from the
                 individual-particle representation to the full-macroparticle
                 representation
  - example: Let us consider a macroparticle that represents 100 electrons.
             In this case, `weighting` is w=100 and the charge of each
             underlying individual particle is q=-1.6e-19. Then the charge Q of
             the full macroparticle is given by: Q=q w^1 and therefore
             `weightingPower` must be 1.
  - advice to implementors: reading example (with h5py) and extracting charge
                            of the macroparticles in Python. When not
                            absolutely necessary, reading the additional
                            `weighting` record can be avoided for performance
                            reasons like this:
```python
f = h5py.File('example.h5')
species = f["<path_to_species_group>"]
q = species["charge"][:]
u_si = q.attrs["unitSI"]
p = q.attrs["weightingPower"]
if q.attrs["macroWeighted"] == 0 and p != 0:
    w = species["weighting"][:]
    q_macro = u_si * q * w**p
else :
    # No need to read the weighting from disk
    q_macro = u_si * q
```

### Namings for `Records` per Particle Species

When added as records to a particle output, the following naming conventions
shall be used to allow an easy identification of essential particle
properties. If these namings are not used, tools might still detect a particles
property by it's `unitDimension` as, e.g., *an* arbitrary momentum (could be,
e.g., an additional record defined by the user that stores the integrated
momentum change due to collisions) but not as *the* particle momentum that
should be used to push the particle.

  - `charge`
    - type: *(floatX)* or *(intX)* or *(uintX)*
    - description: electric charge of the macroparticle or of the underlying
                   individual particle (depending on the `macroWeighted` flag)
    - advice to implementors: must have `weightingPower = 1` and
                              `unitDimension = (0., 0., 1., 1., 0., 0., 0.)`
                              (charge = current * time)

  - `mass`
    - type: *(floatX)* or *(intX)* or *(uintX)*
    - description: mass of the macroparticle or of the underlying individual
                   particle (depending on the `macroWeighted` flag)
    - advice to implementors: must have `weightingPower = 1` and
                              `unitDimension = (0., 1., 0., 0., 0., 0., 0.)`
                              (mass)

  - `weighting`
    - type: *(floatX)* or *(intX)* or *(uintX)*
    - description: the number of underlying individual particles that
                   the macroparticles represent
    - advice to implementors: must have `weightingPower = 1`,
                              `macroWeighted = 1`, `unitSI = 1` and
                              `unitDimension == (0., ..., 0.)`

  - `momentum/` + components such as `x`, `y` and `z`
    - type: each component in *(floatX)* or *(intX)* or *(uintX)*
    - description: component-wise momentum of the macroparticle or of the
                   underlying individual particle (depending on the
                   `macroWeighted` flag)
    - advice to implementors: must have `weightingPower = 1` and
                              `unitDimension = (1., 1., -1., 0., 0., 0., 0.)`
                              (momentum = mass * length / time)

  - `position/` + components such as `x`, `y` and `z`
    - type: each component in *(floatX)* or *(intX)* or *(uintX)*
    - description: component-wise position of a particle, relative to
                   `positionOffset`
      - in the case where the `component`s of `positionOffset` are constant,
        position is the position relative to a global offset (e.g., the offset
        of a moving window)
      - in the case where the `component`s of `positionOffset` are
        non-constant, `position` must represent the in-cell-position and
        `positionOffset` must represent the position of the beginning of the
        cell (see below)
    - rationale: dividing the particle position in a beginning of the cell
                 (as *(intX)*) and in-cell position (as *(floatX)*) can
                 dramatically improve the precision of stored particle
                 positions; this division creates a connection between
                 particles and the fields on their cells
    - advice to implementors: must have `weightingPower = 0` and
                              `unitDimension = (1., 0., 0., 0., 0., 0., 0.)`
                              (length)
    - advice to implementors: a *(floatX)* type is likely the most frequent case
                              for this record
    - example: use only `x` and `y` in 2D

  - `positionOffset/` + components such as `x`, `y` and `z`
    - type: each component in *(floatX)* or *(intX)* or *(uintX)*
    - description: if the `component`s of this record are non-constant
                   this must represent the position of the beginning of the
                   cell the particle is associated with;
                   for the zero-based index `i` of the first cartesian field
                   coordinate, the position of the beginning of the cell is
                   defined via `gridGlobalOffset + i * gridSpacing`;
                   the `unitSI` of each component must be set to the
                   corresponding lengths of the cell's edges in SI units
    - advice to implementors: the interpretation of `position` and
                              `positionOffset` does not alter the pure
                              calculation of the global position of the
                              particle from the base standard; see the base
                              standard for a code example
    - advice to implementors: must have `weightingPower = 0` and
                              `unitDimension = (1., 0., 0., 0., 0., 0., 0.)`
                              (length)
    - advice to implementors: an *(intX)* or *(uintX)* type is likely the most
                              frequent case for this record
    - advice to implementors: if you want to neglect the relation between
                              particles and their cells, simply store this
                              record with constant components, e.g., the
                              global moving window offset

  - `particlePatches`
    - description: if this sub-group is used in combination with non-constant
                   components in the `positionOffset` components, the
                   position for `offset` and `extent` refers to the
                   position of the beginning of the cell (see `positionOffset`)
    - advice to implementors: the calculation and description of
                              `position` and `positionOffset` is as in
                              the base standard still the same;
                              for non-constant components in `positionOffset`
                              (beginning-of-cell representation) one can simply
                              check `offset` and `extent` against the
                              `positionOffset` record to select particles
                              in patches "by cell"

  - `boundElectrons`
    - type: *(floatX)* or *(intX)* or *(uintX)*
    - description: number of bound electrons of an ion/atom;
                   to provide information to atomic physics algorithms
    - advice to implementors: must have `weightingPower = 1` and
                              `unitDimension = (0., ..., 0.)` (dimensionless)

  - `protonNumber`
    - type: *(floatX)* or *(intX)* or *(uintX)*
    - description: the atomic number Z of an ion/atom;
                   to provide information to atomic physics algorithms
    - advice to implementors: must have `weightingPower = 1` and
                              `unitDimension = (0., ..., 0.)` (dimensionless)

  - `neutronNumber`
    - type: *(floatX)* or *(intX)* or *(uintX)*
    - description: the neutron number N = the mass number - A and
                   the atomic number Z of an ion/atom;
                   to provide information to atomic physics algorithms
    - advice to implementors: must have `weightingPower = 1` and
                              `unitDimension = (0., ..., 0.)` (dimensionless)
