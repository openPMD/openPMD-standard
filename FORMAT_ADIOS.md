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
