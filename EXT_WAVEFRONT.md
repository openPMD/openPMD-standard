Domain-Specific Naming Conventions for Coherent Wavefront Propagation Codes
===========================================================================

openPMD extension name: `WAVEFRONT`


Introduction
------------

This extension is specifically designed for the domain of coherent wavefront propagation codes.

Additional attributes on `series`
---------------------------------
On the `series` object, set the following attributes:

  - `beamline`
    - type: *(string)*
    - scope: *optional*
    - description: The string representation of the optical beamline.

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

Additional records
------------------
- `z coordinate`
    -type: *(floatX)*
    -description: The z coordinate with respect to the beamline origin.
    - `unitDimension = (1., 0., 0., 0., 0., 0., 0.)` (m)
    - scope: *required*

- `photon energy`
    - type: *(floatX)* or *(intX)* or *(uintX)*
    - description: The central photon energy of the wavefield.
    - `unitDimension = (1., 2., -2., 0., 0., 0., 0.)` (J = kg m^2/s^2)
    - `unitSI = 1.602176634e−19`
    - scope: *required*

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


Mesh records
------------

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


