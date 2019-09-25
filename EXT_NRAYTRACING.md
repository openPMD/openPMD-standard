Domain-Specific Naming Conventions for Neutron raytracing codes
===============================================================

openPMD extension name: `NRAYTRACING`


Introduction
------------

This extention is designed for transfer of neutron particle states between neutron raytracing simulation codes.
The neutrons are saved in rays with a given weight corresponding to expected intensity.
This standard is not yet finished and is currently based on EXT_BeamPhysics / EXT_WAVEFRONT

Particle Records
----------------

- `position/`
    - type: Required 3-vector *(real)*
    - components: (`x`, `y`, `z`)
    - description: particle Position relative to the `positionOffset`.
    That is, true position relative to the coordinate origin = `position + positionOffset`.

- `positionOffset/`
    - type: Optional 3-vector *(real)*
    - description: Offset for each particle position component relative to the coordinate origin. Assumed zero if not present.
    - components: (`x`, `y`, `z`)
    
- `spin/`
    - type: Optional 3-vector *(real)*
    - description: Particle spin.
    - components: (`x`, `y`, `z`) or (`r`, `theta`, `phi`).
    
- `time/`
    - type: Optional *(real)*
    - description: Time relative to `timeOffset`. That is, absolute time = `time + timeOffset`.
    
- `timeOffset/`
    - type: Optional *(real)*
    - description: Base time from which `time` is measured. That is, absolute time = `time + timeOffset`. Assumed zero if not present. Some programs will use the `timeOffset` to store the **reference time** in which case `time` will then be the deviation from the reference.

- `velocity/`
  - type: Required 3-vector *(real)*
  - description: (`x`, `y`, `z`) velocity vector. Meant to be used for photons where using `momentum` is not appropriate.

- `weight/`
    - type: Required *(real)*
    - description: Weight of the neutron ray with the physical unit of intensity, neutrons per second. When simulating a source with a given intensity, this intensity is split up into weights of the neutron rays that will be simulated.
    
    
