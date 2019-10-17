Domain-Specific Naming Conventions for Coherent Wavefront Propagation Codes
===========================================================================

openPMD extension name: `WAVEFRONT`


Introduction
------------

This extension is specifically designed for the domain of electro-dynamic and
electro-static particle-in-cell (PIC) codes.

Mesh Based Records (Fields)
---------------------------

### Additional Attributes for the Group `meshesPath`

The following additional attributes are defined to this extension.
The individual requirement is given in `scope`.

  - `beamline`
    - type: array *(string)*
    - scope: *optional*
    - description: The string representation of the optical beamline.

  - `photon energy`
    - type: *(floatX)* or *(intX)* or *(uintX)*
    - description: The central photon energy of the wavefield.
    - `unitDimension = (1., 0., 0., 0., 0., 0., 0.)` (m)1
    - `unitSI = 1.602176634e−19`
    - scope: *required*

  - `temporal domain`
    - type: *(string)*
    - scope: *required*
    - description: Indicates whether the data represents a field in time or
      frequency (energy) domain.
    - allowed values:
      - `time`: The field is given for the time domain.
      - `frequency`: The field is given for the frequency (energy) domain.

  - `spatial domain`
    - type: *(string)*
    - scope: *required*
    - description: Indicates whether the data represents a field in cartesian
      (r) or reciprocal (k) space.
    - allowed values:
      - `r`: The field is given in cartesian space.
      - `k`: The field is given in reciprocmal space.

  - `R/x`
    - type: *(floatX)*
    - scope: *required*
    - description: Horizontal wavefront curvature radius.
    - advice to implementors: must have
                              `unitDimension = (1., 0., 0., 0., 0., 0., 0.)`
                              (m)

  - `R/y`
    - type: *(floatX)*
    - scope: *required*
    - description: Vertical wavefront curvature radius.
    - advice to implementors: must have
                              `unitDimension = (1., 0., 0., 0., 0., 0., 0.)`
                              (m)

  - `Delta_R/x`
    - type: *(floatX)*
    - scope: *required*
    - description: Error in horizontal wavefront curvature radius.
    - advice to implementors: must have
                              `unitDimension = (1., 0., 0., 0., 0., 0., 0.)`
                              (m)

  - `Delta_R/y`
    - type: *(floatX)*
    - scope: *required*
    - description: Error in vertical wavefront curvature radius.
    - advice to implementors: must have
                              `unitDimension = (1., 0., 0., 0., 0., 0., 0.)`
                              (m)


### Naming Conventions for `mesh record`s (field records)

When added to an output, the following naming conventions shall be used for
electric field `mesh records`.

- fundamental fields:
  - `E_real/x` and `E_real/y`
    - type: *(floatX)* or *(intX)* or *(uintX)*
    - description: the real part of the complex electric field.
    - advice to implementors: a *(floatX)* type is likely the most frequent case
                              for this record
    - advice to implementors: must have
                              `unitDimension = (0., 0.5, -1.5, 0., 0., 0., 0.)`
                              (W^{1/2} / m = (kg / s^3)^{1/2})
                              if attribute `Fourier domain` is 'time', or
                              `unitDimension = (0., -1,0, 0., 0., 0., 0., 0.)`
                              ((J / eV)^{1/2} / m  = m^{-1})
                              if attribute `Fourier domain` is 'frequency`.
 
 - `E_imag/x` and `E_imag/y`
    - type: *(floatX)* or *(intX)* or *(uintX)*
    - description: the imaginary part of the complex electric field.
    - advice to implementors: a *(floatX)* type is likely the most frequent case
                              for this record
    - advice to implementors: must have
                              `unitDimension = (0., 0.5, -1.5, 0., 0., 0., 0.)`
                              (W^{1/2} / m = (kg / s^3)^{1/2})
                              if attribute `Fourier domain` is 'time', or
                              `unitDimension = (0., -1,0, 0., 0., 0., 0., 0.)`
                              ((J / eV)^{1/2} / m  = m^{-1})
                              if attribute `Fourier domain` is 'frequency`.


