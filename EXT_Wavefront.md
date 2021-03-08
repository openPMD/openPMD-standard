Domain-Specific Naming Conventions for Coherent Wavefront Propagation Codes
===========================================================================

openPMD extension name: `Wavefront`


Introduction
------------

This extension is specifically designed for the domain of coherent wavefront propagation codes.



Mesh Based Records (Fields)
---------------------------

### Naming Conventions for `mesh record`s (field records)

When added to an output, the following naming conventions shall be used for complex
electric field `mesh records`. 


- `electricField/` 
  - type: *(complexX)*
  - scope: *(required)*  
  - components:
    - `x/` 
    - `y/` 
    - `z/`     
  - decription: electric field representing the wavefront. The field oscillate as $\exp(-i \omega t)$, where the angular frequency $\omega$ is related to `photonEnergy` defined below. The real field at a time $t$ is then $\Re($ `electricField` * $\exp(-i \omega t)$)
  
  - advice to implementors: if attribute `temporal domain` is `'time'`, this is an electric field with SI unit in `V/m`, and therefore must have:
    - `unitDimension = (1, 1, -3, -1, 0, 0, 0)`  (electric field)
  - advice to implementors: if attribute `temporal domain` is `'frequency'`, this must have:
    - `unitDimension = (0. -1, 0, 0, 0, 0, 0)` (inverse length, as $\sqrt{\textrm{J} / \textrm{eV} }/ \textrm{m}  = \textrm{m}^{-1}$)


### Additional attributes on the `mesh record` named `electricField`

On the `series` object, set the following attributes:

  - `photonEnergy`
    - type: *(floatX)* 
    - description: The central photon energy of the wavefield $E_\textrm{photon} = \hbar \omega $, where $\hbar$ is Planck's constant divided by $2\pi$.
    - scope: *required*
    - `unitDimension = (2., 1., -2., 0., 0., 0., 0.)` (energy)


  - `temporalDomain`
    - type: *(string)*
    - scope: *required*
    - description: Indicates whether the data represents a field in time or
      frequency (energy) domain.
    - allowed values:
      - `time`: The field is given for the time domain.
      - `frequency`: The field is given for the frequency (energy) domain.
      
      
  - `spatialDomain`
    - type: *(string)*
    - scope: *required*
    - description: Indicates whether the data represents a field in cartesian
      (r) or reciprocal (k) space.
    - allowed values:
      - `r`: The field is given in cartesian space.
      - `k`: The field is given in reciprocmal space.
      
 
  - `zCoordinate`
    - type: *(floatX)*
    - description: The z coordinate with respect to the beamline origin.
    - `unitDimension = (1., 0., 0., 0., 0., 0., 0.)` (length)
    - scope: *required*      


  - `beamline`
    - type: *(string)*
    - scope: *optional*
    - description: The string representation of the optical beamline.


  - `radiusOfCurvatureX`
    - type: *(floatX)*
    - scope: *optional*
    - description: Horizontal wavefront curvature radius.
    - `unitDimension = (1., 0., 0., 0., 0., 0., 0.)` (length)


  - `radiusOfCurvatureY`
    - type: *(floatX)*
    - scope: *optional*
    - description: Vertical wavefront curvature radius.
    - `unitDimension = (1., 0., 0., 0., 0., 0., 0.)` (length)


  - `deltaRadiusOfCurvatureX`
    - type: *(floatX)*
    - scope:*optional*
    - description: Error in horizontal wavefront curvature radius.
    - `unitDimension = (1., 0., 0., 0., 0., 0., 0.)` (length)


  - `deltaRadiusOfCurvatureY`
    - type: *(floatX)*
    - scope: *optional*
    - description: Error in vertical wavefront curvature radius.
    - `unitDimension = (1., 0., 0., 0., 0., 0., 0.)` (length)



