Domain-Specific Naming Conventions for Neutron raytracing codes
===============================================================

openPMD extension name: `NRAYTRACING`


Introduction
------------

This extention is designed for transfer of neutron particle states between neutron raytracing simulation codes.
The neutrons are saved in rays with a given weight corresponding to expected intensity.
This standard is not yet finished and is currently based on EXT_BeamPhysics / EXT_WAVEFRONT

Each record needs to have the same length, as the n'th index for each record correspond to particle n.

Coordinates are defined with z in the beam direction and if possible y in the direction opposite gravity.

Particle Records
----------------

- `position/`
    - type: Required
    - description: particle Position relative to the `positionOffset`.
    That is, true position relative to the coordinate origin = `position + positionOffset`.
    - `x` 
        - type: Required *(real)*
        - description: x coordinate
        - unitDimension: [m] (1., 0., 0., 0., 0., 0., 0.)
        - unitSI: 1.0      
    - `y` 
        - type: Required *(real)*
        - description: y coordinate
        - unitDimension: [m] (1., 0., 0., 0., 0., 0., 0.)        
        - unitSI: 1.0      
    - `z` 
        - type: Required *(real)*
        - description: z coordinate
        - unitDimension: [m] (1., 0., 0., 0., 0., 0., 0.)        
        - unitSI: 1.0

- `positionOffset/`
    - type: Optional
    - description: Offset for each particle position component relative to the coordinate origin. Assumed zero if not present. If only one present, assumed the same for each particle.
    - `x` 
        - type: Optional *(real)*
        - description: x coordinate offset
        - unitDimension: [m] (1., 0., 0., 0., 0., 0., 0.)
        - unitSI: 1.0      
    - `y` 
        - type: Optional *(real)*
        - description: y coordinate offset
        - unitDimension: [m] (1., 0., 0., 0., 0., 0., 0.)        
        - unitSI: 1.0      
    - `z` 
        - type: Optional *(real)*
        - description: z coordinate offset
        - unitDimension: [m] (1., 0., 0., 0., 0., 0., 0.)   
        - unitSI: 1.0      
    
- `velocity/`
    - type: Required
    - description: (`x`, `y`, `z`) velocity vector. Used over momentum due to direct relevance for ray-tracing.
    - `x` 
        - type: Required *(real)*
        - description: x velocity
        - unitDimension: [m/s] (1., 0., -1.0, 0., 0., 0., 0.)
        - unitSI: 1.0      
    - `y` 
        - type: Required *(real)*
        - description: y velocity
        - unitDimension: [m/s] (1., 0., -1.0, 0., 0., 0., 0.)    
        - unitSI: 1.0      
    - `z` 
        - type: Required *(real)*
        - description: z velocity
        - unitDimension: [m/s] (1., 0., -1.0, 0., 0., 0., 0.)
        - unitSI: 1.0
    
- `spin/`
    - type: Optional 
    - description: Particle spin direction, no unit
    - `x` 
        - type: Optional *(real)*
        - description: x component of spin
        - unitDimension: [unitless] (0., 0., 0., 0., 0., 0., 0.)
        - unitSI: 1.0
    - `y` 
        - type: Optional *(real)*
        - description: y component of spin
        - unitDimension: [unitless] (0., 0., 0., 0., 0., 0., 0.)
        - unitSI: 1.0
    - `z` 
        - type: Optional *(real)*
        - description: z component of spin
        - unitDimension: [unitless] (0., 0., 0., 0., 0., 0., 0.)
        - unitSI: 1.0        
    
- `time/`
    - type: Required *(real)*
    - description: Time relative to `timeOffset`. That is, absolute time = `time + timeOffset`.
    - unitDimension: [unitless] (0., 0., 0., 1., 0., 0., 0., 0.)
    - unitSI: 1.0        
    
- `timeOffset/`
    - type: Optional *(real)*
    - description: Base time from which `time` is measured. That is, absolute time = `time + timeOffset`. Assumed zero if not present. Some programs will use the `timeOffset` to store the **reference time** in which case `time` will then be the deviation from the reference.
    - unitDimension: [unitless] (0., 0., 0., 1., 0., 0., 0., 0.)
    - unitSI: 1.0            

- `weight/`
    - type: Required *(real)*
    - description: Weight of the neutron ray with the physical unit of intensity, neutrons per second. When simulating a source with a given intensity, this intensity is split up into weights of the neutron rays that will be simulated.
    - unitDimension: [unitless] (0., 0., 0., 1., 0., 0., 0., 0.)
    - unitSI: 1.0
