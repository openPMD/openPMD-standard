Conventions for Weighted Particles
==================================

openPMD extension name: `ParticleWeighting`


Introduction
------------

In the description of discrete particle distributions, it is common to represent a collection of particles with fewer, representative particles. A typical approach is to assign a weight to each particle, which scales all physical properties it represents accordingly.


Particle Records
----------------

Weighted particles are also known as macroparticles.

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
# `default` handles the case where conversion to SI is not provided
u_si = q.attrs.get("unitSI", default=1.)
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
shall be used.

  - `weighting`
    - type: *(floatX)* or *(intX)* or *(uintX)*
    - description: the number of underlying individual particles that
                   the macroparticles represent
    - advice to implementors: must have `weightingPower = 1`,
                              `macroWeighted = 1`, `unitSI = 1` and
                              `unitDimension == (0., ..., 0.)`

