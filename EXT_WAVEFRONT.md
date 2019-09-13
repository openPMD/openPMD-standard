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
    - description: The list of beamline elements

  - `beamline parameters`
    - type: array of *(int)* of shape 11 `N`
    - scope: *required* if `beamline` is present
TODO: check dimensions
    - description: The 11 propagation parameters for each of the `N` beamline elements.

### Additional Attributes for each `mesh record` (field record)

The following additional attributes for `mesh record`s are defined in this
extension. The individual requirement is given in `scope`.

  - `Fourier domain`
    - type: *(string)*
    - scope: *required*
    - description: Indicates whether the data represents a field in time or
      frequency (energy) domain.
    - allowed values:
      - `time`: The field is given for the time domain.
      - `frequency`: The field is given for the frequency (energy) domain.

### Naming Conventions for `mesh record`s (field records)

When added to an output, the following naming conventions shall be used for
`mesh records` to allow an easy the identification of essential fields. If
these namings are not used, tools might still detect a record by it's
`unitDimension` as, e.g., *an* electric field but not as *the* main electric
field that should be distributed again on the cells.

- fundamental fields:
  - `E_real`
    - type: *(floatX)* or *(intX)* or *(uintX)*
    - description: the real part of the complex electric field.
    - advice to implementors: a *(floatX)* type is likely the most frequent case
                              for this record
TODO: check unit dimensions
    - advice to implementors: must have
                              `unitDimension = (1., 1., -3., -1., 0., 0., 0.)`
                              (V/m = kg * m / (A * s^3))
                              if attribute `Fourier domain` is 'time', or
                              `unitDimension = (1., 1., -3., -1., 0., 0., 0.)`
                              (V/m = kg * m / (A * s^3))
                              if attribute `Fourier domain` is 'frequency`.

  - `E_imag`
    - type: *(floatX)* or *(intX)* or *(uintX)*
    - description: the imaginary part of the complex electric field.
    - advice to implementors: must have
                              `unitDimension = (1., 1., -3., -1., 0., 0., 0.)`
                              if attribute `Fourier domain` is 'time', or
                              `unitDimension = (1., 1., -3., -1., 0., 0., 0.)`
                              (V/m = kg * m / (A * s^3))
                              if attribute `Fourier domain` is 'frequency`.

   - advice to implementors: a *(floatX)* type is likely the most frequent case
                              for this record


