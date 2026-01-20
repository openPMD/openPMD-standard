# Implementation Details: ADIOS1/2

## Datatype Conventions

### Boolean Types

ADIOS1 (BP3) was traditionally a C library and as such as no notion for boolean types.
[At the moment](https://github.com/ornladios/ADIOS2/issues/2606), also ADIOS2 (BP4) does not define boolean types.
Although the openPMD-standard avoids using boolean types itself, developers might choose to implement them as attributes or dataset types.

#### ADIOS1

ADIOS1 is deprecated.

For compatibility, boolean types shall be written as `adios_unsigned_byte`.

On the read side, a stored boolean type is identified as `adios_unsigned_byte`, since no convention for bool-identification is specified.

#### ADIOS2

For compatibility, boolean types shall be stored as `unsigned char`.
ADIOS2 internally identifies this as `uint8_t`.

On the read side, a stored boolean *attribute* is associated with an attribute itentifying it as boolean for data readers.
The additional attribute is prefixed with `__is_boolean__/` and then adding the full path of the described attribute.

Output from `bpls -A` for a boolean attribute `pybool` stored in the location of the root group (path `/`):
```
  uint8_t         /pybool                      attr
  uint8_t         __is_boolean__/pybool        attr
```

There is no convention yet for a unique representation of ADIOS2 variables with boolean type.
Thus, implementations should cast the data to and from `unsigned char` instead.

## `variableBased` Encoding of Iterations

The `iterationEncoding` mode `variableBased` must be implemented via ADIOS steps.

## Datasets

An openPMD **data set** is represented by an ADIOS `Variable` at the location where it would usually be stored.

**attributes** are defined further below and can also appear at the dataset's **group** prefix level.

## Attributes

openPMD **attributes** stored as ADIOS `Attributes` at the location where they would usually be stored.

Example for a mesh record `E` with record component `x` and attributes `unitDimension` and `unitSI`:
```
  double    /data/meshes/E/unitDimension          attr   = {1, 1, -3, -1, 0, 0, 0}
  double    /data/meshes/E/x                      {128, 2048, 128}
  double    /data/meshes/E/x/position             attr   = {0.5, 0.5, 0.5}
  double    /data/meshes/E/x/unitSI               attr   = 1.22627e+13
```

This example uses `variableBased` iteration encoding, but other iteration encodings would work similarly with their respective `basePath` prefix.

